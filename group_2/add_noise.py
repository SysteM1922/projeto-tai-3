import colorednoise as cn
import numpy as np
import wave

def add_noise(audio_file: str, output_file: str, noise_level: float) -> None:
    # Abrir o arquivo de áudio
    with wave.open(audio_file, 'rb') as wav_in:
        params = wav_in.getparams()  # Pegar os parâmetros do áudio
        frames = wav_in.readframes(params.nframes)  # Ler os frames de áudio
        audio_data = np.frombuffer(frames, dtype=np.int16)  # Converter para array numpy

    # Gerar ruído uniforme
    noise = np.random.uniform(-1, 1, audio_data.shape).astype(np.float32)

    # Escalar o ruído pelo nível de ruído desejado e converter para int16
    scaled_noise = (noise * noise_level * (2**15 - 1)).astype(np.int16)

    # Adicionar o ruído aos dados de áudio
    noisy_audio = audio_data + scaled_noise

    # Assegurar que os valores estão dentro dos limites do tipo int16
    noisy_audio = np.clip(noisy_audio, -2**15, 2**15 - 1)

    # Salvar o novo arquivo de áudio com ruído
    with wave.open(output_file, 'wb') as wav_out:
        wav_out.setparams(params)
        wav_out.writeframes(noisy_audio.tobytes())

def add_white_noise(audio_file: str, output_file: str, noise_level: float) -> None:
    # Abrir o arquivo de áudio
    with wave.open(audio_file, 'rb') as wav_in:
        params = wav_in.getparams()  # Pegar os parâmetros do áudio
        frames = wav_in.readframes(params.nframes)  # Ler os frames de áudio
        audio_data = np.frombuffer(frames, dtype=np.int16)  # Converter para array numpy

    # Gerar ruído branco
    noise = np.random.normal(0, noise_level, audio_data.shape).astype(np.float32)

    # Escalar o ruído pelo nível de ruído desejado e converter para int16
    scaled_noise = (noise * (2**15 - 1)).astype(np.int16)

    # Adicionar o ruído aos dados de áudio
    noisy_audio = audio_data + scaled_noise

    # Assegurar que os valores estão dentro dos limites do tipo int16
    noisy_audio = np.clip(noisy_audio, -2**15, 2**15 - 1)

    # Salvar o novo arquivo de áudio com ruído
    with wave.open(output_file, 'wb') as wav_out:
        wav_out.setparams(params)
        wav_out.writeframes(noisy_audio.tobytes())

def add_pink_noise(audio_file: str, output_file: str, noise_level: float) -> None:
    # Abrir o arquivo de áudio
    with wave.open(audio_file, 'rb') as wav_in:
        params = wav_in.getparams()  # Pegar os parâmetros do áudio
        frames = wav_in.readframes(params.nframes)  # Ler os frames de áudio
        audio_data = np.frombuffer(frames, dtype=np.int16)  # Converter para array numpy

    # Gerar ruído rosa
    noise = cn.powerlaw_psd_gaussian(1, audio_data.shape[0]).astype(np.float32)

    # Escalar o ruído pelo nível de ruído desejado e converter para int16
    scaled_noise = (noise * noise_level * (2**15 - 1)).astype(np.int16)

    # Adicionar o ruído aos dados de áudio
    noisy_audio = audio_data + scaled_noise

    # Assegurar que os valores estão dentro dos limites do tipo int16
    noisy_audio = np.clip(noisy_audio, -2**15, 2**15 - 1)

    # Salvar o novo arquivo de áudio com ruído
    with wave.open(output_file, 'wb') as wav_out:
        wav_out.setparams(params)
        wav_out.writeframes(noisy_audio.tobytes())

def add_brown_noise(audio_file: str, output_file: str, noise_level: float) -> None:
    # Abrir o arquivo de áudio
    with wave.open(audio_file, 'rb') as wav_in:
        params = wav_in.getparams()  # Pegar os parâmetros do áudio
        frames = wav_in.readframes(params.nframes)  # Ler os frames de áudio
        audio_data = np.frombuffer(frames, dtype=np.int16)  # Converter para array numpy

    # Gerar ruído marrom
    noise = cn.powerlaw_psd_gaussian(2, audio_data.shape[0]).astype(np.float32)

    # Escalar o ruído pelo nível de ruído desejado e converter para int16
    scaled_noise = (noise * noise_level * (2**15 - 1)).astype(np.int16)

    # Adicionar o ruído aos dados de áudio
    noisy_audio = audio_data + scaled_noise

    # Assegurar que os valores estão dentro dos limites do tipo int16
    noisy_audio = np.clip(noisy_audio, -2**15, 2**15 - 1)

    # Salvar o novo arquivo de áudio com ruído
    with wave.open(output_file, 'wb') as wav_out:
        wav_out.setparams(params)
        wav_out.writeframes(noisy_audio.tobytes())

def add_echo(audio_file: str, output_file: str, delay: int = 500, decay: float = 0.5) -> None:
    # Abrir o arquivo de áudio
    with wave.open(audio_file, 'rb') as wav_in:
        params = wav_in.getparams()  # Pegar os parâmetros do áudio
        frames = wav_in.readframes(params.nframes)  # Ler os frames de áudio
        audio_data = np.frombuffer(frames, dtype=np.int16)  # Converter para array numpy

    # Calcular o número de frames de atraso
    delay_frames = int(delay * params.framerate / 1000)

    # Criar um array de zeros para armazenar o áudio com eco
    echo_audio = np.zeros(audio_data.shape, dtype=np.int16)

    # Adicionar o áudio original ao áudio com eco
    echo_audio[:audio_data.shape[0]] = audio_data

    # Adicionar o eco ao áudio
    for i in range(delay_frames, audio_data.shape[0]):
        echo_audio[i] += int(decay * echo_audio[i - delay_frames])

    # Assegurar que os valores estão dentro dos limites do tipo int16
    echo_audio = np.clip(echo_audio, -2**15, 2**15 - 1)

    # Salvar o novo arquivo de áudio com eco
    with wave.open(output_file, 'wb') as wav_out:
        wav_out.setparams(params)
        wav_out.writeframes(echo_audio.tobytes())

def main():
    audio_file = 'sample.wav'

    add_noise(audio_file, "noisy_audio.wav", 0.2)
    add_white_noise(audio_file, "white_noisy_audio.wav", 0.2)
    add_pink_noise(audio_file, "pink_noisy_audio.wav", 0.2)
    add_brown_noise(audio_file, "brown_noisy_audio.wav", 0.2)
    add_echo(audio_file, "echo_audio.wav", 1000, 0.5)

if __name__ == '__main__':
    main()