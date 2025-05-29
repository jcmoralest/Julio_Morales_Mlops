# src/monitoring/logging_config.py
import logging
import json
from datetime import datetime
from typing import Dict, Any

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        
    def log_prediction(self, event_type: str, data: Dict[str, Any]):
        """Log estructurado para predicciones"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'service': 'ml-diagnosis-api',
            'version': '2.0.0',
            'data': data
        }
        self.logger.info(json.dumps(log_entry))
    
    def log_error(self, error: Exception, context: Dict[str, Any]):
        """Log estructurado para errores"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': 'error',
            'service': 'ml-diagnosis-api',
            'error': {
                'type': type(error).__name__,
                'message': str(error),
                'context': context
            }
        }
        self.logger.error(json.dumps(log_entry))

def setup_logging():
    """Configurar logging estructurado"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )