#include <iostream>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

int main(int argc, char* argv[]) {

	if(argc < 5) {
		cerr << "Usage: GetMaxFreqs [ -v (verbose) ]" << endl;
		cerr << "                   [ -ws winSize ]" << endl;
		cerr << "                   [ -sh shift ]" << endl;
		cerr << "                   [ -ds downSampling ]" << endl;
		cerr << "                   [ -nf nFreqs ]" << endl;
		cerr << "                   [ -mF musicsFolder ]" << endl;
        cerr << "                   [ -fF freqsFolder ]" << endl;
		return 1;
	}

    string musics_folder = "";
    string freqs_folder = "";

    string extra_args = "";

    for(int n = 1 ; n < argc ; n++) {
        if(string(argv[n]) == "-mF") {
            musics_folder = argv[n+1];
            n++;
        } else if(string(argv[n]) == "-fF") {
            freqs_folder = argv[n+1];
            n++;
        } else {
            extra_args += " " + string(argv[n]);
        }
    }

    cout << "musics_folder: " << musics_folder << endl;
    cout << "freqs_folder: " << freqs_folder << endl;

    if (!fs::exists(musics_folder)) {
        cout << "Error: " << musics_folder << " does not exist" << endl;
        return 1;
    }

    if (!fs::exists(freqs_folder)) {
        if (system(("mkdir " + freqs_folder).c_str()) != 0) {
            cout << "Error: " << freqs_folder << " could not be created" << endl;
            return 1;
        }
    }

    for (const auto & entry : fs::directory_iterator(musics_folder)) {
        string music_path = entry.path();
        string music_name = music_path.substr(music_path.find_last_of("/\\") + 1);
        music_name = music_name.substr(0, music_name.find_last_of("."));
        string freq_path = freqs_folder + "/" + music_name + ".freq";

        string command = "./GetMaxFreqs/bin/GetMaxFreqs -w \"" + freq_path + "\"" + extra_args + " '" + music_path + "'";
        cout << "--- " <<music_name << " ---" << endl;
        if (system(command.c_str()) != 0) {
            cout << "Error: " << command << endl;
            return 1;
        }
    }

    return 0;
}