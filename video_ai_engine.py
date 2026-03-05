# video_ai_engine.py
import os
import time
import base64
import io
import requests
from PIL import Image
from config import TEMP_DIR, GOOGLE_CLOUD_API_KEY, versioned_path
from logger import logger

BASE_URL = "https://generativelanguage.googleapis.com/v1beta"


def generate_video_from_image(image_path: str, prompt_action: str, filename: str) -> str | None:
    logger.info("[KROK 2/4] Ozywianie zdjecia (Model: Veo)...")
    logger.info("To potrwa kilka minut.")

    try:
        # Kompresja obrazu do JPEG max 1080x1920 (Veo ma limit rozmiaru)
        img = Image.open(image_path)
        img.thumbnail((1080, 1920), Image.LANCZOS)
        buffer = io.BytesIO()
        img.convert("RGB").save(buffer, format="JPEG", quality=85)
        image_b64 = base64.b64encode(buffer.getvalue()).decode()
        mime_type = "image/jpeg"
        logger.info(f"Rozmiar obrazu po kompresji: {len(buffer.getvalue()) // 1024} KB")

        params = {"key": GOOGLE_CLOUD_API_KEY}
        headers = {"Content-Type": "application/json"}

        payload = {
            "instances": [{
                "prompt": f"{prompt_action}, high quality, cinematic, slow motion, 4k",
                "image": {
                    "bytesBase64Encoded": image_b64,
                    "mimeType": mime_type
                }
            }],
            "parameters": {
                "aspectRatio": "9:16",
                "resolution": "1080p"
            }
        }

        resp = requests.post(
            f"{BASE_URL}/models/veo-3.1-generate-preview:predictLongRunning",
            json=payload,
            params=params,
            headers=headers,
        )
        if not resp.ok:
            logger.error(f"API error {resp.status_code}: {resp.text}")
            return None
        operation_name = resp.json()["name"]
        logger.info(f"Operacja uruchomiona: {operation_name}")

        # Polling na status operacji
        while True:
            op_resp = requests.get(
                f"{BASE_URL}/{operation_name}",
                params=params,
            )
            op_data = op_resp.json()
            if op_data.get("done"):
                break
            logger.info("Czekam na wideo...")
            time.sleep(15)

        # Pobieranie wideo
        samples = op_data["response"]["generateVideoResponse"]["generatedSamples"]
        video_uri = samples[0]["video"]["uri"]
        logger.info(f"SUKCES! Pobieranie wideo: {video_uri}")

        video_data = requests.get(video_uri, params=params).content
        video_path = versioned_path(TEMP_DIR, f"{filename}_raw_ai", "mp4")
        with open(video_path, "wb") as f:
            f.write(video_data)

        return video_path

    except Exception as e:
        logger.error(f"Blad generowania wideo: {e}")
        return None
