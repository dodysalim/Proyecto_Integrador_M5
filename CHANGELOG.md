# Changelog

Todos los cambios relevantes de este proyecto se documentan aquí.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y [Versionado Semántico](https://semver.org/lang/es/).

## [2.0.0] - 2026-10-26

### 🔧 Mantenimiento

- **Arquitectura:** `app.py` (604 líneas) dividido en el paquete `mlops_pipeline/src/dashboard/` (`config`, `data`, `segments`, `drift`, `charts`, `views`). El comando `streamlit run mlops_pipeline/src/app.py` no cambia.
- **SOLID:** la lógica estadística (variables con drift, puntaje, estado de salud, tablas KS/PSI/Chi²) son funciones puras sin Streamlit; `run()` recibe el cargador de datos y la clase de monitoreo por inyección de dependencias; cada vista tiene una sola responsabilidad.
- **Corregido:** si faltaba `Base_de_datos.xlsx`, la carga devolvía 2 valores en lugar de 4 y el dashboard se caía; ahora muestra el aviso correspondiente.
- **Corregido:** el orden de las variables con drift era aleatorio (uso de `set`); ahora es estable.
- **Diseño moderno:** tema oscuro unificado con el portafolio, encabezado destacado, tarjetas de métricas, indicador de estado y gráficos con paleta común.
- 12 pruebas nuevas de la lógica del dashboard (26 en total).
- Verificación: con la base real, el dashboard modular muestra las mismas métricas, alertas y 28 gráficos que la versión anterior, sin excepciones.

## [1.1.0] - 2026-10-26

### 🔧 Mantenimiento

- **Corregido:** el dashboard de monitoreo fallaba al mostrar las tablas de drift con pandas moderno (`Styler.applymap` fue eliminado); ahora usa `Styler.map`. `pandas>=2.1` declarado en `requirements.txt`.
- Verificación: 14 pruebas aprobadas y las 3 pestañas del dashboard abren sin excepciones.
- Licencia MIT e insignias de CI y versión en el README.
