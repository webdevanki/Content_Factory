# video_ai_engine.py
import replicate
import requests
import os
import time
from replicate.exceptions import ReplicateError
from config import TEMP_DIR

def generate_video_from_image(image_path, prompt_action, filename):
    print(f"🎥 [KROK 2/4] Ożywianie zdjęcia (Model: Minimax)...")
    print("⏳ To potrwa kilka minut. Minimax generuje bardzo płynny ruch.")

    # Otwieramy plik zdjęcia
    with open(image_path, "rb") as img_file:
        
        # PĘTLA RETRY (Odporność na błędy sieciowe/zajęte serwery)
        max_retries = 3
        for attempt in range(max_retries):
            try:
                print(f"   👉 Próba połączenia {attempt+1}/{max_retries}...")
                
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
                print(f"✅ SUKCES! Wideo wygenerowane. Pobieranie: {video_url}")
                
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
                    print(f"⚠️ Serwer zajęty (Tłok). Czekam {wait_time}s i próbuję ponownie...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ Błąd API Replicate: {e}")
                    # Jeśli to błąd 404 lub 422, nie ma sensu próbować ponownie tym samym kodem
                    if '404' in str(e) or '422' in str(e):
                        return None
            
            except Exception as e:
                print(f"❌ Nieoczekiwany błąd: {e}")
                return None

    print("❌ Nie udało się wygenerować wideo po 3 próbach.")
    return None