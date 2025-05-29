from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from loguru import logger
from pipeline import run_diagnosis

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
