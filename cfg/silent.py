import wave
import struct

# Impostazioni
durata_secondi = 30
frequenza = 44100  # Hz
nome_file = "silenzio_30sec.wav"

# Calcolo del numero totale di frame
num_frames = durata_secondi * frequenza

# Creazione del file
with wave.open(nome_file, 'w') as wav_file:
    # (nchannels, sampwidth, framerate, nframes, comptype, compname)
    # 1 canale (mono), 2 byte (16 bit), 44100 Hz
    wav_file.setparams((1, 2, frequenza, num_frames, 'NONE', 'not compressed'))
    
    # Scrivi '0' per ogni frame (silenzio)
    # struct.pack('h', 0) crea un numero intero a 16 bit con valore 0
    valore_silenzio = struct.pack('h', 0)
    
    # Scrivi i dati
    for _ in range(num_frames):
        wav_file.writeframes(valore_silenzio)

print(f"File '{nome_file}' creato con successo!")
