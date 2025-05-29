# src/api/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import logging
from datetime import datetime
import mlflow
import joblib

from src.ml.models.common_diseases import CommonDiseaseModel
from src.ml.models.rare_diseases import RareDiseaseModel
from src.monitoring.metrics import ModelMetrics
from src.monitoring.logging_config import setup_logging

# Setup
app = FastAPI(
    title="Sistema de Diagnóstico ML",
    description="API para predicción de enfermedades comunes y huérfanas",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Modelos globales
common_model = CommonDiseaseModel()
rare_model = RareDiseaseModel()
metrics_tracker = ModelMetrics()

# Pydantic models
class SymptomInput(BaseModel):
    patient_id: str = Field(..., description="ID único del paciente")
    symptoms: Dict[str, int] = Field(
        ..., 
        description="Síntomas con intensidad 1-5",
        example={
            "fiebre": 4,
            "dolor_cabeza": 3,
            "fatiga": 5
        }
    )
    patient_age: Optional[int] = Field(None, ge=0, le=120)
    medical_history: Optional[List[str]] = Field(None)

class DiagnosisResponse(BaseModel):
    patient_id: str
    primary_prediction: str
    confidence: float
    alternative_predictions: Dict[str, float]
    recommendations: List[str]
    model_used: str
    timestamp: datetime
    processing_time_ms: int

@app.on_event("startup")
async def startup_event():
    """Inicializar modelos al arrancar"""
    try:
        # Cargar modelos pre-entrenados si existen
        common_model.load_model("src/data/models")
        logger.info("Modelo de enfermedades comunes cargado")
    except:
        logger.warning("No se encontró modelo pre-entrenado para enfermedades comunes")
    
    try:
        rare_model.load_model("src/data/models")
        logger.info("Modelo de enfermedades huérfanas cargado")
    except:
        logger.warning("No se encontró modelo pre-entrenado para enfermedades huérfanas")

@app.post("/v2/diagnosis", response_model=DiagnosisResponse)
async def get_diagnosis(symptoms_data: SymptomInput):
    """Endpoint principal de diagnóstico con ML real"""
    start_time = datetime.now()
    
    try:
        # Validar síntomas
        if len(symptoms_data.symptoms) < 3:
            raise HTTPException(
                status_code=400, 
                detail="Se requieren al menos 3 síntomas"
            )
        
        # Determinar qué modelo usar basado en el patrón de síntomas
        symptom_score = sum(symptoms_data.symptoms.values())
        
        # Lógica de routing de modelos
        if symptom_score > 15 or len(symptoms_data.symptoms) > 8:
            # Patrón complejo -> probar modelo de enfermedades huérfanas
            rare_prediction = rare_model.predict(symptoms_data.symptoms)
            
            if rare_prediction['confidence'] > 0.5:
                model_used = "rare_disease_model"
                primary_prediction = rare_prediction['prediction']
                confidence = rare_prediction['confidence']
                alternatives = rare_prediction.get('similarities', {})
                recommendations = [
                    "Consultar especialista inmediatamente",
                    "Realizar pruebas específicas para enfermedad huérfana"
                ]
            else:
                # Fallback a modelo común
                common_prediction = common_model.predict(symptoms_data.symptoms)
                model_used = "common_disease_model"
                primary_prediction = common_prediction['prediction']
                confidence = common_prediction['confidence']
                alternatives = common_prediction['probabilities']
                recommendations = ["Seguimiento médico general"]
        else:
            # Patrón simple -> modelo de enfermedades comunes
            common_prediction = common_model.predict(symptoms_data.symptoms)
            model_used = "common_disease_model"
            primary_prediction = common_prediction['prediction']
            confidence = common_prediction['confidence']
            alternatives = common_prediction['probabilities']
            recommendations = ["Tratamiento sintomático", "Descanso y hidratación"]
        
        # Calcular tiempo de procesamiento
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Log para monitoreo
        metrics_tracker.log_prediction(
            prediction=primary_prediction,
            confidence=confidence,
            processing_time_ms=processing_time,
            model_used=model_used
        )
        
        # Respuesta
        response = DiagnosisResponse(
            patient_id=symptoms_data.patient_id,
            primary_prediction=primary_prediction,
            confidence=confidence,
            alternative_predictions=alternatives,
            recommendations=recommendations,
            model_used=model_used,
            timestamp=datetime.now(),
            processing_time_ms=int(processing_time)
        )
        
        logger.info(f"Diagnóstico completado para paciente {symptoms_data.patient_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error en diagnóstico: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "models_loaded": {
            "common_disease": common_model.model is not None,
            "rare_disease": len(rare_model.support_embeddings) > 0
        }
    }

@app.get("/metrics")
async def get_metrics():
    """Métricas del modelo para monitoreo"""
    return metrics_tracker.get_current_metrics()