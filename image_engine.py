# image_engine.py
import replicate
import requests
import os
from config import MEDICAL_STYLE, TEMP_DIR
from logger import logger

def generate_medical_image(prompt_subject, filename):
    logger.info(f"[KROK 1/4] Generowanie ZDJECIA BAZOWEGO (Flux Pro): {prompt_subject}...")
    
    # Dodajemy "action shot" do prompta
    full_prompt = f"Action shot of {prompt_subject}, {MEDICAL_STYLE}"

    try:
        output = replicate.run(
            "black-forest-labs/flux-1.1-pro",
            input={
                "prompt": full_prompt,
                "aspect_ratio": "9:16",
                "output_format": "png",
                "output_quality": 100,
                "safety_tolerance": 2
            }
        )

        image_url = str(output)
        logger.info("Zdjecie gotowe. Pobieranie...")
        img_data = requests.get(image_url).content
        
        path = os.path.join(TEMP_DIR, f"{filename}.png")
        with open(path, 'wb') as handler:
            handler.write(img_data)
            
        return path
        
    except Exception as e:
        logger.error(f"Blad generowania obrazu: {e}")
        return None