#
GetMaxFreqs converts audio files into a frequency-domain "signature".
Armando J. Pinho, ap@ua.pt, 2016-2020.

=== To build:

Please see "CMakeLists.txt" for library requirements.

For linux:
> make -f Makefile.linux clean; make -f Makefile.linux

For windows:
> make -f Makefile.windows clean; make -f Makefile.windows

For both linux and windows:
> make clean; make

=== Usage:

GetMaxFreqs [ -v (verbose) ]
            [ -w freqsFile ]
            [ -ws winSize ]
            [ -sh shift ]
            [ -ds downSampling ]
            [ -nf nFreqs ]
            AudioFile

-v
	Verbose. Some additional information is displayed.

-w freqsFile
    File in which the "signature" will be written.

-ws winSize
    Length (in number of audio samples) of the block (window) used for
    frequency analysis. The default value is 1024.

-sh shift
    Right shift (in number of audio samples) from one block to the next.
    The default value is 256.

-ds downSampling
    Down sampling (from the original 44100 samples per second). The default
    value is 4, i.e., 4:1, yielding 44100/4 = 11025 samples per second.

-nf nFreqs
    Number of (the most significant) frequency components retained for each
    block. The default value is 4.

AudioFile
    A .wav or .flac audio file, stereo (2 channels), sampled at 44100 Hz,
    16 bits per sample.

=== Example of use:

> ../bin/GetMaxFreqs -w test.freqs test.wav

