from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from fastapi.responses import JSONResponse

app = FastAPI()

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

class SintomasInput(BaseModel):
    sintomas: Dict[str, int]

@app.post("/diagnostico")
async def obtener_diagnostico(datos: SintomasInput):
    resultado = diagnostico_sintomas(datos.sintomas)
    return JSONResponse(content={"diagnostico": resultado})