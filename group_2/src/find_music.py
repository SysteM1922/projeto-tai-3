from argparse import ArgumentParser
import os
import shutil

TEMP_FOLDER = 'temp'
extension = ''

def compress_and_get_size(compressor: str, compressor_args: str, file: str) -> int:
    file_name = file.split('/')[-1]

    command = f'{compressor} {compressor_args} -c -k -f "{file}" > "{TEMP_FOLDER}/{file_name}.{extension}"'
    os.system(command)

    return os.path.getsize(f'{TEMP_FOLDER}/{file_name}.{extension}')

def concat_signatures(compressor: str, file1: str, file2: str) -> None:
    file1_name = file1.split('/')[-1]
    file2_name = file2.split('/')[-1]

    command = f'cat "{file1}" "{file2}" | {compressor} -c -k -f > "{TEMP_FOLDER}/{file1_name}_{file2_name}.freq"'
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

def find_music(compressor: str, compressor_args: str, sample: str, freqs_folder: str) -> list:

    set_extension(compressor)

    music_args = ""
    with open(f'{freqs_folder}/__args', 'r') as f:
        music_args = f.read().strip()

    if not os.path.exists(TEMP_FOLDER):
        os.mkdir(TEMP_FOLDER)

    command = f'./GetMaxFreqs/bin/GetMaxFreqs -w "{TEMP_FOLDER}/sample.freq" {music_args} "{sample}"'
    os.system(command)

    sample_size = compress_and_get_size(compressor, compressor_args, f'{TEMP_FOLDER}/sample.freq')

    music_ncd = {}

    for file in os.listdir(freqs_folder):
        if file.endswith('.freq'):
            file_size = compress_and_get_size(compressor, compressor_args, f'{freqs_folder}/{file}')
            concat_file = concat_signatures(compressor, f'{TEMP_FOLDER}/sample.freq', f'{freqs_folder}/{file}')
            concat_size = compress_and_get_size(compressor, compressor_args, concat_file)
            music_name = file.split('.')[0]
            music_ncd[music_name] = ncd(sample_size, file_size, concat_size)

    shutil.rmtree(TEMP_FOLDER)

    sorted_music_ncd = [(k, v) for k, v in sorted(music_ncd.items(), key=lambda item: item[1])]

    return sorted_music_ncd

def main():
    
    parser = ArgumentParser(description='Find the most similar audio files using Normalized Compression Distance')
    parser.add_argument('-c', '--compressor', help='Compressor to use (gzip, bzip2, lzma, zstd, xz, lzop)', type=str, required=True)
    parser.add_argument('-s', '--sample', help='Sample file', type=str, required=True)
    parser.add_argument('-f', '--freqs_folder', help='Folder with frequency files', type=str, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.freqs_folder):
        print('Folder with frequency files does not exist')
        return
    
    if not os.path.exists(args.sample):
        print('Sample file does not exist')
        return
    
    compressor = args.compressor.split()
    compressor_args = " ".join(compressor[1:])
    compressor = compressor[0]

    if compressor not in ['gzip', 'bzip2', 'lzma', 'zstd', 'xz', 'lzop']:
        print('Invalid compressor')
        return
    
    if os.system(f'which {compressor} > /dev/null') != 0:
        print(f'{compressor} is not installed or not in PATH')
        return

    ranking = find_music(compressor, compressor_args, args.sample, args.freqs_folder)

    for music, ncd_value in reversed(ranking):
        print("{:.6f} | {}".format(ncd_value, music))
    print(f'\nBest match:\n\t{ranking[0][0]}\n')
    
    
if __name__ == '__main__':
    main()