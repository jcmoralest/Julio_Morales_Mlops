import os
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
from loguru import logger

# ------------------- CONFIGURACIONES -------------------
DATA_PATH = "../../data/dataset_enfermedades.csv"
MODEL_OUTPUT_PATH = "../../models/modelo_entrenado.pkl"
EXPERIMENT_NAME = "DiagnosticoMedicoML"
TARGET_COL = "diagnostico"

# ------------------- CARGA DE DATOS ---------------------
def cargar_datos():
    if not os.path.exists(DATA_PATH):
        logger.error(f"Archivo no encontrado: {DATA_PATH}")
        raise FileNotFoundError(f"{DATA_PATH} no existe.")
    df = pd.read_csv(DATA_PATH)
    return df

# ------------------- ENTRENAMIENTO ---------------------
def entrenar_modelo():
    logger.info("Iniciando entrenamiento de modelo...")

    df = cargar_datos()
    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)

    # Tracking en MLflow
    mlflow.set_experiment(EXPERIMENT_NAME)
    with mlflow.start_run():
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)

        # Log de parámetros y métricas
        mlflow.log_params({"n_estimators": 100, "modelo": "RandomForest"})
        mlflow.log_metric("accuracy", acc)
        mlflow.log_dict(report, "classification_report.json")

        # Registro del modelo
        mlflow.sklearn.log_model(modelo, artifact_path="model")

        # Guardar modelo local
        os.makedirs(os.path.dirname(MODEL_OUTPUT_PATH), exist_ok=True)
        joblib.dump(modelo, MODEL_OUTPUT_PATH)

        logger.success(f"Modelo entrenado y guardado en {MODEL_OUTPUT_PATH}")
        logger.info(f"Accuracy: {acc:.3f}")

if __name__ == "__main__":
    entrenar_modelo()
