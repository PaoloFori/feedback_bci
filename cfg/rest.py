from gtts import gTTS
from pydub import AudioSegment
from pydub.silence import detect_leading_silence

def generate_rest_wav():
    text = "rest"
    temp_mp3 = "temp_rest.mp3"
    output_wav = "783.wav" # Rinominato come richiesto

    # 1. Genera l'audio
    tts = gTTS(text=text, lang='en')
    tts.save(temp_mp3)

    # 2. Carica il file
    audio = AudioSegment.from_mp3(temp_mp3)

    # 3. Rimuovi il silenzio
    trim_leading = lambda x: x[detect_leading_silence(x):]
    trim_trailing = lambda x: trim_leading(x.reverse()).reverse()
    clean_audio = trim_trailing(trim_leading(audio))

    if len(clean_audio) > 1000:
        clean_audio = clean_audio[:1000]

    # --- MODIFICA QUI: Conversione Formato ---
    # Imposta i canali a 2 (Stereo) e il sample rate a 44100 Hz
    clean_audio = clean_audio.set_frame_rate(44100).set_channels(2)
    # -----------------------------------------

    # 4. Esporta in WAV (assicuriamoci che sia 16-bit PCM)
    clean_audio.export(output_wav, format="wav", parameters=["-acodec", "pcm_s16le"])
    
    print(f"File '{output_wav}' generato correttamente!")
    print(f"Proprietà: {clean_audio.frame_rate}Hz, {clean_audio.channels} canali, {len(clean_audio)}ms")

if __name__ == "__main__":
    generate_rest_wav()
