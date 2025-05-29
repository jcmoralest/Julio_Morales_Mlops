from abc import ABC, abstractmethod
import joblib
import mlflow
from typing import Dict, List, Any
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class BaseHealthModel(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.model_version = "1.0.0"
        
    @abstractmethod
    def train(self, X_train, y_train):
        pass
    
    @abstractmethod
    def predict(self, symptoms: Dict[str, int]) -> Dict[str, Any]:
        pass
    
    def save_model(self, path: str):
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names,
            'version': self.model_version
        }
        joblib.dump(model_data, f"{path}/{self.model_name}.pkl")
        
    def load_model(self, path: str):
        model_data = joblib.load(f"{path}/{self.model_name}.pkl")
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data['feature_names']
        self.model_version = model_data['version']