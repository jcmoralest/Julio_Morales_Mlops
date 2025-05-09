# Diagnóstico Médico Simulado

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