from gtts import gTTS
from pydub import AudioSegment
from pydub.silence import detect_leading_silence

def generate_rest_wav():
    text = "rest"
    temp_mp3 = "temp_rest.mp3"
    output_wav = "rest.wav"

    # 1. Genera l'audio (lingua inglese per la pronuncia corretta)
    tts = gTTS(text=text, lang='en')
    tts.save(temp_mp3)

    # 2. Carica il file con pydub
    audio = AudioSegment.from_mp3(temp_mp3)

    # 3. Rimuovi il silenzio per renderlo istantaneo e sotto il secondo
    trim_leading = lambda x: x[detect_leading_silence(x):]
    trim_trailing = lambda x: trim_leading(x.reverse()).reverse()
    
    clean_audio = trim_trailing(trim_leading(audio))

    # Forza la durata se necessario (opzionale, ma utile per sicurezza)
    if len(clean_audio) > 1000:
        clean_audio = clean_audio[:1000]

    # 4. Esporta in WAV
    clean_audio.export(output_wav, format="wav")
    print(f"File '{output_wav}' generato con successo!")
    print(f"Durata effettiva: {len(clean_audio)} ms")

if __name__ == "__main__":
    generate_rest_wav()
