FROM python:3.11-slim

# Dependensi sistem untuk OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependensi Python terlebih dahulu (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin kode aplikasi
COPY . .

# Port default (Hugging Face Spaces = 7860; Render/Cloud Run override via $PORT)
ENV PORT=7860
EXPOSE 7860

# 1 worker karena TensorFlow berat; timeout 120s untuk cold start model
CMD gunicorn app:app --bind 0.0.0.0:${PORT} --workers 1 --timeout 120