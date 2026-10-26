"""Carga de datos y partición referencia (entrenamiento) / actual (holdout)."""
import os
from dataclasses import dataclass, replace
from typing import Callable, Iterable, Optional

import pandas as pd
from sklearn.model_selection import train_test_split

from mlops_pipeline.src.dashboard import config


@dataclass(frozen=True)
class MonitoringData:
    """Variables crudas y objetivos de los conjuntos de referencia y actual."""
    reference: pd.DataFrame
    current: pd.DataFrame
    y_reference: pd.Series
    y_current: pd.Series

    def where(self, ref_mask: pd.Series, curr_mask: pd.Series) -> "MonitoringData":
        return replace(self, reference=self.reference[ref_mask], current=self.current[curr_mask],
                       y_reference=self.y_reference[ref_mask], y_current=self.y_current[curr_mask])


def find_data_file(paths: Iterable[str] = config.DATA_SEARCH_PATHS,
                   exists: Optional[Callable[[str], bool]] = None) -> Optional[str]:
    exists = exists or os.path.exists
    return next((p for p in paths if exists(p)), None)


def build_monitoring_data(df: pd.DataFrame, feature_engineering: Callable) -> MonitoringData:
    """Separa referencia/actual con el mismo split del entrenamiento.

    Se monitorean las variables crudas (dinero, edad reales), no las escaladas: así el drift
    se expresa en unidades que el negocio entiende. Los objetivos provienen de
    `feature_engineering` para coincidir exactamente con los usados al entrenar.
    """
    _, _, y_train, y_test, _ = feature_engineering(df)
    X = df.drop(columns=[config.TARGET])
    X_train, X_test, _, _ = train_test_split(X, df[config.TARGET], test_size=config.TEST_SIZE,
                                             random_state=config.RANDOM_STATE, stratify=df[config.TARGET])
    drop = [c for c in config.DROP_FOR_DRIFT if c in X.columns]
    return MonitoringData(X_train.drop(columns=drop), X_test.drop(columns=drop), y_train, y_test)
