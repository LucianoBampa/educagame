import pyttsx3
import queue
import threading

engine = pyttsx3.init()

# ✅ CONFIGURAÇÕES DE VOZ (COLOQUE AQUI)
engine.setProperty('rate', 150)     # velocidade
engine.setProperty('volume', 1.0)   # volume (0.0 a 1.0)

# Escolher voz
voices = list(engine.getProperty('voices'))
if len(voices) > 0:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('voice', voices[0].id)  # teste 0 ou 1

# Fila de fala
fila_fala = queue.Queue()

def worker_fala():
    while True:
        texto = fila_fala.get()
        if texto is None:
            break
        engine.say(texto)
        engine.runAndWait()
        fila_fala.task_done()

threading.Thread(target=worker_fala, daemon=True).start()

def falar(texto):
    fila_fala.put(texto)