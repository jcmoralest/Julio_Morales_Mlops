import os
import json
from datetime import datetime
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict
from fastapi.responses import JSONResponse
from loguru import logger
from ..model.pipeline import run_diagnosis

# Actualizar rutas relativas para logs
LOG_DIR = "../../logs"
LOG_FILE = os.path.join(LOG_DIR, "predicciones.log")
os.makedirs(LOG_DIR, exist_ok=True)

app = FastAPI(title="Sistema de Diagnóstico Médico")

@app.post("/diagnostico")
async def diagnostico(request: Request):
    try:
        data = await request.json()
        logger.info(f"Datos recibidos: {data}")
        resultado = run_diagnosis(data)
        return JSONResponse(content={"diagnostico": resultado})
    except Exception as e:
        logger.exception("Error al procesar el diagnóstico")
        return JSONResponse(status_code=500, content={"error": "Error interno en el diagnóstico"})
