import pandas as pd
from pathlib import Path
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, recall_score
from mlops_pipeline.src.ft_engineering import cargar_datos, feature_engineering
import platform
from mlops_pipeline.src.project_paths import MODEL_DIR, DATA_FILE

def train_and_save(data_file=None, model_dir=None):
    print("Iniciando carga de datos...")
    
    df = cargar_datos(Path(data_file) if data_file is not None else DATA_FILE)
    
    print("Ejecutando ingeniería de características...")
    X_train, X_test, y_train, y_test, preprocessor = feature_engineering(df)
    
    print("Entrenando el modelo (Regresión Logística con class_weight='balanced')...")
    # Solo ~4.7% de los clientes no paga a tiempo: se balancean las clases para detectarlos
    model = LogisticRegression(max_iter=2000, random_state=42, class_weight='balanced')
    model.fit(X_train, y_train)
    
    proba = model.predict_proba(X_test)[:, 1]
    print(f"ROC-AUC en Test: {roc_auc_score(y_test, proba):.4f}")
    print(f"Recall de impagos (clase 0): {recall_score(y_test, model.predict(X_test), pos_label=0):.4f}")
    
    print("Guardando el modelo y preprocesador...")
    # Creamos un directorio de modelos
    model_dir = Path(model_dir) if model_dir is not None else MODEL_DIR
    model_dir.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(model, model_dir / "modelo_final.pkl")
    joblib.dump(preprocessor, model_dir / "preprocesador.pkl")
    
    print("¡Modelos guardados con éxito en la carpeta 'models'!")

if __name__ == "__main__":
    train_and_save()
