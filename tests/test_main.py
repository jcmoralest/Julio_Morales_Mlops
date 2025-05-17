import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from main import simular_prediccion

def test_categoria_sano():
    sintomas = {"fiebre": 1, "tos": 1, "dolor": 1}  # suma = 3
    assert simular_prediccion(sintomas) == "SANO"

def test_categoria_leve():
    sintomas = {"fiebre": 3, "tos": 3, "dolor": 3}  # suma = 9
    assert simular_prediccion(sintomas) == "ENFERMEDAD LEVE"

def test_categoria_moderada():
    sintomas = {"fiebre": 5, "tos": 5, "dolor": 4}  # suma = 14
    assert simular_prediccion(sintomas) == "ENFERMEDAD MODERADA"

def test_categoria_grave():
    sintomas = {"fiebre": 7, "tos": 7, "dolor": 6}  # suma = 20
    assert simular_prediccion(sintomas) == "ENFERMEDAD GRAVE"

def test_categoria_terminal():
    sintomas = {"fiebre": 10, "tos": 10, "dolor": 10}  # suma = 30
    assert simular_prediccion(sintomas) == "ENFERMEDAD TERMINAL"