# Changelog

Todos los cambios relevantes de este proyecto se documentan aquí.
El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y [Versionado Semántico](https://semver.org/lang/es/).

## [1.1.0] - 2026-10-26

### 🔧 Mantenimiento

- **Corregido:** el dashboard de monitoreo fallaba al mostrar las tablas de drift con pandas moderno (`Styler.applymap` fue eliminado); ahora usa `Styler.map`. `pandas>=2.1` declarado en `requirements.txt`.
- Verificación: 14 pruebas aprobadas y las 3 pestañas del dashboard abren sin excepciones.
- Licencia MIT e insignias de CI y versión en el README.
