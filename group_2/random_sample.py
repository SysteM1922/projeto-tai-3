from argparse import ArgumentParser
import wave
import random
import os

#random.seed(0) # for testing purposes // remove for production

SAMPLE_SIZE = 5

def random_sample(file_path: str, sample_size: int, output_name: str) -> None:

    with wave.open(file_path, 'rb') as wav_file:
        params = wav_file.getparams()
        nframes = params.nframes
        framerate = params.framerate
        nchannels = params.nchannels
        sampwidth = params.sampwidth
        duration = nframes / framerate
        print(f'File: {file_path}')
        print(f'Number of frames: {nframes}')
        print(f'Frame rate: {framerate}')
        print(f'Number of channels: {nchannels}')
        print(f'Sample width: {sampwidth}')
        print(f'Duration: {duration} seconds')
        # generate random start time
        start_time = random.uniform(0, duration - sample_size)
        start_frame = int(start_time * framerate)
        # generate random end time
        end_time = start_time + sample_size
        end_frame = int(end_time * framerate)
        print(f'Start time: {start_time} seconds')
        print(f'End time: {end_time} seconds')
        print(f'Start frame: {start_frame}')
        print(f'End frame: {end_frame}')
        # read frames
        wav_file.setpos(start_frame)
        frames = wav_file.readframes(end_frame - start_frame)
        # save frames to new file
        _, file_extension = os.path.splitext(file_path)
        new_file_path = f'{output_name}{file_extension}'
        with wave.open(new_file_path, 'wb') as new_wav_file:
            new_wav_file.setparams(params)
            new_wav_file.writeframes(frames)
        print(f'New file: {new_file_path}')

def main():
    parser = ArgumentParser(description='Generate a random sample of SAMPLE_SIZE seconds from a .wav file')
    parser.add_argument('-s', '--sample_size', help='Size of the sample in seconds', type=int, default=SAMPLE_SIZE)
    parser.add_argument('-f', '--file_path', help='Path to the .wav file', type=str)
    parser.add_argument('-o', '--output_name', help='Name of the output file', type=str, default='sample')
    args = parser.parse_args()

    if not args.file_path:
        print('Please provide a path to the .wav file')
        return
    
    random_sample(args.file_path, args.sample_size, args.output_name)

if __name__ == '__main__':
    main()