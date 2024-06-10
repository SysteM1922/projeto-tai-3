from argparse import ArgumentParser
import random
from pydub import AudioSegment
from pydub.generators import WhiteNoise
import numpy as np
import wave

random.seed(0) # for testing purposes // remove for production

def add_noise(audio_file: str, output_file: str, noise_level: float) -> None:
    
    with wave.open(audio_file, 'rb') as wav_file:
        params = wav_file.getparams()  # Pegar os parâmetros do áudio
        frames = wav_file.readframes(params.nframes)  # Ler os frames de áudio
        audio_data = np.frombuffer(frames, dtype=np.int16)  # Converter para array numpy

    # Gerar ruído
    noise = np.random.uniform(-1, 1, len(audio_data))

    # Normalizar o ruído
    noise = noise * noise_level * np.iinfo(np.int16).max

    # Adicionar ruído ao áudio
    noisy_audio = audio_data + noise

    # Assegurar que os valores estão dentro dos limites do tipo int16
    noisy_audio = np.clip(noisy_audio, -32768, 32767)

    # Converter para array de bytes
    noisy_audio = noisy_audio.astype(np.int16).tobytes()

    # Salvar o novo arquivo de áudio com ruído
    with wave.open(output_file, 'wb') as wav_file:
        wav_file.setparams(params)
        wav_file.writeframes(noisy_audio)

def add_analog_noise(audio_file: str, output_file: str) -> None:
    
    audio_data = AudioSegment.from_file(audio_file, format='wav')

    audio_data = audio_data.set_frame_rate(11025)

    audio_data = audio_data.low_pass_filter(4000)
    audio_data = audio_data.high_pass_filter(200)

    audio_data = audio_data.set_frame_rate(44100)

    white_noise = WhiteNoise().to_audio_segment(duration=len(audio_data), volume=-40)

    noisy_audio = audio_data.overlay(white_noise)

    noisy_audio.export(output_file, format='wav')


def add_echo(audio_file: str, output_file: str, delay: int = 500, decay: float = 0.5) -> None:
    
    audio_data = AudioSegment.from_file(audio_file, format='wav')
    echo_data = audio_data + audio_data.dBFS*(1-decay)

    # Adicionar eco ao áudio
    echo_audio = audio_data.overlay(echo_data, position=delay)

    # Salvar o novo arquivo de áudio com eco
    echo_audio.export(output_file, format='wav')

def add_noise_file(audio_file: str, output_file: str, noise_file: str) -> None:

    audio_data = AudioSegment.from_file(audio_file, format='wav')
    noise_data = AudioSegment.from_file(noise_file, format='wav')

    # Obter um trecho aleatório do ruído
    start = random.randint(0, len(noise_data) - len(audio_data))
    noise_data = noise_data[start:start + len(audio_data)]

    # Igualar amplitude do áudio e do ruído
    noise_data = noise_data + (audio_data.dBFS - noise_data.dBFS)

    # Adicionar o ruído ao áudio
    noisy_audio = audio_data.overlay(noise_data)

    # Salvar o novo arquivo de áudio com ruído
    noisy_audio.export(output_file, format='wav')


def main():
    parser = ArgumentParser(description='Add noise to an audio file')
    parser.add_argument('-f', '--file', help='Path to the audio file', type=str, required=True)
    parser.add_argument('-n', '--noise', help='Noise level', type=float, default=0.5)
    parser.add_argument('-e', '--echo', help='Echo delay in milliseconds', type=int, default=500)
    parser.add_argument('-d', '--decay', help='Echo decay', type=float, default=0.5)
    args = parser.parse_args()

    if not args.file:
        print('Please provide a path to the audio file')
        return
    
    audio_file = args.file.split('.')[0]

    add_noise(args.file, f"{audio_file}_noisy.wav", 1)
    add_analog_noise(args.file, f"{audio_file}_analog_noisy.wav")
    add_echo(args.file, f"{audio_file}_echo.wav", 500, 0.5)
    add_noise_file(args.file, f"{audio_file}_city_noisy.wav", "./noises/city-traffic-outdoor-6414.wav")
    add_noise_file(args.file, f"{audio_file}_cafe_noisy.wav", "./noises/cafe-noise-32940.wav")

if __name__ == '__main__':
    main()