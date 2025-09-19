# streamlit
pip install streamlit-folium

#Librerias

import streamlit as st
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

# --------------------
# Configuración general
# --------------------
st.set_page_config(page_title="Hospitales Públicos Perú", layout="wide")

st.title("🏥 Hospitales Públicos Operativos en el Perú")

# --------------------
# Pestañas
# --------------------
tabs = st.tabs([
    "📄 Descripción de los datos",
    "🗺️ Mapas estáticos y análisis departamental",
    "🧭 Mapas dinámicos"
])

# --------------------
# Función auxiliar para cargar hospitales
# --------------------
def load_hospitals(csv_path):
    try:
        df = pd.read_csv(csv_path)
        # Convertir a GeoDataFrame si tiene lat/lon
        if 'latitud' in df.columns and 'longitud' in df.columns:
            gdf = gpd.GeoDataFrame(
                df,
                geometry=gpd.points_from_xy(df['longitud'], df['latitud']),
                crs="EPSG:4326"
            )
            return gdf
        return None
    except Exception as e:
        st.error(f"Error cargando CSV de hospitales: {e}")
        return None

# --------------------
# Pestaña 1: Descripción de los datos
# --------------------
with tabs[0]:
    st.header("📄 Descripción de los datos")

    st.markdown("""
    **Unidad de análisis:** Hospitales públicos operativos en el Perú.  

    **Fuentes de datos:**  
    - MINSA – IPRESS (subconjunto operativo): `C:/Users/atara/Desktop/Hospitals-Access-Peru/Outputs/hospitals_ipress.csv`  
    - Centros Poblados (distritos): `C:/Users/atara/Desktop/Hospitals-Access-Peru/_data/DISTRITOS.shp`  
    - IPRESS original: `C:/Users/atara/Desktop/Hospitals-Access-Peru/_data/IPRESS.csv`  
    - Centros Poblados IGN: `C:/Users/atara/Desktop/Hospitals-Access-Peru/_data/CCPP_IGN100K.shp`  

    **Reglas de filtrado:** Solo hospitales operativos con latitud y longitud válidas.
    """)

    # Entrada para cargar CSV de hospitales
    csv_path = st.sidebar.text_input(
        "Ruta al CSV de hospitales (MINSA IPRESS)",
        value="C:/Users/atara/Desktop/Hospitals-Access-Peru/Outputs/hospitals_ipress.csv"
    )
    hospitals_gdf = load_hospitals(csv_path)

    if hospitals_gdf is not None:
        st.success(f"Datos cargados: {len(hospitals_gdf)} registros")
        st.dataframe(hospitals_gdf.head())
    else:
        st.warning("Cargue un archivo CSV válido para visualizar los datos.")


# --------------------
# Pestaña 2: Mapas estáticos y resumen departamental
# --------------------
with tabs[1]:
    st.header("🗺️ Mapas estáticos y análisis departamental")

    # Ruta por defecto a Outputs
    outputs_dir = st.sidebar.text_input("Carpeta Outputs (png/html)", value="Outputs")

    # Archivos PNG esperados
    expected_pngs = {
        'Mapa 1': 'Mapa1.png',
        'Mapa 2': 'Mapa2.png',
        'Mapa 3': 'Mapa3.png',
        'Mapa Coroplético': 'Mapacoroplético.png',
        'Gráfico hospitales por departamento': 'hospitales_por_departamento.png'
    }

    st.subheader("Mapas estáticos cargados desde Outputs")
    for title, fname in expected_pngs.items():
        fullpath = f"{outputs_dir}/{fname}"
        try:
            st.image(fullpath, caption=title, use_column_width=True)
        except Exception as e:
            st.info(f"No se encontró {fname} en {outputs_dir} (o no se puede leer): {e}")

    # Mostrar tabla CSV de resumen departamental
    csv_summary = f"{outputs_dir}/hospitales_por_departamento.csv"
    try:
        df_summary = pd.read_csv(csv_summary)
        st.subheader("Tabla de resumen por departamento")
        st.dataframe(df_summary)
    except Exception as e:
        st.info(f"No se encontró hospitales_por_departamento.csv en {outputs_dir}: {e}")

    st.markdown("---")

# --------------------
# Pestaña 3: Mapas dinámicos con Folium
# --------------------
with tabs[2]:
    st.header("🧭 Mapas dinámicos (Folium)")

    outputs_dir = st.sidebar.text_input("Carpeta Outputs (png/html)", value="Outputs", key="outputs_dir_input")


    # Archivos HTML esperados
    html_files = {
        'Mapa interactivo nacional': 'mapa_interactivo_hospitales.html',
        'Mapa de proximidad': 'mapa_proximidad.html'
    }

    st.subheader("Mapas interactivos (archivos HTML)")
    any_html = False
    for title, fname in html_files.items():
        fullpath = f"{outputs_dir}/{fname}"
        try:
            with open(fullpath, 'r', encoding='utf-8') as f:
                html = f.read()
            st.markdown(f"**{title}**")
            components.html(html, height=600, scrolling=True)
            any_html = True
        except Exception as e:
            st.info(f"No se encontró o no se puede leer {fname} en {outputs_dir}: {e}")

    if not any_html:
        st.warning("No se cargó ningún archivo HTML desde la carpeta Outputs. Verifica nombres y la ruta en la barra lateral.")

    st.markdown("---")
    st.caption("Nota: Ajuste nombres de archivos según su carpeta Outputs.")
