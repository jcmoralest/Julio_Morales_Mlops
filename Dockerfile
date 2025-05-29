# Imagen base
FROM python:3.11-slim

# Evita prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Crear directorio de trabajo
WORKDIR /app

# Copiar solo los archivos necesarios primero
COPY requirements.txt .
COPY setup.py .
COPY src/ src/
COPY logs/ logs/
COPY config.yaml .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

# Crear directorio para logs si no existe
RUN mkdir -p logs

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
