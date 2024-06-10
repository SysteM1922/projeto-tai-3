# Identify the Music (Group 2)
## Setup

To run our project you need to download the dataset provided in `dataset_url.txt` and unzip the file into a new folder.
Then we highly recommend creating a python virtual environment and installing the requirements present in the requirements.txt file.

## Generate Freqs


To run __generate_freqs.py__, you must run the following program with the following arguments:

- `-v` flag to activate verbose mode
- `-ws` length (in number of audio samples) of the block (window) used for frequency analysis. The default value is 1024
- `-sh` right shift (in number of audio samples) from one block to the next. The default value is 256.
- `-ds` down sampling (from the original 44100 samples per second). The default value is 4, i.e., 4:1, yielding 44100/4 = 11025 samples per second.
- `-nf` Number of (the most significant) frequency components retained for each block. The default value is 4.
- `-d` to specify the path to the .wav stereo 44100Hz musics directory 
- `-o` to specify the output folder where you want to write the "signatures" of the musics

### Examples of usage

```bash
python src/generate_freqs.py -d musics/ -o freqs/
```

```bash
python src/generate_freqs.py -v -ws 1024 -sh 256 -ds 4 -nf 4 -d musics/ -o freqs/
```

## Random Sample


To run __random_sample.py__, you must run the following program with the following arguments:

- `-s` to specify the size of the sample that we want to cut in seconds (default = 5 seconds)
- `-f` to specify the path to the .wav stereo 44100Hz music file that we want to sample from
- `-o` to specify the output name of the .wav stereo 44100Hz music file that we want to sample from (default = "sample")

### Examples of usage

```bash
python src/random_sample.py -f musics/Afterglow-Ed\ Sheeran-Afterglow.wav
```

```bash
python src/random_sample.py -s 5 -f musics/Afterglow-Ed Sheeran-Afterglow -o sample
```

## Add Noise

To run __add_noise.py__, you must run the following program with the following arguments:

- `-f` to specify the path to the .wav stereo 44100Hz sample file that we want to apply noise
- `-n` to specify the level of noise to be added to the constant noise sample (default = 0.5)
- `-e` to specify the echo delay to apply in milliseconds to the echoed sample (default = 500)
- `-d` to specify the echo decay to apply to the echoed sample (default = 0.5)

### Examples of usage

```bash
python src/add_noise.py -f sample.wav
```

```bash
python src/add_noise.py -f sample.wav -n 0.5 -e 500 -d 0.5 
```

## Find Music

To run __find_music.py__, you must run the following program with the following arguments:

- `-c` to specify the compressor and its configuration that we want to use
- `-s` to specify the path to the .wav stereo 44100Hz sample file that we want to know which song it belongs to
- `-f` to specify the folder the "signatures" of the musics are stored

```bash
python src/find_music.py -c xz -s sample.wav -f freqs/
```

```bash
python src/find_music.py -c "xz -9" -s sample.wav -f freqs/
```