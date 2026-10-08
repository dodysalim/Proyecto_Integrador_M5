![Credit Risk Monitor](docs/cover.svg)

# Credit Risk Monitor

**Preparación, evaluación y monitoreo de un modelo de pago a tiempo.**

HENRY · MÓDULO 5 · Python · scikit-learn · FastAPI · Streamlit

[Portafolio](https://dodysalim.github.io/) · [Caso y alcance](docs/PORTFOLIO_CASE.md) · [Verificación](docs/VALIDATION.md)

## La pregunta

¿Cómo evaluar una clasificación de crédito y detectar cambios en los datos sin confundir monitoreo con validación en producción?

## Qué puedes revisar

- Preprocesamiento y entrenamiento de clasificadores.
- API local de predicción y dashboard de monitoreo de distribuciones.
- KS, PSI, chi-cuadrado y divergencias; Power BI de cinco páginas.

## Inicio local

Usa Python 3.11 o 3.12 en un entorno independiente. Desde la raíz:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

Después de configurar los datos:

```bash
python -m streamlit run mlops_pipeline/src/app.py
# API local (requiere artefactos compatibles):
python -m uvicorn mlops_pipeline.src.model_deploy:app --host 127.0.0.1 --port 8080
```

## Datos y configuración

Base académica y componentes locales presentes. Se excluye puntaje por fuga de información. Pago_atiempo=1 significa paga a tiempo; no invertir la interpretación del riesgo.

## Power BI · PC y móvil

[Archivos e instrucciones](powerbi/README.md). Descarga el repositorio completo y abre `powerbi/Abrir-PowerBI.bat` en Windows; después pulsa **Actualizar**. Incluye A4 horizontal a tamaño real (100 %) y diseño móvil vertical. El archivo `.pbip` necesita sus carpetas Report, SemanticModel y data.

## Recorrido por el código

| Ruta | Qué contiene |
| --- | --- |
| [mlops_pipeline/src/](mlops_pipeline/src/) | Preparación, entrenamiento, API y monitoreo |
| [tests/](tests/) | Pruebas de lógica y API |
| [requirements.txt](requirements.txt) | Dependencias |

## Comprobación y alcance

14 pruebas existentes aprobadas. Dashboard de monitoreo abrió sin excepciones con la base disponible.

El conjunto Actual de Power BI es el holdout, no datos de producción. Las métricas de drift precalculadas no se recalculan al filtrar clientes. El modelo requiere validación adicional para un uso operativo.

Para repetir las pruebas desde la raíz:

```bash
python -m pytest tests -q
```

## Autoría

Proyecto académico Henry M5. Dody Salim Dueñas Remache.

[Documentación anterior](docs/ORIGINAL_README.md), conservada como referencia histórica.
