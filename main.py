# main.py
import os
from config import OUTPUT_DIR
from logger import logger

# IMPORTUJEMY WSZYSTKIE 4 SILNIKI
from image_engine import generate_medical_image 
from video_ai_engine import generate_video_from_image # <-- NOWOŚĆ
from voice_engine import generate_voice
# Zmieniliśmy nazwę funkcji w video_engine na bardziej pasującą
from video_engine import assemble_final_video 

tasks = [
    {
        "id": "Demo_PRP_Real_Motion",
        # Prompt 1: DLA ZDJĘCIA (Statyczny, opisuje co widzimy)
        "subject": "A close-up photograph of a aesthetic doctor's hands wearing light blue gloves, holding a mesotherapy gun focused on a patient's cheek skin. Clear PRP plasma is visible in the syringe. The skin has realistic texture, pores, and slight redness. Luxurious clinic background",
        
        # Prompt 2: DLA WIDEO (Dynamiczny, opisuje RUCH na zdjęciu)
        # To jest kluczowe - opisujemy co ma się zadziać.
        "action_prompt": "The doctor gently presses the mesotherapy gun against the skin, subtle micro-injection movement, the plasma liquid inside the syringe moves slightly. Slow, controlled, professional movement.",
        
        "hook": "Prawdziwe efekty.\nPrawdziwa nauka.",
        "body": "Zobacz, jak Twoje własne osocze rewitalizuje skórę. To precyzyjny, naturalny proces regeneracji. Bezpieczny i skuteczny."
    }
]

def main():
    logger.info("--- Start: ContentFactory Medical (REAL MOTION V1) ---")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for task in tasks:
        logger.info(f"=== Przetwarzanie zadania: {task['id']} ===")
        task_id = task['id']

        # 1. KROK: Obraz Bazowy (Flux)
        image_path = generate_medical_image(task['subject'], task_id)
        if not image_path: 
            logger.error("Przerwano: Blad generowania zdjecia.")
            continue

        # 2. KROK: Wideo AI na bazie zdjęcia (Kling)
        # To potrwa najdłużej (3-5 minut)
        ai_video_path = generate_video_from_image(image_path, task['action_prompt'], task_id)
        if not ai_video_path:
            logger.error("Przerwano: Blad generowania wideo AI.")
            continue

        # 3. KROK: Głos (ElevenLabs)
        audio_path = generate_voice(task['body'], task_id)
        if not audio_path:
            logger.error("Przerwano: Blad audio.")
            continue

        # 4. KROK: Montaż końcowy (MoviePy)
        try:
            # Używamy nowej funkcji montującej
            final_output = assemble_final_video(ai_video_path, audio_path, task['hook'], task_id)
            
            if final_output and os.path.exists(final_output):
                logger.info(f"SUKCES! Ostateczne wideo gotowe: {final_output}")
            else:
                logger.error("Blad: Plik koncowy nie powstal.")
                 
        except Exception as e:
            logger.error(f"Krytyczny blad montazu: {e}")

if __name__ == "__main__":
    main()