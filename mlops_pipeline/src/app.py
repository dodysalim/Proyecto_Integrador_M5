"""Monitor de modelos MLOps · punto de entrada de Streamlit.

    streamlit run mlops_pipeline/src/app.py

La interfaz vive en el paquete `mlops_pipeline/src/dashboard/`.
"""
import sys
from pathlib import Path

# app.py está en mlops_pipeline/src/: la raíz del proyecto está dos niveles arriba (Streamlit Cloud)
root_path = str(Path(__file__).resolve().parents[2])
if root_path not in sys.path:
    sys.path.append(root_path)

import streamlit as st  # noqa: E402

import mlops_pipeline.src.ft_engineering as fte  # noqa: E402
from mlops_pipeline.src.dashboard.app import run  # noqa: E402
from mlops_pipeline.src.dashboard.data import build_monitoring_data, find_data_file  # noqa: E402

# Expuestos para pruebas
_fte = fte
_cargar_datos = fte.cargar_datos


@st.cache_data
def load_and_process_data():
    """Carga la base, separa referencia/actual y devuelve (ref, curr, y_ref, y_curr)."""
    try:
        path = find_data_file()
        if path is None:
            st.error("No se encontró el archivo de base de datos.")
            return None, None, None, None
        data = build_monitoring_data(_cargar_datos(path), _fte.feature_engineering)
        return data.reference, data.current, data.y_reference, data.y_current
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None, None, None, None


if __name__ == "__main__":
    run(load_and_process_data)
