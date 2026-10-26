"""Sección 2: tablas de drift y comparación visual por variable."""
import numpy as np
import pandas as pd
import streamlit as st

from mlops_pipeline.src.dashboard import charts, config
from mlops_pipeline.src.dashboard.drift import categorical_summary, is_valid_category, numeric_summary


def _highlight(df):
    return df.style.map(lambda x: 'color: #FF6B6B; font-weight: bold' if 'DRIFT' in str(x) else 'color: #3FB68B',
                        subset=['Estado'])


def _numeric_comparison(data, var):
    left, right = st.columns(2)
    with left:
        st.markdown("**Distribución Acumulada (ECDF)**")
        st.plotly_chart(charts.ecdf(data.reference[var], data.current[var]), use_container_width=True)
    with right:
        st.markdown("**Violin Plot (Densidad + Box)**")
        st.plotly_chart(charts.violin(data.reference[var], data.current[var]), use_container_width=True)

    st.markdown("**Interacción Multivariable (3D Scatter)**")
    nums = data.reference.select_dtypes(include=[np.number]).columns.tolist()
    if len(nums) > 2:
        var2 = nums[1] if nums[1] != var else nums[0]
        var3 = nums[2] if nums[2] != var else nums[0]
        idx = np.random.choice(len(data.reference), min(config.SAMPLE_SIZE, len(data.reference)), replace=False)
        sample = data.reference.iloc[idx].copy()
        sample['Color'] = data.y_reference.iloc[idx].astype(str).values
        st.plotly_chart(charts.scatter_3d(sample, var, var2, var3, 'Color',
                                          f"Interacción 3D: {var} vs {var2} vs {var3}"), use_container_width=True)


def category_proportions(data, var, top_n=config.TOP_CATEGORIES) -> pd.DataFrame:
    frames = []
    for df, name in ((data.reference, 'Referencia'), (data.current, 'Actual')):
        clean = df[df[var].apply(is_valid_category)]
        counts = clean[var].astype(str).value_counts(normalize=True).head(top_n).reset_index()
        counts.columns = [var, 'Proporción']
        counts['Dataset'] = name
        frames.append(counts)
    return pd.concat(frames)


def render_details(results, thresholds, drifted, data):
    st.markdown("---")
    st.header("2. Análisis Detallado")
    tab_num, tab_cat, tab_viz = st.tabs(["📊 Variables Numéricas", "📋 Variables Categóricas",
                                         "📈 Visualización Comparativa"])
    with tab_num:
        st.subheader("Métricas de Drift Numérico (KS & PSI)")
        st.dataframe(_highlight(numeric_summary(results, thresholds)), use_container_width=True)
    with tab_cat:
        st.subheader("Test de Chi-Cuadrado")
        if not results['chi_square']:
            st.info("No hay variables categóricas para analizar.")
        else:
            st.dataframe(_highlight(categorical_summary(results, thresholds)), use_container_width=True)
    with tab_viz:
        st.subheader("3.1. Comparación Visual Detallada")
        columns = data.reference.columns.tolist()
        default = columns.index(drifted[0]) if drifted and drifted[0] in columns else 0
        with st.columns([1, 2])[0]:
            var = st.selectbox("Seleccionar Variable Principal", columns, index=default)
        if var in data.reference.select_dtypes(include=[np.number]).columns:
            _numeric_comparison(data, var)
        else:
            st.markdown(f"**Distribución de Categorías: {var}**")
            st.plotly_chart(charts.category_proportions(category_proportions(data, var), var), use_container_width=True)
