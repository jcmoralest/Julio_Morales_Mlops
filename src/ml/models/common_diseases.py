from .base_model import BaseHealthModel
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score
import numpy as np

class CommonDiseaseModel(BaseHealthModel):
    def __init__(self):
        super().__init__("common_disease_classifier")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        
        # Mapeo de síntomas a features
        self.symptom_mapping = {
            'fiebre': 0, 'dolor_cabeza': 1, 'fatiga': 2,
            'tos': 3, 'dolor_garganta': 4, 'dolor_muscular': 5,
            'nauseas': 6, 'vomito': 7, 'diarrea': 8,
            'dolor_abdominal': 9, 'perdida_apetito': 11
        }
        
        self.feature_names = list(self.symptom_mapping.keys())
        
        # Enfermedades comunes que puede diagnosticar
        self.disease_classes = [
            'SANO', 'GRIPE_COMUN', 'GASTROENTERITIS', 
            'INFECCION_RESPIRATORIA', 'ESTRES_FATIGA'
        ]
    
    def _symptoms_to_features(self, symptoms: Dict[str, int]) -> np.ndarray:
        """Convierte síntomas a vector de features"""
        features = np.zeros(len(self.symptom_mapping))
        for symptom, intensity in symptoms.items():
            if symptom in self.symptom_mapping:
                features[self.symptom_mapping[symptom]] = intensity
        return features.reshape(1, -1)
    
    def train(self, X_train, y_train):
        # Normalizar features
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Entrenar modelo
        self.model.fit(X_scaled, y_train)
        
        # Log en MLflow
        with mlflow.start_run():
            mlflow.log_param("model_type", "RandomForest")
            mlflow.log_param("n_estimators", 100)
            mlflow.sklearn.log_model(self.model, "model")
    
    def predict(self, symptoms: Dict[str, int]) -> Dict[str, Any]:
        if not self.model:
            raise ValueError("Modelo no entrenado")
            
        # Convertir síntomas a features
        features = self._symptoms_to_features(symptoms)
        features_scaled = self.scaler.transform(features)
        
        # Predicción
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Confidence score
        confidence = np.max(probabilities)
        
        # Feature importance para explicabilidad
        feature_importance = dict(zip(
            self.feature_names, 
            self.model.feature_importances_
        ))
        
        return {
            'prediction': self.disease_classes[prediction],
            'confidence': float(confidence),
            'probabilities': {
                disease: float(prob) 
                for disease, prob in zip(self.disease_classes, probabilities)
            },
            'feature_importance': feature_importance,
            'model_version': self.model_version
        }