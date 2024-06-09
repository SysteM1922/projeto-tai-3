from argparse import ArgumentParser
import os

TEMP_FOLDER = 'temp'
extension = ''

def compress_and_get_size(compressor: str, file: str) -> int:
    file_name = file.split('/')[-1]

    command = f'{compressor} -c "{file}" > "{TEMP_FOLDER}/{file_name}.{extension}"'
    os.system(command)

    return os.path.getsize(f'{TEMP_FOLDER}/{file_name}.{extension}')

def concat_signatures(compressor: str, file1: str, file2: str) -> None:
    file1_name = file1.split('/')[-1]
    file2_name = file2.split('/')[-1]

    command = f'cat "{file1}" "{file2}" | {compressor} > "{TEMP_FOLDER}/{file1_name}_{file2_name}.freq"'
    os.system(command)

    return f'{TEMP_FOLDER}/{file1_name}_{file2_name}.freq'

def ncd(x_size: int, y_size: int, xy_size: int) -> float:
    return (xy_size - min(x_size, y_size)) / max(x_size, y_size)

def set_extension(compressor: str) -> None:
    global extension
    if compressor == "gzip":
        extension = "gz"
    if compressor == "bzip2":
        extension = "bz2"
    if compressor == "lzma":
        extension = "lzma"
    if compressor == "zstd":
        extension = "zst"
    if compressor == "xz":
        extension = "xz"
    if compressor == "lzop":
        extension = "lzo"
    if compressor == "lz4":
        extension = "lz4"

def main():
    
    parser = ArgumentParser(description='Find the most similar audio files using Normalized Compression Distance')
    parser.add_argument('-c', '--compressor', help='Compressor to use (gzip, bzip2, lzma, zstd, xz, lzop, lz4)', type=str, required=True)
    parser.add_argument('-s', '--sample', help='Sample file', type=str, required=True)
    parser.add_argument('-ss', '--sample_size', help='Size of the sample in seconds', type=int, default=5)
    parser.add_argument('-f', '--freqs_folder', help='Folder with frequency files', type=str, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.freqs_folder):
        print('Folder with frequency files does not exist')
        return
    
    if not os.path.exists(args.sample):
        print('Sample file does not exist')
        return
    
    if args.compressor not in ['gzip', 'bzip2', 'lzma', 'zstd', 'xz', 'lzop', 'lz4']:
        print('Invalid compressor')
        return
    
    if os.system(f'which {args.compressor} > /dev/null') != 0:
        print(f'{args.compressor} is not installed or not in PATH')
        return

    set_extension(args.compressor)

    music_args = ""
    with open(f'{args.freqs_folder}/__args', 'r') as f:
        music_args = f.read().strip()

    if not os.path.exists(TEMP_FOLDER):
        os.mkdir(TEMP_FOLDER)

    command = f'./GetMaxFreqs/bin/GetMaxFreqs -w "{TEMP_FOLDER}/sample.freq" {music_args} "{args.sample}"'
    os.system(command)

    sample_size = compress_and_get_size(args.compressor, f'{TEMP_FOLDER}/sample.freq')

    music_ncd = {}

    for file in os.listdir(args.freqs_folder):
        if file.endswith('.freq'):
            file_size = compress_and_get_size(args.compressor, f'{args.freqs_folder}/{file}')
            concat_file = concat_signatures(args.compressor, f'{TEMP_FOLDER}/sample.freq', f'{args.freqs_folder}/{file}')
            concat_size = compress_and_get_size(args.compressor, concat_file)
            music_name = file.split('.')[0]
            music_ncd[music_name] = ncd(sample_size, file_size, concat_size)

    sorted_music_ncd = [(k, v) for k, v in sorted(music_ncd.items(), key=lambda item: item[1])]

    for music, ncd_value in reversed(sorted_music_ncd):
        print("{:.6f} | {}".format(ncd_value, music))

    print(f'\nBest match:\n\t{sorted_music_ncd[0][0]}\n')

    os.system(f'rm -rf {TEMP_FOLDER}')
    
if __name__ == '__main__':
    main()