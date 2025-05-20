FROM python:3.10-slim

# Instalar librerías del sistema necesarias para OpenCV y RetinaFace
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar los archivos
COPY detector.py .
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto Flask
EXPOSE 5002

# Ejecutar la app
CMD ["python", "detector.py"]
