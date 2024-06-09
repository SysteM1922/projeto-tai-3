from argparse import ArgumentParser
import os

def main():

    parser = ArgumentParser(description='Generate a .freq file for each of the .wav files in the input directory')
    parser.add_argument('-d', '--input_dir', help='Path to the input directory', type=str, required=True)
    parser.add_argument('-o', '--output_dir', help='Path to the output directory', type=str, required=True)
    parser.add_argument('-v', '--verbose', help='Print additional information', action='store_true', default=False)
    parser.add_argument('-ws', '--window_size', help='Size of the window for computing the FFT', type=int, default=1024)
    parser.add_argument('-sh', '--shift', help='Window overlap', type=int, default=256)
    parser.add_argument('-ds', '--downsample', help='Down-sampling factor', type=int, default=4)
    parser.add_argument('-nf', '--num_freqs', help='Number of significant frequencies', type=int, default=4)
    args = parser.parse_args()

    if not args.input_dir:
        print('Please provide a path to the input directory')
        return
    
    if not os.path.isdir(args.input_dir):
        print('Input directory does not exist')
        return
    
    if not args.output_dir:
        print('Please provide a path to the output directory')
        return
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    extra_args = f'-ws {args.window_size} -sh {args.shift} -ds {args.downsample} -nf {args.num_freqs}'

    if args.verbose:
        extra_args += ' -v'
    
    for file_name in os.listdir(args.input_dir):
        if file_name.endswith('.wav'):
            music_name = file_name.split('.')[0]
            freq_path = f'{args.output_dir}/{music_name}.freq'
            print(f'--- {music_name} ---')
            
            command = f'./GetMaxFreqs/bin/GetMaxFreqs -w "{freq_path}" {extra_args} "{args.input_dir}/{file_name}"'
            os.system(command)
            
    with open(f'{args.output_dir}/__args', 'w') as f:
        f.write(extra_args)

if __name__ == '__main__':
    main()
