import yaml
import joblib
import shap
import pandas as pd
from loguru import logger
from sklearn.preprocessing import StandardScaler
import os

# Cargar configuraciones
CONFIG_PATH = "../../config.yaml"
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

# Cargar modelo - Actualizar ruta relativa
MODEL_PATH = config["model"]["path"]
if not os.path.isabs(MODEL_PATH):
    MODEL_PATH = os.path.join(os.path.dirname(__file__), "../..", MODEL_PATH)
MODEL = joblib.load(MODEL_PATH)

# Preprocesamiento simple
def preprocess(data: dict) -> pd.DataFrame:
    df = pd.DataFrame([data])
    numeric_cols = df.select_dtypes(include=['number']).columns
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df

# Diagnóstico con ML
def run_diagnosis(raw_input: dict) -> str:
    try:
        processed_input = preprocess(raw_input)
        prediction = MODEL.predict(processed_input)[0]
        explanation = explain_prediction(processed_input)
        logger.info(f"Predicción: {prediction}, Explicación: {explanation}")
        return prediction
    except Exception as e:
        logger.exception("Error en el pipeline de predicción")
        return "Error en el procesamiento"

# Explicabilidad
def explain_prediction(input_df):
    explainer = shap.Explainer(MODEL)
    shap_values = explainer(input_df)
    return shap_values[0].values.tolist()
