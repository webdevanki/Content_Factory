import os
from dotenv import load_dotenv

# Wczytuje zmienne z pliku .env (jeśli istnieje)
load_dotenv()

# --- KLUCZE API ---
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if REPLICATE_API_TOKEN:
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN 

# --- STYL (PROMPT) ---
MEDICAL_STYLE = os.getenv(
    "MEDICAL_STYLE", 
    "documentary medical photography, macro shot focusing on action, "
    "shallow depth of field, natural clinic lighting, "
    "hyper-realistic skin texture, visible pores, authentic medical setting, 8k"
) 

# --- ŚCIEŻKI I FOLDERY ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pobieramy nazwę folderu z .env (lub domyślnie używamy "assets", "output", "temp"), 
# a następnie łączymy to z głównym katalogiem projektu (BASE_DIR)
ASSETS_DIR = os.path.join(BASE_DIR, os.getenv("ASSETS_DIR", "assets"))
OUTPUT_DIR = os.path.join(BASE_DIR, os.getenv("OUTPUT_DIR", "output"))
TEMP_DIR = os.path.join(BASE_DIR, os.getenv("TEMP_DIR", "temp"))

# Upewnij się, że foldery istnieją
for d in [ASSETS_DIR, OUTPUT_DIR, TEMP_DIR]:
    os.makedirs(d, exist_ok=True)