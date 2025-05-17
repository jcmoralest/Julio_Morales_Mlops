# Diagnóstico Médico Simulado

# 🧠 Julio-MLOps  
**Predicción de enfermedades en pacientes**

---

## 📌 Problema

Dados los avances tecnológicos, en el campo de la medicina la cantidad de información que existe de los pacientes es muy abundante.  
Sin embargo, para algunas enfermedades no tan comunes, llamadas *huérfanas*, los datos que existen escasean.  

🔍 Se pretende construir un modelo que sea capaz de predecir, dados los datos de síntomas de un paciente, si es posible o no que este sufra de alguna enfermedad.  
Esto se requiere tanto para:

- Enfermedades **comunes** (con muchos datos disponibles)
- Enfermedades **huérfanas** (con pocos datos disponibles)

---

## 🎯 Propósito

Diseñar un **sistema de diagnóstico automatizado** que, a partir de los síntomas ingresados por un médico, pueda **clasificar el estado de salud** de un paciente en función del riesgo de enfermedad.

✅ El objetivo es apoyar la toma de decisiones clínicas tanto en el caso de enfermedades comunes como huérfanas.  
✅ Se utilizará una lógica interpretativa simulada (no ML real) para asegurar accesibilidad y comprensión.  
✅ El sistema debe ser fácilmente ejecutable localmente mediante tecnologías accesibles como **Docker**.

---

## Descripción
Este proyecto simula un modelo de diagnóstico médico. Dado un conjunto de síntomas (mínimo 3), retorna una clasificación simple:
- NO ENFERMO
- ENFERMEDAD LEVE
- ENFERMEDAD AGUDA
- ENFERMEDAD CRÓNICA

## Cómo usar

### 1. Construir la imagen Docker
```bash
docker build -t diagnostico-medico .
```

### 2. Ejecutar el contenedor
```bash
docker run -p 8000:8000 diagnostico-medico
```

### 3. Probar la API
```bash
curl -X POST http://localhost:8000/diagnostico \
  -H "Content-Type: application/json" \
  -d '{"sintomas": {"fiebre": 7, "dolor": 5, "tos": 4}}'
```

### Respuesta esperada
```json
{"diagnostico": "ENFERMEDAD AGUDA"}
```

### Enrriquisimiento del formulario
## Se agregaron mas preguntas al formulario, estas se pueden usar y validar a futuro ,
## una vez se mejore e implementen los modelos.



---

## 🗂️ Estructura del Proyecto

```bash
diagnostico-enfermedades/
├── app/
│   ├── main.py                 # Lógica principal de la API (FastAPI)
│   ├── diagnostico.py          # Función de clasificación simulada
│   ├── models.py               # Definición de esquemas (Pydantic)
│   └── templates/
│       └── index.html          # Interfaz web opcional (formulario médico)
│
├── tests/
│   └── test_diagnostico.py     # Pruebas unitarias para la lógica de diagnóstico
│
├── Dockerfile                  # Imagen Docker para ejecución local
├── requirements.txt            # Dependencias del proyecto (FastAPI, Uvicorn, etc.)
├── README.md                   # Instrucciones detalladas del proyecto
├── .gitignore                  # Archivos a ignorar por Git
└── docs/
    └── especificacion.md       # Propósito, alcance, supuestos y notas técnicas

```
---

## 🚀 Extras

CI/CD (.github/workflows/test.yml): Automatización de pruebas al hacer push/pull request.
