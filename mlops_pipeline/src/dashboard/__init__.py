"""Dashboard de monitoreo de drift, organizado por responsabilidades.

    config   → umbrales, colores y columnas (sin lógica)
    data     → carga y partición referencia/actual
    segments → filtros de segmentación (funciones puras)
    drift    → interpretación de resultados estadísticos (funciones puras)
    charts   → fábrica de gráficos con estilo unificado
    views    → secciones de Streamlit
"""
