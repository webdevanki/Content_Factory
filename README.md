# ContentFactory - Automated Multimodal AI Video Engine

## Opis projektu
ContentFactory to zaawansowany system do automatycznego generowania wysokiej jakości materiałów wideo, zaprojektowany z myślą o branży medycznej i estetycznej. System automatyzuje cały proces twórczy: od generowania fotorealistycznych obrazów, przez syntezę mowy, aż po finalny montaż wideo.

## Kluczowe cechy
- **SOTA Image Generation**: Implementacja modelu **Flux 1.1 Pro** via Replicate API, zapewniająca najwyższy stopień fotorealizmu (eliminacja efektu "sztuczności" typowego dla starszych modeli).
- **High-End Voice Synthesis**: Wykorzystanie **ElevenLabs** do generowania naturalnie brzmiących lektorów.
- **Automated Video Assembly**: Silnik oparty na **MoviePy**, który łączy ścieżki dźwiękowe, obrazy i podkład muzyczny w gotowy plik MP4.
- **Modular Architecture**: Odseparowane silniki (`image_engine`, `voice_engine`, `video_engine`) pozwalają na szybką wymianę dostawców modeli AI.

## Tech Stack
- **Language**: Python 3.10+
- **AI Models**: Flux 1.1 Pro (Image), ElevenLabs (Voice)
- **APIs**: Replicate, ElevenLabs
- **Libraries**: MoviePy, Pandas, PIL

## Instalacja i Bezpieczeństwo
1. Sklonuj repozytorium.
2. Skonfiguruj plik `.env` (klucze API dla Replicate i ElevenLabs). **Nigdy nie udostępniaj tego pliku publicznie!**
3. Zainstaluj zależności: `pip install -r requirements.txt`.

*Projekt rozwijany z myślą o skalowalnej produkcji treści marketingowych "premium".*
