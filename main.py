# main.py
import asyncio
import json
import os
from pathlib import Path

from config import OUTPUT_DIR
from logger import logger
from schemas import VideoTask, PipelineResult

from image_engine import generate_medical_image
from video_ai_engine import generate_video_from_image
from voice_engine import generate_voice
from video_engine import assemble_final_video


def load_tasks(path: str = "tasks.json") -> list[VideoTask]:
    """Wczytuje zadania z pliku JSON i waliduje je przez Pydantic.

    Pydantic rzuci błąd z czytelną wiadomością jeśli jakieś pole jest niepoprawne
    - zamiast tajemniczego KeyError w połowie pipeline'u.
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [VideoTask(**item) for item in raw]


async def run_task(task: VideoTask) -> PipelineResult:
    """Wykonuje cały pipeline dla jednego zadania.

    Używamy asyncio.to_thread() ponieważ nasze funkcje (requests, file I/O)
    są synchroniczne i blokujące. to_thread() uruchamia je w osobnym wątku,
    nie blokując pętli zdarzeń - dzięki temu wiele zadań może działać równolegle.
    """
    logger.info(f"=== START zadania: {task.id} ===")

    # KROK 1: Zdjęcie bazowe (Gemini Imagen)
    image_path = await asyncio.to_thread(
        generate_medical_image, task.subject, task.id
    )
    if not image_path:
        return PipelineResult(task_id=task.id, success=False, error_message="Błąd generowania zdjęcia")

    # KROK 2: Animacja wideo (Google Veo)
    ai_video_path = await asyncio.to_thread(
        generate_video_from_image, image_path, task.action_prompt, task.id
    )
    if not ai_video_path:
        return PipelineResult(task_id=task.id, success=False, error_message="Błąd generowania wideo AI")

    # KROK 3: Głos lektora (ElevenLabs)
    audio_path = await asyncio.to_thread(
        generate_voice, task.body, task.id
    )
    if not audio_path:
        return PipelineResult(task_id=task.id, success=False, error_message="Błąd generowania głosu")

    # KROK 4: Montaż końcowy (MoviePy)
    try:
        final_output = await asyncio.to_thread(
            assemble_final_video, ai_video_path, audio_path, task.hook, task.id
        )
    except Exception as e:
        return PipelineResult(task_id=task.id, success=False, error_message=f"Błąd montażu: {e}")

    if final_output and os.path.exists(final_output):
        logger.info(f"SUKCES! Wideo gotowe: {final_output}")
        return PipelineResult(task_id=task.id, success=True, output_path=final_output)

    return PipelineResult(task_id=task.id, success=False, error_message="Plik końcowy nie powstał")


async def main():
    """Uruchamia pipeline dla wszystkich zadań równolegle (asyncio.gather).

    asyncio.gather() uruchamia wszystkie corouitny jednocześnie.
    Gdy jedno zadanie czeka na odpowiedź z API (np. Veo przez 3 minuty),
    inne mogą w tym czasie przetwarzać swoje kroki.
    """
    logger.info("--- Start: ContentFactory Medical ---")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    tasks = load_tasks()
    logger.info(f"Załadowano {len(tasks)} zadanie(a) z tasks.json")

    # Uruchamiamy wszystkie zadania równolegle
    results: list[PipelineResult] = await asyncio.gather(
        *[run_task(task) for task in tasks]
    )

    # Podsumowanie
    logger.info("--- Podsumowanie ---")
    for result in results:
        status = "OK" if result.success else "BŁĄD"
        detail = result.output_path or result.error_message
        logger.info(f"[{status}] {result.task_id}: {detail}")


if __name__ == "__main__":
    asyncio.run(main())
