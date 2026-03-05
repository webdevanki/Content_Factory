# video_ai_engine.py
import replicate
import requests
import os
import time
from replicate.exceptions import ReplicateError
from config import TEMP_DIR
from logger import logger

def generate_video_from_image(image_path, prompt_action, filename):
    logger.info("[KROK 2/4] Ozywianie zdjecia (Model: Minimax)...")
    logger.info("To potrwa kilka minut. Minimax generuje bardzo plynny ruch.")

    # Otwieramy plik zdjęcia
    with open(image_path, "rb") as img_file:
        
        # PĘTLA RETRY (Odporność na błędy sieciowe/zajęte serwery)
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"Proba polaczenia {attempt+1}/{max_retries}...")
                
                # ZMIANA: Używamy Minimax (jest bardziej stabilny publicznie niż Kling)
                output = replicate.run(
                    "minimax/video-01",
                    input={
                        "first_frame_image": img_file, # Minimax wymaga tej nazwy parametru
                        "prompt": f"{prompt_action}, high quality, cinematic, slow motion, 4k",
                        "prompt_optimizer": True,      # AI ulepszy Twój prompt
                        "loop": False
                    }
                )
                
                # Minimax zwraca URL bezpośrednio
                video_url = str(output)
                logger.info(f"SUKCES! Wideo wygenerowane. Pobieranie: {video_url}")
                
                video_data = requests.get(video_url).content
                
                # Zapisujemy
                video_path = os.path.join(TEMP_DIR, f"{filename}_raw_ai.mp4")
                with open(video_path, 'wb') as handler:
                    handler.write(video_data)
                    
                return video_path

            except ReplicateError as e:
                # Obsługa błędu Rate Limit (429) - czekamy dłużej
                if '429' in str(e) or 'throttled' in str(e.detail):
                    wait_time = 30 # Zwiększyliśmy czas oczekiwania do 30s
                    logger.warning(f"Serwer zajety (Tlok). Czekam {wait_time}s i probuje ponownie...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Blad API Replicate: {e}")
                    # Jeśli to błąd 404 lub 422, nie ma sensu próbować ponownie tym samym kodem
                    if '404' in str(e) or '422' in str(e):
                        return None
            
            except Exception as e:
                logger.error(f"Nieoczekiwany blad: {e}")
                return None

    logger.error("Nie udalo sie wygenerowac wideo po 3 probach.")
    return None