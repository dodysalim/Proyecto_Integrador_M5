"""Rutas compartidas, independientes del directorio de ejecución."""
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = Path(os.environ.get("M5_MODEL_DIR", str(PROJECT_ROOT / "models"))).expanduser().resolve()
DATA_FILE = Path(os.environ.get("M5_DATA_FILE", str(PROJECT_ROOT / "Base_de_datos.xlsx"))).expanduser().resolve()
