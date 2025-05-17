import os
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from fastapi.responses import JSONResponse

app = FastAPI()
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "predicciones.log")
os.makedirs(LOG_DIR, exist_ok=True)

def diagnostico_sintomas(sintomas):
    if not isinstance(sintomas, dict) or len(sintomas) < 3:
        return "Error: se requieren al menos 3 síntomas como diccionario."

    puntuacion_total = sum(sintomas.values())

    if puntuacion_total < 5:
        return "NO ENFERMO"
    elif puntuacion_total < 15:
        return "ENFERMEDAD LEVE"
    elif puntuacion_total < 25:
        return "ENFERMEDAD AGUDA"
    else:
        return "ENFERMEDAD CRÓNICA"

def simular_prediccion(sintomas: dict) -> str:
    score = sum(sintomas.values())
    if score < 5:
        return "SANO"
    elif score < 10:
        return "ENFERMEDAD LEVE"
    elif score < 15:
        return "ENFERMEDAD MODERADA"
    elif score < 20:
        return "ENFERMEDAD GRAVE"
    else:
        return "ENFERMEDAD TERMINAL"

class SintomasInput(BaseModel):
    sintomas: Dict[str, int]

def registrar_prediccion(categoria: str):
    fecha = datetime.now().isoformat()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{fecha},{categoria}\n")

def leer_estadisticas():
    if not os.path.exists(LOG_FILE):
        return {
            "conteo_por_categoria": {},
            "ultimas_5_predicciones": [],
            "fecha_ultima_prediccion": None
        }
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lineas = [line.strip() for line in f if line.strip()]
    conteo = {}
    predicciones = []
    for linea in lineas:
        fecha, categoria = linea.split(",", 1)
        conteo[categoria] = conteo.get(categoria, 0) + 1
        predicciones.append({"fecha": fecha, "categoria": categoria})
    ultimas_5 = predicciones[-5:] if len(predicciones) >= 5 else predicciones
    fecha_ultima = predicciones[-1]["fecha"] if predicciones else None
    return {
        "conteo_por_categoria": conteo,
        "ultimas_5_predicciones": ultimas_5,
        "fecha_ultima_prediccion": fecha_ultima
    }

@app.post("/diagnostico")
async def obtener_diagnostico(datos: SintomasInput):
    resultado = diagnostico_sintomas(datos.sintomas)
    registrar_prediccion(resultado)
    return JSONResponse(content={"diagnostico": resultado})

@app.get("/reporte")
async def obtener_reporte():
    estadisticas = leer_estadisticas()
    return JSONResponse(content=estadisticas)