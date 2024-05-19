# from a .wav file generate a random sample of 5 seconds abd save it as a new .wav file

from argparse import ArgumentParser
import wave
import random
import os

def random_sample(file_path):
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
        start_time = random.uniform(0, duration - 5)
        start_frame = int(start_time * framerate)
        # generate random end time
        end_time = start_time + 5
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
        new_file_path = f'sample{file_extension}'
        with wave.open(new_file_path, 'wb') as new_wav_file:
            new_wav_file.setparams(params)
            new_wav_file.writeframes(frames)
        print(f'New file: {new_file_path}')

def main():
    parser = ArgumentParser(description='Generate a random sample of 5 seconds from a .wav file')
    parser.add_argument('file_path', help='Path to the .wav file', type=str)
    args = parser.parse_args()

    if not args.file_path:
        print('Please provide a path to the .wav file')
        return
    
    random_sample(args.file_path)

if __name__ == '__main__':
    main()