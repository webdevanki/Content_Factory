# Używamy lekkiego obrazu Pythona
FROM python:3.10-slim

# Instalacja zależności systemowych wymaganych przez MoviePy
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    && rm -rf /var/lib/apt/lists/*

# Fix uprawnień ImageMagick na Linuksie (bardzo ważne: bez tego MoviePy nie wygeneruje napisów)
RUN sed -i 's/<policy domain="path" rights="none" pattern="@\*"//g' /etc/ImageMagick-6/policy.xml || true

# Ustawienie katalogu roboczego
WORKDIR /app

# Kopiowanie listy zależności i ich instalacja
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie całego kodu do kontenera
COPY . .

# Domyślna komenda odpalająca aplikację
CMD ["python", "main.py"]