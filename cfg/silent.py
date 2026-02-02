import wave
import struct

# Impostazioni
durata_secondi = 30
frequenza = 44100  # Hz
canali = 2         # Stereo
nome_file = "silenzio_30sec.wav"

# Calcolo del numero totale di frame
num_frames = durata_secondi * frequenza

# Creazione del file
with wave.open(nome_file, 'w') as wav_file:
    # Parametri: (nchannels, sampwidth, framerate, nframes, comptype, compname)
    # nchannels = 2 (stereo), sampwidth = 2 (16 bit)
    wav_file.setparams((canali, 2, frequenza, num_frames, 'NONE', 'not compressed'))
    
    # Per ogni frame in un file stereo a 16 bit, dobbiamo scrivere 4 byte:
    # 2 byte per il canale Sinistro + 2 byte per il canale Destro
    # struct.pack('hh', 0, 0) crea esattamente questi 4 byte di silenzio
    valore_silenzio_stereo = struct.pack('hh', 0, 0)
    
    print(f"Generazione di {durata_secondi} secondi di silenzio stereo...")
    
    # Scrivi i dati
    for _ in range(num_frames):
        wav_file.writeframes(valore_silenzio_stereo)

print(f"File '{nome_file}' creato con successo!")
