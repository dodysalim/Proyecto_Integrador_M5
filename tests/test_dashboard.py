"""Pruebas de la lógica del dashboard de monitoreo (sin Streamlit)."""
import numpy as np
import pandas as pd
import pytest

from mlops_pipeline.src.dashboard.data import MonitoringData, build_monitoring_data, find_data_file
from mlops_pipeline.src.dashboard.drift import (DriftThresholds, categorical_summary, drift_score, drifted_variables,
                                                health_status, is_valid_category, numeric_summary, target_deviation)
from mlops_pipeline.src.dashboard.segments import SegmentSelection, apply_segments
from mlops_pipeline.src.dashboard.views.details import category_proportions

RESULTS = {
    'ks_test': {'edad': {'ks_statistic': 0.5, 'p_value': 0.0001}, 'salario': {'ks_statistic': 0.1, 'p_value': 0.4}},
    'psi_numeric': {'edad': 0.05, 'salario': 0.35},
    'chi_square': {'tipo': {'chi2_statistic': 3.2, 'p_value': 0.2}, 'mala': {'error': 'sin datos'}},
}
T = DriftThresholds(p_value=0.001, psi=0.2)


def test_drifted_variables_combines_tests_without_duplicates():
    assert drifted_variables(RESULTS, T) == ['edad', 'salario']


def test_score_and_health_status():
    assert drift_score(2, RESULTS) == pytest.approx(0.5)
    assert drift_score(0, {'ks_test': {}, 'chi_square': {}}) == 0
    assert health_status(0.05).level == 'ok'
    assert health_status(0.2).level == 'warning'
    assert health_status(0.5).label.startswith('Crítico')


def test_summaries_flag_drift():
    num = numeric_summary(RESULTS, T).set_index('Variable')
    assert num.loc['edad', 'Estado'] == '🔴 DRIFT' and num.loc['salario', 'Estado'] == '🔴 DRIFT'
    assert num.loc['edad', 'PSI'] == '0.050'
    cat = categorical_summary(RESULTS, T)
    assert list(cat['Variable']) == ['tipo'] and cat['Estado'].iloc[0] == '🟢 OK'


def test_target_deviation():
    assert target_deviation(pd.Series([1, 1, 0, 0]), pd.Series([1, 1, 1, 0])) == pytest.approx(0.25)


@pytest.mark.parametrize("value,ok", [("Empleado", True), ("nan", False), ("3.5", False), (12, False)])
def test_valid_category(value, ok):
    assert is_valid_category(value) is ok


@pytest.fixture
def data():
    ref = pd.DataFrame({'tipo_laboral': ['A', 'B', 'A', 'B'], 'edad_cliente': [20, 30, 40, 50],
                        'tendencia_ingresos': ['Estable', 'Creciente', 'Estable', 'Decreciente']})
    curr = ref.iloc[:2].copy()
    return MonitoringData(ref, curr, pd.Series([1, 0, 1, 0]), pd.Series([1, 0]))


def test_segments_keep_targets_aligned(data):
    out = apply_segments(data, SegmentSelection(job_types=['A'], age_range=(15, 35)))
    assert list(out.reference['edad_cliente']) == [20] and list(out.y_reference) == [1]
    assert len(out.current) == len(out.y_current) == 1
    trend = apply_segments(data, SegmentSelection(income_trends=['Estable']))
    assert len(trend.reference) == 2


def test_category_proportions_clean_and_label(data):
    df = category_proportions(data, 'tipo_laboral')
    assert set(df['Dataset']) == {'Referencia', 'Actual'}
    assert df.groupby('Dataset')['Proporción'].sum().round(6).eq(1).all()


def test_find_data_file():
    assert find_data_file(['a', 'b'], exists=lambda p: p == 'b') == 'b'
    assert find_data_file(['a'], exists=lambda p: False) is None


def test_build_monitoring_data_drops_ids_and_aligns_targets():
    n = 20
    df = pd.DataFrame({'id_cliente': range(n), 'fecha_prestamo': pd.date_range('2024-01-01', periods=n),
                       'edad_cliente': np.arange(n), 'Pago_atiempo': [0, 1] * 10})

    def fake_fe(frame):
        y = frame['Pago_atiempo']
        return None, None, y.iloc[:16], y.iloc[16:], None

    out = build_monitoring_data(df, fake_fe)
    assert 'id_cliente' not in out.reference.columns and 'fecha_prestamo' not in out.current.columns
    assert len(out.reference) == 16 and len(out.current) == 4
