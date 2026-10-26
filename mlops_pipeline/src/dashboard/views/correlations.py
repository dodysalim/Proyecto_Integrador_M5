"""Sección 5: correlaciones con el objetivo y matrices de correlación."""
import numpy as np
import streamlit as st

from mlops_pipeline.src.dashboard import charts


def render_correlations(data):
    st.markdown("---")
    st.header("5. Análisis de Correlaciones")
    numeric = data.reference.select_dtypes(include=[np.number])
    if numeric.empty:
        st.info("No hay suficientes variables numéricas para correlación.")
        return
    try:
        corrs = numeric.assign(TARGET=data.y_reference.values).corr()['TARGET'].drop('TARGET').sort_values(ascending=False)
        st.subheader("Importancia de Variables (Correlación con Target)")
        st.plotly_chart(charts.importance(corrs), use_container_width=True)
    except (TypeError, ValueError):
        st.warning("No se pudo calcular correlación con target (tipo de dato incompatible).")

    left, right = st.columns(2)
    with left:
        st.subheader("Matriz Correlación (Referencia)")
        st.plotly_chart(charts.correlation_heatmap(numeric.corr()), use_container_width=True)
    with right:
        st.subheader("Matriz Correlación (Actual)")
        st.plotly_chart(charts.correlation_heatmap(data.current[numeric.columns].corr()), use_container_width=True)
