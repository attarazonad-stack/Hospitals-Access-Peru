# Hospitals-Access-Peru

# Filtrado de hospitales operativos

Para este proyecto se trabajó con la base de datos de hospitales del MINSA (IPRESS). Como nuestro objetivo era analizar la infraestructura de salud disponible para la población, se realizaron los siguientes pasos:

Filtrado por estado de funcionamiento:
Solo se consideraron los hospitales cuya columna Condición indicaba "EN FUNCIONAMIENTO". Esto asegura que los resultados reflejen la infraestructura realmente activa y disponible.

Eliminación de registros sin coordenadas válidas:
Algunos hospitales no tenían latitud (NORTE) o longitud (ESTE) registrada. Estos registros se eliminaron para poder generar mapas geoespaciales precisos y confiables.

Creación de geometría para análisis espacial:
Con las coordenadas válidas, se creó un GeoDataFrame usando GeoPandas. Esto permitió analizar la ubicación de los hospitales a nivel de distrito y departamento, y construir mapas coropléticos.

Impacto del filtrado en el análisis:
Gracias a estos filtros, los conteos de hospitales por distrito y departamento representan únicamente la infraestructura operativa, lo que mejora la precisión de los mapas y tablas resumen.
