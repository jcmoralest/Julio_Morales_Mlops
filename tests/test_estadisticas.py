import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Limpia el log antes de la prueba
log_path = os.path.join("logs", "predicciones.log")
if os.path.exists(log_path):
    os.remove(log_path)

from src.api.main import simular_prediccion, registrar_prediccion, leer_estadisticas

def test_prediccion_y_estadisticas():
    sintomas = {"fiebre": 3, "tos": 2, "dolor": 2}
    resultado = simular_prediccion(sintomas)
    registrar_prediccion(resultado, sintomas)
    estadisticas = leer_estadisticas()
    # Verifica que la última predicción registrada sea la esperada
    assert estadisticas["fecha_ultima_prediccion"] is not None
    assert estadisticas["ultimas_5_predicciones"][-1]["categoria"] == resultado

    sintomas = {"fiebre": 8, "tos": 8, "dolor": 7}
    resultado = simular_prediccion(sintomas)
    registrar_prediccion(resultado, sintomas)
    estadisticas = leer_estadisticas()
    # Verifica que la última predicción registrada sea la esperada
    assert estadisticas["fecha_ultima_prediccion"] is not None
    assert estadisticas["ultimas_5_predicciones"][-1]["categoria"] == resultado

    sintomas = {"fiebre": 5, "tos": 5, "dolor": 5}
    resultado = simular_prediccion(sintomas)
    registrar_prediccion(resultado, sintomas)
    estadisticas = leer_estadisticas()

    # Verifica que la última predicción registrada sea la esperada
    assert estadisticas["fecha_ultima_prediccion"] is not None
    assert estadisticas["ultimas_5_predicciones"][-1]["categoria"] == resultado