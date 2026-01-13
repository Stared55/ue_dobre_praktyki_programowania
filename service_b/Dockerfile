# service_b/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalacja bibliotek systemowych
# ZMIANA: Używamy 'libgl1' zamiast 'libgl1-mesa-glx'
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Kopiowanie pliku z zależnościami
COPY requirements.txt .

# Instalacja zależności Python
RUN pip install --no-cache-dir -r requirements.txt

# Kopiowanie kodu źródłowego
COPY . .

# Domyślna komenda
CMD ["python", "worker.py"]