import os
from find_music import find_music
import json

MUSICS_DIR = 'musics'
WS = 1024
SH = 256
DS = 4
NF = 4
SAMPLE_SIZE = 5
N = 0.5
E = 500
D = 0.5

os.system(f'python3 src/generate_freqs.py -d "{MUSICS_DIR}" -o freqs/ -ws {WS} -sh {SH} -ds {DS} -nf {NF}')

results = {}

for file in os.listdir(MUSICS_DIR):
    if not file.endswith('.wav'):
        continue

    music_name = file.split('.')[0]
    print(f"Processing {music_name}")

    results[music_name] = {}

    for run in range(10):
        print(f"Run {run}")
        os.system(f'python3 src/random_sample.py -f "{MUSICS_DIR}/{file}" -o sample -s {SAMPLE_SIZE}')
        os.system(f'python3 src/add_noise.py -f sample.wav -n {N} -e {E} -d {D}')

        results[music_name][run] = {}

        for compressor in ['gzip', 'bzip2', 'lzma', 'zstd', 'xz', 'lzop']:
            print(f"Compressor {compressor}")
            results[music_name][run][compressor] = {}
            for sample in ['sample.wav', 'sample_noisy.wav', 'sample_analog_noisy.wav', 'sample_echo.wav', 'sample_city_noisy.wav', 'sample_cafe_noisy.wav']:
                print(f"Sample {sample}")
                ranking = find_music(compressor, "", sample, 'freqs')
                result_idx = -1
                for idx, (music, result) in enumerate(ranking):
                    if music_name == music:
                        result_idx = idx
                        break

                results[music_name][run][compressor][sample] = {"top_3": ranking[:3], "guessed_rank": result_idx, "guessed": True if result_idx == 0 else False}

with open('results.json', 'w') as f:
    json.dump(results, f)