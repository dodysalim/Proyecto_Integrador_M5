"""Interpretación de los resultados de `ModelMonitor` (sin Streamlit)."""
from dataclasses import dataclass
from typing import Dict, List

import pandas as pd

from mlops_pipeline.src.dashboard import config


@dataclass(frozen=True)
class DriftThresholds:
    p_value: float
    psi: float


@dataclass(frozen=True)
class HealthStatus:
    level: str   # ok | warning | critical
    label: str


def drifted_variables(results: Dict, t: DriftThresholds) -> List[str]:
    ks, psi, chi = results['ks_test'], results['psi_numeric'], results['chi_square']
    found = [v for v, r in ks.items() if r['p_value'] < t.p_value]
    found += [v for v, value in psi.items() if value > t.psi]
    found += [v for v, r in chi.items() if r.get('p_value', 1) < t.p_value]
    return list(dict.fromkeys(found))   # sin duplicados, orden estable


def drift_score(n_drifted: int, results: Dict) -> float:
    total = len(results['ks_test']) + len(results['chi_square'])
    return n_drifted / total if total else 0.0


def health_status(score: float) -> HealthStatus:
    if score > config.CRITICAL_SCORE:
        return HealthStatus('critical', 'Crítico 🔴')
    if score > config.WARNING_SCORE:
        return HealthStatus('warning', 'Advertencia 🟡')
    return HealthStatus('ok', 'Saludable 🟢')


def _status(is_drift: bool) -> str:
    return "🔴 DRIFT" if is_drift else "🟢 OK"


def numeric_summary(results: Dict, t: DriftThresholds) -> pd.DataFrame:
    rows = []
    for var, ks in results['ks_test'].items():
        psi = results['psi_numeric'].get(var, 0)
        rows.append({"Variable": var, "KS Statistic": f"{ks['ks_statistic']:.3f}",
                     "P-Value": f"{ks['p_value']:.4e}", "PSI": f"{psi:.3f}",
                     "Estado": _status(ks['p_value'] < t.p_value or psi > t.psi)})
    return pd.DataFrame(rows)


def categorical_summary(results: Dict, t: DriftThresholds) -> pd.DataFrame:
    rows = [{"Variable": var, "Chi2 Stat": f"{r['chi2_statistic']:.3f}", "P-Value": f"{r['p_value']:.4e}",
             "Estado": _status(r['p_value'] < t.p_value)}
            for var, r in results['chi_square'].items() if 'error' not in r]
    return pd.DataFrame(rows)


def target_deviation(y_ref: pd.Series, y_curr: pd.Series) -> float:
    """Máxima diferencia absoluta entre las proporciones de clase."""
    return (y_ref.value_counts(normalize=True) - y_curr.value_counts(normalize=True)).abs().max()


def is_valid_category(value) -> bool:
    """Descarta 'nan' y valores numéricos colados en columnas categóricas."""
    s = str(value)
    if s.lower() == 'nan':
        return False
    try:
        float(s)
        return False
    except ValueError:
        return True
