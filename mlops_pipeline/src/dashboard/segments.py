"""Filtros de segmentación aplicados por igual a referencia y actual."""
from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

from mlops_pipeline.src.dashboard.data import MonitoringData


@dataclass(frozen=True)
class SegmentSelection:
    job_types: Optional[Sequence[str]] = None
    age_range: Optional[Tuple[int, int]] = None
    income_trends: Optional[Sequence[str]] = None


def apply_segments(data: MonitoringData, sel: SegmentSelection) -> MonitoringData:
    ref, curr = data.reference, data.current
    if sel.job_types and 'tipo_laboral' in ref.columns:
        data = data.where(ref['tipo_laboral'].isin(sel.job_types), curr['tipo_laboral'].isin(sel.job_types))
    ref, curr = data.reference, data.current
    if sel.age_range and 'edad_cliente' in ref.columns:
        lo, hi = sel.age_range
        data = data.where(ref['edad_cliente'].between(lo, hi), curr['edad_cliente'].between(lo, hi))
    ref, curr = data.reference, data.current
    if sel.income_trends and 'tendencia_ingresos' in ref.columns:
        data = data.where(ref['tendencia_ingresos'].isin(sel.income_trends),
                          curr['tendencia_ingresos'].isin(sel.income_trends))
    return data
