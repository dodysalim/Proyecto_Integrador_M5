"""Sección 1: estado de salud, drift del objetivo y alertas."""
import streamlit as st

from mlops_pipeline.src.dashboard import charts, config
from mlops_pipeline.src.dashboard.drift import drift_score, health_status, target_deviation


def render_health(results, drifted, data):
    st.header("1. Estado de Salud del Modelo")
    status = health_status(drift_score(len(drifted), results))
    col1, _, col3, col4 = st.columns(4)
    col1.metric("Variables Numéricas", len(results['ks_test']))
    col1.metric("Variables Categóricas", len(results['chi_square']))
    col3.metric("Variables con Drift", len(drifted), delta_color="inverse")
    color = config.STATUS_COLORS[status.level]
    col4.markdown(f"<div class='status-pill' style='border-color:{color}; color:{color}'>{status.label}</div>",
                  unsafe_allow_html=True)

    st.markdown("---")
    st.header("1.1 Análisis del Objetivo (Target Drift)")
    left, right = st.columns([1, 2])
    with left:
        st.info(f"Distribución de la Variable Objetivo: '{config.TARGET}'")
        diff = target_deviation(data.y_reference, data.y_current)
        st.metric("Máxima Desviación (Clases)", f"{diff:.2%}",
                  delta=f"{'⚠️ Drift' if diff > config.TARGET_DRIFT_LIMIT else 'Estable'}", delta_color="inverse")
    with right:
        st.plotly_chart(charts.target_distribution(data.y_reference, data.y_current), use_container_width=True)

    if drifted:
        st.error(f"⚠️ **Drift Detectado**: {', '.join(drifted)}")
        with st.expander("🔍 Ver Detalles y Recomendaciones", expanded=True):
            st.markdown(f"""
            **Diagnóstico:**
            - Se ha detectado un cambio significativo en la distribución de **{len(drifted)}** variables de entrada.
            - Esto puede indicar cambios en el comportamiento de los clientes o problemas en la recolección de datos.

            **Acciones Recomendadas:**
            1.  **Investigar Fuente**: Validar pipelines de datos e ingesta.
            2.  **Evaluar Impacto**: Verificar si el rendimiento del modelo (Accuracy/F1) ha decaído en el set actual.
            3.  **Reentrenar**: Si el drift es legítimo, incorporar los datos recientes al entrenamiento y generar la versión **v1.2.0**.
            """)
    else:
        st.success("✅ El modelo opera dentro de los parámetros estables.")
