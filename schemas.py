
from pydantic import BaseModel, Field


class VideoTask(BaseModel):
    """Schemat pojedynczego zadania produkcyjnego.

    Pydantic automatycznie:
    - waliduje typy przy tworzeniu obiektu
    - generuje czytelny .model_dump() / .model_json_schema()
    - daje autocomplete w IDE
    """
    id: str = Field(..., description="Unikalny identyfikator zadania, używany jako nazwa pliku")
    subject: str = Field(..., description="Prompt do generowania zdjęcia bazowego (Gemini Imagen)")
    action_prompt: str = Field(..., description="Prompt opisujący RUCH do animacji (Veo)")
    hook: str = Field(..., description="Tekst napisu wyświetlanego na wideo")
    body: str = Field(..., description="Tekst lektora (ElevenLabs TTS)")


class PipelineResult(BaseModel):
    """Wynik przetwarzania jednego zadania przez cały pipeline."""
    task_id: str
    success: bool
    output_path: str | None = None
    error_message: str | None = None
