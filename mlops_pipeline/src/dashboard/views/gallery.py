"""Sección 4: galería compacta de todas las variables."""
import numpy as np
import pandas as pd
import streamlit as st

from mlops_pipeline.src.dashboard import charts, config
from mlops_pipeline.src.dashboard.charts import stacked

_NO_TOOLBAR = {'displayModeBar': False}


def _numeric_tile(data, var):
    n_ref, n_curr = min(config.SAMPLE_SIZE, len(data.reference)), min(config.SAMPLE_SIZE, len(data.current))
    df = stacked(data.reference[var].sample(n_ref), data.current[var].sample(n_curr), 'Val', 'Set', ('Ref', 'Act'))
    st.plotly_chart(charts.mini_histogram(df, var), use_container_width=True, config=_NO_TOOLBAR)


def _categorical_tile(data, var):
    st.caption(f"📊 {var} (Cat)")
    frames = []
    for df, name in ((data.reference, 'Ref'), (data.current, 'Act')):
        top = df[var].astype(str).value_counts(normalize=True).head(5)
        frames.append(pd.DataFrame({'Cat': top.index.astype(str), 'Prop': top.values, 'Set': name}))
    st.plotly_chart(charts.mini_categories(pd.concat(frames)), use_container_width=True, config=_NO_TOOLBAR)


def render_gallery(data):
    st.markdown("---")
    st.header("4. Galería de Variables (Vista Rápida)")
    st.markdown("Visualización compacta de todas las variables monitoreadas.")
    variables = data.reference.columns.tolist()[:config.GALLERY_LIMIT]
    numeric = set(data.reference.select_dtypes(include=[np.number]).columns)
    for start in range(0, len(variables), config.GALLERY_COLUMNS):
        row = variables[start:start + config.GALLERY_COLUMNS]
        for col, var in zip(st.columns(config.GALLERY_COLUMNS), row):
            with col:
                (_numeric_tile if var in numeric else _categorical_tile)(data, var)
