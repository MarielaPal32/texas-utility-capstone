import os
import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from pathlib import Path

st.set_page_config(page_title="Texas Utility Prospecting", layout="wide")

st.title("Texas Utility Prospecting & Market Prioritization")
st.caption("Capstone: priorización de mercado en Texas usando utilities + infraestructura (subestaciones).")

BASE = Path(__file__).resolve().parents[1]
RANK_PATH = BASE / "outputs" / "texas_priority_zip_ranking.csv"
PROSPECTS_PATH = BASE / "outputs" / "top_prospects_in_top50_zips.csv"
SUB_PATH = BASE / "data" / "processed" / "substations_tx.csv"

df_rank = pd.read_csv(RANK_PATH)

# Sidebar filtros
st.sidebar.header("Filtros")
top_n = st.sidebar.slider("Top N ZIPs", 10, 300, 50, 10)

min_utils = st.sidebar.slider("Mínimo utilities en ZIP", 0, int(df_rank["n_utilities"].max()), 1)
min_subs = st.sidebar.slider("Mínimo subestaciones en ZIP", 0, int(df_rank["n_substations"].max()), 1)

score_min, score_max = st.sidebar.slider(
    "Rango de score",
    0.0,
    float(df_rank["tmps_score"].max()),
    (0.0, float(df_rank["tmps_score"].max())),
)

df_f = df_rank[
    (df_rank["n_utilities"] >= min_utils)
    & (df_rank["n_substations"] >= min_subs)
    & (df_rank["tmps_score"] >= score_min)
    & (df_rank["tmps_score"] <= score_max)
].copy()

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("ZIPs en ranking", f"{df_rank.shape[0]:,}")
c2.metric("ZIPs filtrados", f"{df_f.shape[0]:,}")
c3.metric("Máx subestaciones", int(df_rank["n_substations"].max()))
c4.metric("Máx utilities", int(df_rank["n_utilities"].max()))

tab1, tab2, tab3, tab4 = st.tabs(["Ranking", "Prospects", "Mapa", "Metodología"])

with tab1:
    st.subheader("Ranking de ZIPs")
    st.write("ZIPs con mejor score según: utilities (presencia comercial) + subestaciones (infraestructura).")
    st.dataframe(df_f.head(top_n), width="stretch")

    st.download_button(
        "Descargar ranking filtrado (CSV)",
        data=df_f.to_csv(index=False).encode("utf-8"),
        file_name="ranking_filtrado.csv",
        mime="text/csv",
    )

with tab2:
    st.subheader("Prospecting: a quién llamar primero")
    if os.path.exists(PROSPECTS_PATH):
        df_pros = pd.read_csv(PROSPECTS_PATH)
        st.write("Utilities que más aparecen en ZIPs prioritarios (Top 50 del notebook).")
        st.dataframe(df_pros.head(80), width="stretch")
        st.download_button(
            "Descargar prospects (CSV)",
            data=df_pros.to_csv(index=False).encode("utf-8"),
            file_name="prospects_top.csv",
            mime="text/csv",
        )
    else:
        st.error("No encuentro outputs/top_prospects_in_top50_zips.csv. Generalo desde 02_ranking.ipynb.")

with tab3:
    st.subheader("Mapa (infraestructura en ZIPs top)")
    st.caption("Mostramos subestaciones dentro de ZIPs prioritarios como proxy visual de infraestructura.")

    st.write("Buscando archivo en:", str(SUB_PATH))

    if not os.path.exists(SUB_PATH):
        st.error("❌ No encuentro el archivo substations_tx.csv en el repo.")
        st.write("Revisá que exista: data/processed/substations_tx.csv")
        st.stop()

    df_sub = pd.read_csv(SUB_PATH, low_memory=False)

    # ZIPs top según filtros actuales
    top_zips_now = df_f.head(top_n)["zip"].astype(str).tolist()

    df_sub["ZIP"] = df_sub["ZIP"].astype(str).str.extract(r"(\d+)", expand=False).str.zfill(5)
    df_map = df_sub[df_sub["ZIP"].isin(top_zips_now)].copy()

    df_map["LATITUDE"] = pd.to_numeric(df_map["LATITUDE"], errors="coerce")
    df_map["LONGITUDE"] = pd.to_numeric(df_map["LONGITUDE"], errors="coerce")
    df_map = df_map.dropna(subset=["LATITUDE", "LONGITUDE"])

    st.write(f"Subestaciones en ZIPs top: {len(df_map):,}")

    sample_n = min(len(df_map), 2000)
    df_s = df_map.sample(sample_n, random_state=42) if sample_n > 0 else df_map

    m = folium.Map(location=[31.0, -99.0], zoom_start=6)
    cluster = MarkerCluster().add_to(m)

    for _, r in df_s.iterrows():
        popup = f"{r.get('NAME','')} - {r.get('CITY','')} ({r.get('COUNTY','')})"
        folium.Marker([r["LATITUDE"], r["LONGITUDE"]], popup=popup).add_to(cluster)

    st_folium(m, width=1100, height=600)

with tab4:
    st.subheader("Metodología")
    st.markdown(
        """
**Problema**
Priorizar dónde enfocar prospecting de utilities/co-ops en Texas, usando datos de mercado e infraestructura.

**Datos**
- Utilities por ZIP (IOU y Non-IOU): identifica compradores/gatekeepers y presencia territorial.
- Subestaciones: proxy de infraestructura eléctrica (demanda/red).

**Limpieza mínima (por qué)**
- ZIP como texto 5 dígitos: evita perder ceros y permite joins.
- `utility_name` strip: evita duplicados falsos.
- Coordenadas numéricas y sin nulos: mapa confiable.
- Rates: 0 → NaN (cuando aplica) para evitar promedios engañosos (0 suele representar faltante en este tipo de dataset).

**Score (simple y explicable)**
- Normalizamos `n_utilities` y `n_substations` (min-max).
- Score = 0.4 * utilities_norm + 0.6 * substations_norm
        """
    )

    with st.expander("🧠 Glosario"):
        try:
            with open("docs/glosario.md", "r", encoding="utf-8") as f:
                st.markdown(f.read())
        except FileNotFoundError:
            st.warning("No se encontró docs/glosario.md. Verificá que esté subido al repo.")


