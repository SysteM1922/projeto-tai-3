# Identify the Music (Group 2)
## Build Project

To build our project you need to download the dataset provided in `dataset_url.txt`, unzip the file into a new folder and run the build.sh script that was created in the root group_2 which will compile the necessary programs for the project, namely generate_freqs and find_music.

```bash
./build.sh
```

## Generate_Freqs


To run __Generate_Freqs__, you must run the following program with the following arguments:

- `-v` flag to activate verbose mode
- `-ws` length (in number of audio samples) of the block (window) used for frequency analysis. The default value is 1024
- `-sh` right shift (in number of audio samples) from one block to the next. The default value is 256.
- `-ds` down sampling (from the original 44100 samples per second). The default value is 4, i.e., 4:1, yielding 44100/4 = 11025 samples per second.
- `-nF` Number of (the most significant) frequency components retained for each block. The default value is 4.
- `-mF` to specify the path to the .wav stereo 44100Hz musics folder 
- `-fF` to specify the folder where we want to write the "signatures" of the musics

### Examples of usage

```bash
./generate_freqs -mF musics/ -fF freqs/
```

```bash
./generate_freqs -v -ws 1024 -sh 256 -ds 4 -nF 4 -mF musics/ -fF freqs/
```

## Random_Sample



## Benchmark

To run __Benchmark__, you must run the following program with the following arguments:

- `-a` to set the value of smoothing alpha
- `-d` to indicate the path to the test directory
- `-h` to specify the path to the human-written text training file
- `-c` to specify the path to the ChatGPT generated text training file
- `-n` to specify the size of the context we want to consider


### Example of usage

```bash
./bin/benchmark -a 1 -h dataset/train/train_human.txt -c dataset/train/train_ai.txt -d dataset/test_tiny/ -n 4
```
