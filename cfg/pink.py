import numpy as np
from scipy.io import wavfile

def pink_noise(duration_sec, sample_rate=44100):
    samples = duration_sec * sample_rate
    # Il rumore rosa è 1/f. Un metodo semplice è filtrare rumore bianco
    # Ma per brevità, usiamo una approssimazione efficace:
    white = np.random.randn(samples)
    # Filtro 1/f (semplificato)
    pink = np.cumsum(white) 
    # Normalizzazione per evitare clipping
    pink = pink / np.max(np.abs(pink)) * 0.7 
    return pink

# Configurazione
SAMPLE_RATE = 44100
DURATION = 30 # 60 secondi
FILENAME = "/home/paolo/pink_noise_clean.wav"

print(f"Generazione di {DURATION}s di rumore rosa...")

# Genera dati
audio_data = pink_noise(DURATION, SAMPLE_RATE)

# Converti in 16-bit PCM (formato standard per C++ libsndfile)
audio_data_int16 = (audio_data * 32767).astype(np.int16)

# Salva
wavfile.write(FILENAME, SAMPLE_RATE, audio_data_int16)
print(f"Salvato: {FILENAME}")
