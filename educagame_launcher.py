import tkinter as tk
import subprocess
import webbrowser
import os
import time
import threading
import requests
import sys
import ctypes

CREATE_NO_WINDOW = 0x08000000

# BASE_DIR correto tanto no .py quanto no .exe
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def resource_path(relative_path):
    """Caminho correto tanto no .py quanto no .exe."""
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        return os.path.join(meipass, relative_path)
    return os.path.join(BASE_DIR, relative_path)

def _python():
    """Retorna o caminho do Python do venv, ou sys.executable como fallback."""
    venv_python = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        return venv_python
    return sys.executable

AZUL      = "#1F3F73"
LARANJA   = "#F28C28"
BRANCO    = "#FFFFFF"
AZUL_CLARO = "#2E5FA3"
VERDE     = "#27AE60"
VERMELHO  = "#E74C3C"

# ── Status da API ──────────────────────────────────────────────────────────────
_api_processo = None
_label_status = None

def _verificar_api():
    try:
        r = requests.get("http://127.0.0.1:8000/api/internal/health", timeout=2)
        return r.status_code == 200
    except Exception:
        return False

def _atualizar_status(online: bool):
    if _label_status:
        if online:
            _label_status.config(text="● API Online", fg=VERDE)
        else:
            _label_status.config(text="● API Offline", fg=VERMELHO)

def _monitorar_api():
    while True:
        _atualizar_status(_verificar_api())
        time.sleep(5)

def _iniciar_api_processo():
    global _api_processo
    api_path = os.path.join(BASE_DIR, "Fast_API")
    _api_processo = subprocess.Popen(
        [_python(), "-m", "uvicorn", "api.main:app",
         "--reload", "--reload-dir", api_path],
        cwd=api_path,
        creationflags=CREATE_NO_WINDOW
    )

def _aguardar_api():
    for _ in range(30):
        if _verificar_api():
            _atualizar_status(True)
            return
        time.sleep(1)
    _atualizar_status(False)

def _auto_iniciar():
    if not _verificar_api():
        _iniciar_api_processo()
    threading.Thread(target=_aguardar_api, daemon=True).start()

# ── Funções dos botões ─────────────────────────────────────────────────────────

def iniciar_api():
    if _verificar_api():
        webbrowser.open("http://localhost:8000/docs")
        return
    _iniciar_api_processo()
    threading.Thread(target=_aguardar_api, daemon=True).start()

def abrir_dashboard():
    script = os.path.join(BASE_DIR, "Fast_API", "dashboard", "streamlit.py")
    subprocess.Popen([_python(), "-m", "streamlit", "run", script],
                     creationflags=CREATE_NO_WINDOW)

def abrir_mosquito():
    caminho = os.path.join(BASE_DIR, "mata_mosquito", "index.html")
    url = "file:///" + caminho.replace(os.sep, "/")
    webbrowser.open(url)

def abrir_aventura():
    script = os.path.join(BASE_DIR, "aventura_letras", "main.py")
    subprocess.Popen([_python(), script],
                     creationflags=CREATE_NO_WINDOW)

def abrir_soletrando():
    script = os.path.join(BASE_DIR, "soletrando", "main.py")
    subprocess.Popen([_python(), script],
                     creationflags=CREATE_NO_WINDOW)

# ── Janela principal ───────────────────────────────────────────────────────────
myappid = 'educagames.launcher.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

janela = tk.Tk()
janela.title("EducaGames")

ico = resource_path("educagame.ico")

if os.path.exists(ico):
    janela.iconbitmap(default=ico)

logo_icon = tk.PhotoImage(file=resource_path("logo.png"))
janela.iconphoto(True, logo_icon)

largura_tela   = janela.winfo_screenwidth()
altura_tela    = janela.winfo_screenheight()
largura_janela = int(largura_tela * 0.40)
altura_janela  = int(altura_tela  * 0.78)
pos_x = int(largura_tela / 2 - largura_janela / 2)
pos_y = int(altura_tela  / 2 - altura_janela  / 2)

janela.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
janela.configure(bg=AZUL)

# ── Logo ───────────────────────────────────────────────────────────────────────
logo = tk.PhotoImage(file=resource_path("logo.png"))
logo = logo.subsample(5)
tk.Label(janela, image=logo, bg=AZUL).pack(pady=(6, 0))

# ── Título ─────────────────────────────────────────────────────────────────────
tk.Label(
    janela,
    text="Plataforma de Jogos Educativos",
    font=("Arial", 18, "bold"),
    bg=AZUL,
    fg=BRANCO
).pack(pady=(0, 2))

# ── Status da API ──────────────────────────────────────────────────────────────
_label_status = tk.Label(
    janela,
    text="● Iniciando API...",
    font=("Arial", 10, "bold"),
    bg=AZUL,
    fg=LARANJA
)
_label_status.pack(pady=(0, 2))

# ── Helpers ────────────────────────────────────────────────────────────────────
def criar_secao(texto):
    frame = tk.Frame(janela, bg=AZUL)
    frame.pack(fill="x", padx=60, pady=(10, 2))
    tk.Frame(frame, bg=LARANJA, height=2).pack(fill="x")
    tk.Label(
        frame,
        text=texto.upper(),
        font=("Arial", 10, "bold"),
        bg=AZUL,
        fg=LARANJA,
        anchor="w"
    ).pack(fill="x", pady=(3, 0))

def criar_botao(texto, comando):
    return tk.Button(
        janela,
        text=texto,
        command=comando,
        width=22,
        height=2,
        bg=LARANJA,
        fg=BRANCO,
        font=("Arial", 11, "bold"),
        relief="flat",
        activebackground=AZUL_CLARO,
        activeforeground=BRANCO,
        cursor="hand2"
    )

# ── Seção: API e Dashboard ─────────────────────────────────────────────────────
criar_secao("API e Dashboard")
criar_botao("Iniciar API",         iniciar_api).pack(pady=5)
criar_botao("Dashboard Professor", abrir_dashboard).pack(pady=5)

# ── Seção: Jogos ───────────────────────────────────────────────────────────────
criar_secao("Jogos")
criar_botao("Mata Mosquito",       abrir_mosquito).pack(pady=5)
criar_botao("Aventura das Letras", abrir_aventura).pack(pady=5)
criar_botao("Soletrando",          abrir_soletrando).pack(pady=5)

# ── Inicia API automaticamente ao abrir ───────────────────────────────────────
threading.Thread(target=_auto_iniciar, daemon=True).start()
threading.Thread(target=_monitorar_api, daemon=True).start()

janela.mainloop()