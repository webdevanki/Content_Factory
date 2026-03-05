import requests
from config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, TEMP_DIR
import os
from logger import logger

def generate_voice(text, filename):
    logger.info("Generowanie glosu lektora (Turbo v2.5)...")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_turbo_v2_5", 
        "voice_settings": {
            "stability": 0.5, 
            "similarity_boost": 0.75
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code != 200:
        logger.error(f"BLAD ElevenLabs: {response.text}")
        return None

    path = os.path.join(TEMP_DIR, f"{filename}.mp3")
    
    with open(path, 'wb') as f:
        f.write(response.content)
    
    return path