# Texas Utility Prospecting & Market Prioritization


🚀 **Live app (Streamlit):**  
https://texas-utility-capstone.streamlit.app/

Streamlit app para priorizar códigos postales en Texas usando:
- distribuidoras eléctricas (utilities) por código postal (IOU y Non-IOU)
- infraestructura eléctrica (subestaciones) 

Proyecto de **data analytics & market intelligence** enfocado en la **priorización de mercado en Texas**, combinando datos de utilities eléctricas y proxies de infraestructura para identificar códigos postales con mayor potencial comercial.

---

## 🎯 Objetivo del proyecto

Responder una pregunta de negocio clara:

> **¿En qué zonas (ZIP Codes) conviene enfocar primero el esfuerzo comercial y de prospecting dentro del mercado eléctrico de Texas?**

El output final es un **ranking accionable de ZIPs** y una **lista priorizada de utilities** a contactar.

---

## 🧠 Enfoque analítico

El proyecto combina:

- **Presencia de utilities por ZIP**
  - IOU (Investor-Owned Utilities / empresas privadas)
  - Non-IOU (cooperativas, municipales)
- **Subestaciones eléctricas**
  - Usadas como *proxy de infraestructura y densidad del grid*
- **Scoring explicable**
  - Fácil de defender frente a negocio / stakeholders

---

## 🧩 Metodología

### 1. Ingesta & limpieza
Notebook: `00_ingesta_limpieza.ipynb`

- Normalización de ZIP Codes (string, 5 dígitos)
- Limpieza de nombres de utilities
- Tratamiento de valores nulos y ceros estructurales
- Validación de coordenadas geográficas

---

### 2. Exploratory Data Analysis (EDA)
Notebook: `01_EDA.ipynb`

- Distribuciones de utilities y subestaciones
- Identificación de outliers
- Validación de hipótesis de negocio

---

### 3. Ranking & priorización
Notebook: `02_ranking.ipynb`

- Cálculo de métricas clave:
  - `n_utilities`
  - `n_substations`
- Normalización Min-Max
- Score final (TMPS Score)
- 
- Generación de:
- Ranking completo de ZIPs
- Top ZIPs priorizados
- Utilities más presentes en ZIPs top (prospecting)

---

### 4. Machine Learning (exploratorio)
Notebook: `03_machine_learning.ipynb`

- Enfoque experimental
- Comparación con ranking heurístico
- Validación de estabilidad del score

---

## 🌐 Aplicación interactiva (Streamlit)

La app permite:

Filtrar ZIPs por:
- Nº mínimo de utilities
- Nº mínimo de subestaciones
- Rango de score
- Tipo de mercado (IOU vs Non-IOU)
  
Visualizar:
- Ranking dinámico
- Lista de prospects
- Mapa interactivo con subestaciones
- Descargar resultados filtrados en CSV

Archivo principal: **app/app.py**

---

## 📊 Power BI (offline)

El análisis también fue desarrollado en **Power BI Desktop** para:

- Exploración visual
- Validación de insights
- Presentación local

⚠️ **Limitación:**  
Power BI Service requiere suscripción paga para publicar dashboards online, por lo que **no se utiliza como solución final de deployment**.

👉 **Decisión profesional:**  
Streamlit se utiliza como **canal principal de entrega**, al ser:
- Público
- Reproducible
- Interactivo
- Accesible sin licencias

---

## 🛠️ Stack tecnológico

- Python
- Pandas
- Streamlit
- Folium
- Scikit-learn
- Power BI Desktop
- GitHub

---

## ▶️ Ejecutar el proyecto localmente

```bash
pip install -r requirements.txt
python -m streamlit run app/app.py


  
