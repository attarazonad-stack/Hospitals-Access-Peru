# --- Librerías ---
import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

st.set_page_config(page_title="Hospitales Públicos Perú", layout="wide")

# --- Cargar datos ---
distritos = gpd.read_file(r"C:\Users\atara\Desktop\Hospitals-Access-Peru\_data\DISTRITOS.shp")
distritos = distritos[['IDDIST', 'DISTRITO', 'geometry']].rename(columns={'IDDIST': 'UBIGEO'})
distritos['UBIGEO'] = distritos['UBIGEO'].astype(int)
distritos = distritos.to_crs(epsg=4326)

hospitales = pd.read_csv(r"C:\Users\atara\Desktop\Hospitals-Access-Peru\_data\IPRESS.csv", encoding="latin1")
hospitales = hospitales[hospitales["Condición"] == "EN FUNCIONAMIENTO"]
hospitales = hospitales.dropna(subset=["ESTE", "NORTE"])
hospitales_gdf = gpd.GeoDataFrame(
    hospitales,
    geometry=gpd.points_from_xy(hospitales["NORTE"], hospitales["ESTE"]),
    crs="EPSG:4326"
)

# Conteo por distrito
hospitales_por_distrito = gpd.sjoin(hospitales_gdf, distritos, how="inner", predicate="within")
conteo = hospitales_por_distrito.groupby("UBIGEO_right").size().reset_index(name="num_hospitales")
conteo = conteo.rename(columns={"UBIGEO_right": "UBIGEO"})
distritos_hosp = distritos.merge(conteo, on="UBIGEO", how="left")
distritos_hosp["num_hospitales"] = distritos_hosp["num_hospitales"].fillna(0).astype(int)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🗂️ Descripción de los Datos", "🖼️ Mapas Estáticos", "🗺️ Mapas Dinámicos"])

# --- Pestaña 1 ---
with tab1:
    st.header("Descripción de los Datos")
    st.write(f"**Total de hospitales:** {len(hospitales)}")
    st.write("### Vista previa de los datos")
    st.dataframe(hospitales.head())
    
    st.write("### Distribución por Departamento")
    dept_summary = distritos_hosp.groupby('DISTRITO').sum()['num_hospitales']
    fig, ax = plt.subplots(figsize=(12,6))
    dept_summary.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_ylabel("Número de hospitales")
    ax.set_xlabel("Departamento")
    st.pyplot(fig)

# --- Pestaña 2 ---
with tab2:
    st.header("Mapas Estáticos (GeoPandas)")
    fig2, ax2 = plt.subplots(figsize=(12,12))
    distritos_hosp.plot(column="num_hospitales", cmap="Purples", legend=True, edgecolor="white", linewidth=0.3, ax=ax2)
    ax2.set_axis_off()
    st.pyplot(fig2)

# --- Pestaña 3 ---
with tab3:
    st.header("Mapas Dinámicos (Folium)")
    lat_centro = hospitales["ESTE"].mean()
    lon_centro = hospitales["NORTE"].mean()
    
    m = folium.Map(location=[lat_centro, lon_centro], zoom_start=6)
    folium.Choropleth(
        geo_data=distritos_hosp,
        data=distritos_hosp,
        columns=["UBIGEO", "num_hospitales"],
        key_on="feature.properties.UBIGEO",
        fill_color="Purples",
        line_opacity=0.2,
        fill_opacity=0.7,
        legend_name="Número de hospitales"
    ).add_to(m)
    
    marker_cluster = MarkerCluster().add_to(m)
    for idx, row in hospitales_gdf.iterrows():
        folium.Marker(
            location=[row["ESTE"], row["NORTE"]],
            popup=row["Nombre del establecimiento"]
        ).add_to(marker_cluster)
    
    st_folium(m, width=800, height=600)
