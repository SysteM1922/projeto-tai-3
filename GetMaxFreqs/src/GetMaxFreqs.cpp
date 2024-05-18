//
// Armando J. Pinho, ap@ua.pt, 2016-2020
//
// See:
// http://www.mega-nerd.com/libsndfile
// http://www.fftw.org
//
// In linux, compile with:
// g++ -W -Wall -std=c++11 -o GetMaxFreqs GetMaxFreqs.cpp -lsndfile -lfftw3 -lm
//
// It should accept .wav and .flac audio files, stereo, sampled at 44100 Hz, 16 bits
//
// Example:
// GetMaxFreqs -w test.freqs test.wav
//
// File test.freqs will contain the "signature" of the audio file test.wav
//
#include <iostream>
#include <fstream>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <sndfile.hh>
#include <fftw3.h>

#define WS	1024	// Size of the window for computing the FFT
#define SH	256		// Window overlap
#define DS	4		// Down-sampling factor
#define NF	4		// Number of significant frequencies

using namespace std;

int main (int argc, char* argv[]) {

	bool verbose { false };
	char* oFName = nullptr;
	ofstream os;
	int ws { WS };
	int sh { SH };
	int ds { DS };
	int nf { NF };

	if(argc < 2) {
		cerr << "Usage: GetMaxFreqs [ -v (verbose) ]" << endl;
		cerr << "                   [ -w freqsFile ]" << endl;
		cerr << "                   [ -ws winSize ]" << endl;
		cerr << "                   [ -sh shift ]" << endl;
		cerr << "                   [ -ds downSampling ]" << endl;
		cerr << "                   [ -nf nFreqs ]" << endl;
		cerr << "                   AudioFile" << endl;
		return 1;
	}

	for(int n = 1 ; n < argc ; n++)
		if(string(argv[n]) == "-v") {
			verbose = true;
			break;
		}

	for(int n = 1 ; n < argc ; n++)
		if(string(argv[n]) == "-w") {
			oFName = argv[n+1];
			break;
		}

	for(int n = 1 ; n < argc ; n++)
		if(string(argv[n]) == "-ws") {
			ws = atoi(argv[n+1]);
			break;
		}

	for(int n = 1 ; n < argc ; n++)
		if(string(argv[n]) == "-sh") {
			sh = atoi(argv[n+1]);
			break;
		}

	for(int n = 1 ; n < argc ; n++)
		if(string(argv[n]) == "-ds") {
			ds = atoi(argv[n+1]);
			break;
		}

	for(int n = 1 ; n < argc ; n++)
		if(string(argv[n]) == "-nf") {
			nf = atoi(argv[n+1]);
			break;
		}

	SndfileHandle audioFile { argv[argc-1] };
	if(audioFile.error()) {
		cerr << "Error: invalid audio file\n";
		return 1;
	}

	if(audioFile.channels() != 2) {
		cerr << "Error: currently supports only 2 channels\n";
		return 1;
	}

	if(audioFile.samplerate() != 44100) {
		cerr << "Error: currently supports only 44100 Hz of sample rate\n";
		return 1;
	}

	if(verbose) {
		printf("Sample rate : %d\n",  audioFile.samplerate());
		printf("Channels    : %d\n",  audioFile.channels());
		printf("Frames      : %ld\n", (long int)audioFile.frames());
	}

	if(oFName != nullptr) {
		os.open(oFName, ofstream::binary);
		if(!os) {
			cerr << "Warning: failed to open file to write\n";
		}

	}

	short* samples = new short[audioFile.frames() << 1];
	audioFile.readf(samples, audioFile.frames());

	fftw_complex in[ws] = {}, out[ws];
	fftw_plan plan;
	double power[ws/2];
	plan = fftw_plan_dft_1d(ws, in, out, FFTW_FORWARD, FFTW_ESTIMATE);

	for(int n = 0 ; n <= (audioFile.frames() - ws * ds) / (sh * ds) ; ++n) {
		for(int k = 0 ; k < ws ; ++k) { // Convert to mono and down-sample
			in[k][0] = (int)samples[(n * (sh * ds) + k * ds) << 1] +
			  samples[((n * (sh * ds) + k * ds) << 1) + 1];
			for(int l = 1 ; l < ds ; ++l) {
				in[k][0] += (int)samples[(n * (sh * ds) + k * ds + l) << 1] +
				  samples[((n * (sh * ds) + k * ds + l) << 1) + 1];
			}

		}

		fftw_execute(plan);

		for(int k = 0 ; k < ws/2 ; ++k)
			power[k] = out[k][0] * out[k][0] + out[k][1] * out[k][1];

		unsigned maxPowerIdx[ws/2];
		for(int k = 0 ; k < ws/2 ; ++k)
			maxPowerIdx[k] = k;

		partial_sort(maxPowerIdx, maxPowerIdx + nf, maxPowerIdx + ws/2,
		  [&power](int i, int j) { return power[i] > power[j]; });

		if(os) {
			for(int i = 0 ; i < nf ; ++i) {
				// To store in a byte, truncate to a max of 255
				os.put(maxPowerIdx[i] > 255 ? 255 : maxPowerIdx[i]);
			}

		}

	}

	delete[] samples;
	fftw_destroy_plan(plan);

	return 0 ;
}

