# Riesgo crediticio · Power BI

Datos agregados del Excel académico original; pago a tiempo observado en el dataset, no una predicción nueva. La moneda no se infiere.

Datos: 17 filas en la exportación. El CSV omite nombres, teléfonos y correos.

Abra `Analytics.pbip` en Power BI Desktop y cambie el parámetro `DataFolder` a la ruta absoluta de `powerbi/data/` (con separador final). Luego actualice los datos. Alternativamente ejecute `python configure_data.py` para configurar la ruta.

Incluye modelo TMDL, Power Query, medidas DAX explícitas, tarjetas y tabla de detalle. Los archivos JSON y las referencias se verificaron por código; apertura, actualización y renderizado en Power BI Desktop pendientes. No se afirma equivalencia funcional completa con la aplicación Python.

La exportación se reconstruye con `build_powerbi.py` durante la preparación del portafolio. La fuente original permanece en este repositorio.
