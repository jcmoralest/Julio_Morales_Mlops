import time
from datetime import datetime, timedelta
from typing import Dict, List
import psutil
import numpy as np
from collections import defaultdict, deque
import json

class ModelMetrics:
    def __init__(self, max_history=1000):
        self.predictions_history = deque(maxlen=max_history)
        self.performance_metrics = defaultdict(list)
        self.drift_detector = DriftDetector()
        
    def log_prediction(self, prediction: str, confidence: float, 
                      processing_time_ms: float, model_used: str):
        """Log una predicción para métricas"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'prediction': prediction,
            'confidence': confidence,
            'processing_time_ms': processing_time_ms,
            'model_used': model_used
        }
        self.predictions_history.append(record)
        
        # Detectar drift
        self.drift_detector.add_prediction(prediction, confidence)
    
    def get_current_metrics(self) -> Dict:
        """Obtener métricas actuales"""
        if not self.predictions_history:
            return {"status": "no_data"}
        
        recent_predictions = list(self.predictions_history)[-100:]  # Últimas 100
        
        # Métricas de performance
        avg_confidence = np.mean([p['confidence'] for p in recent_predictions])
        avg_processing_time = np.mean([p['processing_time_ms'] for p in recent_predictions])
        
        # Distribución de predicciones
        prediction_counts = defaultdict(int)
        model_usage = defaultdict(int)
        
        for pred in recent_predictions:
            prediction_counts[pred['prediction']] += 1
            model_usage[pred['model_used']] += 1
        
        # System metrics
        system_metrics = {
            'cpu_usage': psutil.cpu_percent(),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent
        }
        
        return {
            'timestamp': datetime.now().isoformat(),
            'model_performance': {
                'avg_confidence': float(avg_confidence),
                'avg_processing_time_ms': float(avg_processing_time),
                'total_predictions': len(recent_predictions)
            },
            'prediction_distribution': dict(prediction_counts),
            'model_usage': dict(model_usage),
            'system_metrics': system_metrics,
            'drift_status': self.drift_detector.get_drift_status()
        }

class DriftDetector:
    def __init__(self, window_size=100, threshold=0.1):
        self.window_size = window_size
        self.threshold = threshold
        self.baseline_distribution = None
        self.current_window = deque(maxlen=window_size)
        
    def add_prediction(self, prediction: str, confidence: float):
        self.current_window.append({
            'prediction': prediction,
            'confidence': confidence,
            'timestamp': datetime.now()
        })
        
        # Establecer baseline si tenemos suficientes datos
        if len(self.current_window) == self.window_size and self.baseline_distribution is None:
            self._set_baseline()
    
    def _set_baseline(self):
        """Establecer distribución baseline"""
        predictions = [item['prediction'] for item in self.current_window]
        confidences = [item['confidence'] for item in self.current_window]
        
        self.baseline_distribution = {
            'prediction_dist': self._get_distribution(predictions),
            'confidence_mean': np.mean(confidences),
            'confidence_std': np.std(confidences)
        }
    
    def _get_distribution(self, items: List[str]) -> Dict[str, float]:
        """Calcular distribución de predicciones"""
        counts = defaultdict(int)
        for item in items:
            counts[item] += 1
        
        total = len(items)
        return {k: v/total for k, v in counts.items()}
    
    def get_drift_status(self) -> Dict:
        """Detectar drift en las predicciones"""
        if not self.baseline_distribution or len(self.current_window) < self.window_size:
            return {'status': 'insufficient_data'}
        
        # Distribución actual
        current_predictions = [item['prediction'] for item in self.current_window]
        current_confidences = [item['confidence'] for item in self.current_window]
        
        current_dist = self._get_distribution(current_predictions)
        current_conf_mean = np.mean(current_confidences)
        
        # Calcular divergencia KL simplificada
        kl_divergence = self._calculate_kl_divergence(
            self.baseline_distribution['prediction_dist'],
            current_dist
        )
        
        # Drift en confidence
        confidence_drift = abs(
            current_conf_mean - self.baseline_distribution['confidence_mean']
        )
        
        drift_detected = (
            kl_divergence > self.threshold or 
            confidence_drift > 0.1
        )
        
        return {
            'status': 'drift_detected' if drift_detected else 'stable',
            'kl_divergence': float(kl_divergence),
            'confidence_drift': float(confidence_drift),
            'timestamp': datetime.now().isoformat()
        }
    
    def _calculate_kl_divergence(self, p_dist: Dict, q_dist: Dict) -> float:
        """Calcular divergencia KL simplificada"""
        kl = 0.0
        all_keys = set(p_dist.keys()) | set(q_dist.keys())
        
        for key in all_keys:
            p = p_dist.get(key, 1e-8)
            q = q_dist.get(key, 1e-8)
            kl += p * np.log(p / q)
        
        return kl