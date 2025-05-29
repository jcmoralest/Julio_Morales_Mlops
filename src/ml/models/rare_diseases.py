from .base_model import BaseHealthModel
import torch
import torch.nn as nn
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RareDiseaseModel(BaseHealthModel):
    def __init__(self):
        super().__init__("rare_disease_classifier")
        self.n_support = 5  # Pocos ejemplos por enfermedad
        self.prototype_net = None
        self.support_embeddings = {}
        self.rare_diseases = [
            'LUPUS_SISTEMICO', 'ESCLEROSIS_MULTIPLE', 
            'ENFERMEDAD_CROHN', 'SINDROME_SJOGREN'
        ]
        
    def _create_prototype_network(self, input_dim: int):
        """Red neuronal simple para embeddings"""
        class PrototypeNetwork(nn.Module):
            def __init__(self, input_dim, hidden_dim=64, embedding_dim=32):
                super().__init__()
                self.encoder = nn.Sequential(
                    nn.Linear(input_dim, hidden_dim),
                    nn.ReLU(),
                    nn.Dropout(0.3),
                    nn.Linear(hidden_dim, embedding_dim),
                    nn.ReLU()
                )
                
            def forward(self, x):
                return self.encoder(x)
        
        return PrototypeNetwork(input_dim)
    
    def train(self, support_set: Dict[str, List], query_set: Dict[str, List]):
        """
        Entrenamiento few-shot
        support_set: {disease: [symptoms_list]}
        query_set: {disease: [symptoms_list]}
        """
        input_dim = len(support_set[list(support_set.keys())[0]][0])
        self.prototype_net = self._create_prototype_network(input_dim)
        
        # Crear prototipos para cada enfermedad huérfana
        for disease, symptom_lists in support_set.items():
            symptom_array = np.array(symptom_lists)
            # Calcular centroide como prototipo
            prototype = np.mean(symptom_array, axis=0)
            self.support_embeddings[disease] = prototype
            
        print(f"Entrenado prototipos para {len(self.support_embeddings)} enfermedades huérfanas")
    
    def predict(self, symptoms: Dict[str, int]) -> Dict[str, Any]:
        if not self.support_embeddings:
            return {
                'prediction': 'UNKNOWN_RARE_DISEASE',
                'confidence': 0.0,
                'message': 'Modelo no entrenado para enfermedades huérfanas'
            }
        
        # Convertir síntomas a array
        symptom_vector = np.array(list(symptoms.values()))
        
        # Calcular similitud con cada prototipo
        similarities = {}
        for disease, prototype in self.support_embeddings.items():
            # Usar similitud coseno
            similarity = cosine_similarity(
                symptom_vector.reshape(1, -1), 
                prototype.reshape(1, -1)
            )[0][0]
            similarities[disease] = similarity
        
        # Mejor match
        best_disease = max(similarities, key=similarities.get)
        best_confidence = similarities[best_disease]
        
        # Threshold para detectar casos no conocidos
        if best_confidence < 0.3:
            return {
                'prediction': 'POSSIBLE_RARE_DISEASE',
                'confidence': float(best_confidence),
                'recommendation': 'Consultar especialista - patrón no reconocido',
                'similarities': similarities
            }
        
        return {
            'prediction': best_disease,
            'confidence': float(best_confidence),
            'similarities': similarities,
            'model_version': self.model_version
        }