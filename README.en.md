<p align="center"><img src="https://dodysalim.github.io/assets/project-covers/credit.webp" alt="Credit Risk Monitor" width="100%"></p>

<h1 align="center">Credit Risk Monitor</h1>

<p align="center"><b>Preparation, evaluation and monitoring of a credit-risk model.</b></p>

<p align="center"><img src="https://img.shields.io/badge/Henry_·_Module_5-75E6CE?style=for-the-badge&labelColor=0b1222" alt="Henry · Module 5"></p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"> <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=flat-square&logo=scikitlearn&logoColor=white" alt="scikit-learn"> <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"> <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"> <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker"> <img src="https://img.shields.io/badge/Power_BI-F2C811?style=flat-square&logoColor=black" alt="Power BI">
</p>

<p align="center"><a href="https://dodysalim.github.io/"><b>🌐 Portfolio</b></a> · <a href="README.md"><b>🇪🇸 Versión en español</b></a></p>

---

## 📌 At a glance

| | |
| --- | --- |
| **🎯 Problem** | Evaluate an on-time payment model and detect data drift. |
| **🛠️ Solution** | MLOps pipeline: preprocessing, training, prediction API and drift monitoring (KS, PSI, Chi²). |
| **📈 Deliverables** | Local FastAPI service, modular monitoring dashboard and a 5-page Power BI report. |
| **🧪 Quality** | 26 automated tests; drift logic implemented as pure, testable functions. |

## 🏗️ Architecture

```mermaid
flowchart LR
    XLS[(Base_de_datos.xlsx)] --> FE[ft_engineering<br/>preprocesamiento]
    FE --> TR[Entrenamiento<br/>y evaluación] --> MOD[(models/)]
    MOD --> API[FastAPI<br/>predicción]
    FE --> DATA[dashboard/data<br/>referencia vs actual]
    DATA --> SEG[segments]
    SEG --> MON[ModelMonitor<br/>KS · PSI · Chi²]
    MON --> DR[dashboard/drift<br/>lógica pura]
    DR --> VIEWS[views<br/>salud · detalle · galería · correlaciones]
    MON --> PBI[Power BI · 5 páginas]
```

## 🚀 How to run

```bash
pip install -r requirements.txt
python -m streamlit run mlops_pipeline/src/app.py
python -m uvicorn mlops_pipeline.src.model_deploy:app --port 8080
python -m pytest tests -q
```

## ⚖️ Scope

The 'current' dataset is the holdout split, not production data.

---

<p align="center">
<b>Dody Dueñas Remache</b> · Data Analyst / Data Scientist · Guayaquil, Ecuador (remote LATAM)<br>
<a href="https://dodysalim.github.io/">Portfolio</a> · <a href="https://github.com/dodysalim">GitHub</a> · <a href="https://www.linkedin.com/in/dody-duenas/">LinkedIn</a> · <a href="mailto:dodydurema67@gmail.com">dodydurema67@gmail.com</a>
</p>
