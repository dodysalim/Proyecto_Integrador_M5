"""Composición del dashboard: une datos, análisis estadístico y secciones."""
import streamlit as st

import mlops_pipeline.src.model_monitoring as mm
from mlops_pipeline.src.dashboard import config
from mlops_pipeline.src.dashboard.data import MonitoringData
from mlops_pipeline.src.dashboard.drift import drifted_variables
from mlops_pipeline.src.dashboard.styles import CSS, HERO
from mlops_pipeline.src.dashboard.views.correlations import render_correlations
from mlops_pipeline.src.dashboard.views.details import render_details
from mlops_pipeline.src.dashboard.views.gallery import render_gallery
from mlops_pipeline.src.dashboard.views.health import render_health
from mlops_pipeline.src.dashboard.views.sidebar import render_sidebar


def run(load_data, monitor_cls=mm.ModelMonitor) -> None:
    """`load_data` devuelve (ref, curr, y_ref, y_curr); `monitor_cls` calcula las pruebas de drift."""
    st.set_page_config(**config.PAGE_CONFIG)
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(HERO, unsafe_allow_html=True)

    ref, curr, y_ref, y_curr = load_data()
    if ref is None:
        st.info("Iniciando sistema... Por favor espere mientras se cargan y procesan los datos.")
        return
    thresholds, data = render_sidebar(MonitoringData(ref, curr, y_ref, y_curr))
    with st.spinner('Realizando análisis estadístico...'):
        results = monitor_cls(data.reference, data.current).run_all_checks()
    drifted = drifted_variables(results, thresholds)

    render_health(results, drifted, data)
    render_details(results, thresholds, drifted, data)
    render_gallery(data)
    render_correlations(data)
