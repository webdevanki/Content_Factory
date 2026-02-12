# image_engine.py
import replicate
import requests
import os
from config import MEDICAL_STYLE, TEMP_DIR

def generate_medical_image(prompt_subject, filename):
    print(f"📸 [KROK 1/4] Generowanie ZDJĘCIA BAZOWEGO (Flux Pro): {prompt_subject}...")
    
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
        print(f"✅ Zdjęcie gotowe. Pobieranie...")
        img_data = requests.get(image_url).content
        
        path = os.path.join(TEMP_DIR, f"{filename}.png")
        with open(path, 'wb') as handler:
            handler.write(img_data)
            
        return path
        
    except Exception as e:
        print(f"❌ Błąd generowania obrazu: {e}")
        return None