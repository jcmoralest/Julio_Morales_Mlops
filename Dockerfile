FROM python:3.11-bullseye

WORKDIR /app

# Copiar solo los archivos necesarios
COPY requirements.txt /app/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . /app

# Exponer el puerto
EXPOSE 8000

# Usar una variable de entorno para el puerto
ENV PORT=8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
