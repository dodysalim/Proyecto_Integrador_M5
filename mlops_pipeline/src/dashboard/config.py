"""Constantes del dashboard de monitoreo."""

PAGE_CONFIG = dict(page_title="Monitor de Modelos MLOps", page_icon="🤖", layout="wide",
                   initial_sidebar_state="expanded")

DATA_FILE = "Base_de_datos.xlsx"
DATA_SEARCH_PATHS = (DATA_FILE, f"../../{DATA_FILE}")
TARGET = "Pago_atiempo"
TEST_SIZE = 0.2          # mismo split que ft_engineering.py
RANDOM_STATE = 42
DROP_FOR_DRIFT = ("id_cliente", "fecha_prestamo")   # alta cardinalidad → falsos positivos
INCOME_TRENDS = ("Creciente", "Estable", "Decreciente")

# Umbrales por defecto (barra lateral)
P_VALUE_RANGE = (0.001, 0.10, 0.001)
PSI_RANGE = (0.1, 0.5, 0.2)
WARNING_SCORE = 0.1
CRITICAL_SCORE = 0.3
TARGET_DRIFT_LIMIT = 0.1

GALLERY_LIMIT = 24
GALLERY_COLUMNS = 4
SAMPLE_SIZE = 500
TOP_CATEGORIES = 15

# Paleta (coherente con el portafolio)
REF_COLOR = "#75E6CE"
CURR_COLOR = "#FF8A80"
DATASET_COLORS = {"Referencia": REF_COLOR, "Actual": CURR_COLOR, "Ref": REF_COLOR, "Act": CURR_COLOR}
STATUS_COLORS = {"ok": "#3FB68B", "warning": "#F8B84E", "critical": "#FF6B6B"}
TEXT = "#E6ECF5"
MUTED = "#93A1BD"
GRID = "rgba(147,161,189,0.15)"
SEQUENTIAL = ["#1B2A44", "#2E5E7E", "#3FA3A8", "#75E6CE"]
DIVERGING = ["#FF8A80", "#2A3550", "#75E6CE"]
QUALITATIVE = ["#75E6CE", "#88B7FF", "#C99BFF", "#F8D66D", "#FF8A80"]
