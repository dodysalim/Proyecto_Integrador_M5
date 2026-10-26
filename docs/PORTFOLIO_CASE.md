# Riesgo crediticio · Pipeline de ML

## Qué resuelve

Proyecto académico Henry M5 de preparación de datos, entrenamiento y servicio de predicciones.

## Evidencia para un reclutador

Archivos y carpetas revisados: `mlops_pipeline/src, run_api_test.py, requirements.txt`. El contenido descargado para la revisión incluyó 11 archivos Python y 3 notebooks. Se comprobó la sintaxis de los archivos Python; esto no sustituye ejecutar el pipeline ni entrenar sus modelos.

## Reproducibilidad

Clona el repositorio completo: esta carpeta de mejoras contiene solamente los archivos que cambian. Conserva los datasets, recursos y documentación del repositorio original. Usa su configuración de dependencias y aporta las variables de entorno y artefactos que requiera cada etapa.

## Contexto y atribución

Antes de servir predicciones se necesitan el modelo y el preprocesador generados con los datos originales. No usar para decisiones crediticias reales sin validación adicional.

## Cómo evaluar el proyecto

1. Verifica que las fuentes y el significado de las columnas estén documentados.
2. Repite el procesamiento con los datos originales y conserva el log de ejecución.
3. Para modelos, revisa el corte de entrenamiento y prueba y posibles fugas de información.
4. Compara indicadores del dashboard con consultas o agregados de la fuente.
5. Documenta resultados medidos, fecha de ejecución y límites de interpretación.

Revisión de presentación y código: 7 de octubre de 2026. No se atribuye empleo profesional a un proyecto de formación.
