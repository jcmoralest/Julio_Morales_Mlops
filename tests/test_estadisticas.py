from main import simular_prediccion, registrar_prediccion, leer_estadisticas

def test_prediccion_y_estadisticas():
    sintomas = {"fiebre": 8, "tos": 8, "dolor": 8}
    resultado = simular_prediccion(sintomas)
    registrar_prediccion(resultado)
    estadisticas = leer_estadisticas()
    # Verifica que la última predicción registrada sea la esperada
    assert estadisticas["fecha_ultima_prediccion"] is not None
    assert estadisticas["ultimas_5_predicciones"][-1]["categoria"] == resultado