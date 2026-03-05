# image_engine.py
import os
import base64
from google import genai
from google.genai import types
from config import MEDICAL_STYLE, TEMP_DIR, GOOGLE_CLOUD_API_KEY, versioned_path
from logger import logger

client = genai.Client(api_key=GOOGLE_CLOUD_API_KEY)

def generate_medical_image(prompt_subject: str, filename: str) -> str | None:
    logger.info(f"[KROK 1/4] Generowanie ZDJECIA BAZOWEGO (Gemini Imagen): {prompt_subject}...")

    full_prompt = f"Action shot of {prompt_subject}, {MEDICAL_STYLE}"

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="9:16",
                ),
            ),
        )

        image_data = response.parts[0].inline_data.data
        path = versioned_path(TEMP_DIR, filename, "png")
        with open(path, "wb") as f:
            f.write(image_data if isinstance(image_data, bytes) else base64.b64decode(image_data))

        logger.info("Zdjecie gotowe.")
        return path

    except Exception as e:
        logger.error(f"Blad generowania obrazu: {e}")
        return None
