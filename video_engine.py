# video_engine.py

# --- ŁATKA NAPRAWCZA PIL ---
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS
# ---------------------------

from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip, vfx
import os
from config import OUTPUT_DIR
from moviepy.config import change_settings
from logger import logger

# Ścieżka wymuszana tylko, gdy odpalamy skrypt lokalnie na Windowsie
if os.name == 'nt':
    change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"})

def assemble_final_video(ai_video_path, audio_path, hook_text, output_filename):
    logger.info(f"[KROK 4/4] Montaz koncowy (Skladanie calosci): {output_filename}...")
    
    # Sprawdzamy czy pliki istnieją
    if not os.path.exists(ai_video_path):
        raise Exception(f"Brak pliku wideo AI: {ai_video_path}")
        
    # 1. Audio
    voice_clip = AudioFileClip(audio_path)
    duration = voice_clip.duration + 1.0 # Całkowity czas trwania

    # 2. Wideo tła (z AI)
    bg_clip = VideoFileClip(ai_video_path)
    
    # Zapętlenie wideo (AI ma 5s, audio może mieć 10s)
    bg_clip = vfx.loop(bg_clip, duration=duration)
    
    # Skalowanie do pionu (HD) i centrowanie
    bg_clip = bg_clip.resize(height=1920)
    # Jeśli wideo jest szersze niż format 9:16, wycinamy środek
    if bg_clip.w > 1080:
        bg_clip = bg_clip.crop(x1=bg_clip.w/2 - 540, width=1080, height=1920)
    
    bg_clip = bg_clip.set_position('center')

    # 3. Winieta (Ciemniejszy dół)
    overlay = ColorClip(size=(1080, 1920), color=(0,0,0)).set_opacity(0.3).set_duration(duration)

    # 4. Napisy
    txt_clip = TextClip(
        hook_text.upper(),
        fontsize=65,
        color='white',
        font='Arial',
        kerning=3,
        method='caption',
        size=(950, None)
    ).set_position(('center', 1350)).set_duration(duration).fadein(0.5)

    # 5. Render
    final_video = CompositeVideoClip([bg_clip, overlay, txt_clip], size=(1080, 1920)).set_audio(voice_clip)
    
    output_path = os.path.join(OUTPUT_DIR, f"{output_filename}.mp4")
    
    final_video.write_videofile(
        output_path, 
        fps=30, 
        codec="libx264", 
        preset="medium",
        threads=4,
        logger=None
    )
    
    return output_path