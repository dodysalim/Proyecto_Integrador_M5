"""Barra lateral: umbrales estadísticos y segmentadores."""
import streamlit as st

from mlops_pipeline.src.dashboard import config
from mlops_pipeline.src.dashboard.data import MonitoringData
from mlops_pipeline.src.dashboard.drift import DriftThresholds
from mlops_pipeline.src.dashboard.segments import SegmentSelection, apply_segments


def render_sidebar(data: MonitoringData):
    """Devuelve (umbrales, datos segmentados). Cada filtro se calcula sobre el anterior."""
    st.sidebar.title("⚙️ Configuración")
    st.sidebar.markdown("---")
    lo, hi, default = config.P_VALUE_RANGE
    p_value = st.sidebar.slider("Nivel de Confianza (p-value)", lo, hi, default, format="%.3f")
    lo, hi, default = config.PSI_RANGE
    psi = st.sidebar.slider("Umbral PSI (Alerta)", lo, hi, default)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔎 Segmentadores (Filtros)")
    ref = data.reference
    if 'tipo_laboral' in ref.columns:
        options = list(ref['tipo_laboral'].dropna().unique())
        chosen = st.sidebar.multiselect("Tipo Laboral", options=options, default=options)
        data = apply_segments(data, SegmentSelection(job_types=chosen))

    if 'edad_cliente' in data.reference.columns:
        both = (data.reference['edad_cliente'], data.current['edad_cliente'])
        lo, hi = int(min(s.min() for s in both)), int(max(s.max() for s in both))
        age = st.sidebar.slider("Rango de Edad", min_value=lo, max_value=hi, value=(lo, hi))
        data = apply_segments(data, SegmentSelection(age_range=age))

    if 'tendencia_ingresos' in data.reference.columns:
        trends = list(config.INCOME_TRENDS)
        chosen = st.sidebar.multiselect("Tendencia Ingresos", options=trends, default=trends)
        data = apply_segments(data, SegmentSelection(income_trends=chosen))

    st.sidebar.markdown("---")
    st.sidebar.info("Este dashboard compara los datos de entrenamiento (Referencia) con los datos más recientes "
                    "(Actual) para detectar degradación del modelo y realizar análisis multidimensional.")
    return DriftThresholds(p_value, psi), data
