# Imagen base
FROM python:3.10-slim

# Evita prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Crear directorio de trabajo
WORKDIR /app

# Copiar requerimientos y archivos fuente
COPY requirements.txt .
COPY main.py .
COPY train_model.py .
COPY pipeline.py .
COPY config.yaml .
COPY index.html ./static/
COPY CHANGELOG.md .
COPY README.md .

# Instalar dependencias
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Exponer el puerto del servicio FastAPI
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
