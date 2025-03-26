import streamlit as st
import joblib
import pandas as pd
import numpy as np
import math
import os

# Cargar modelos y normalizador
ruta_modelo = os.path.join(os.path.dirname(__file__), "modelo.joblib")
ruta_normalizador = os.path.join(os.path.dirname(__file__), "normalizador.joblib")
ruta_ciudades = os.path.join(os.path.dirname(__file__), "frecuencia_ciudades.joblib")
ruta_paises = os.path.join(os.path.dirname(__file__), "frecuencia_paises.joblib")

modelo = joblib.load(ruta_modelo)
normalizador = joblib.load(ruta_normalizador)
frecuencia_ciudades = joblib.load(ruta_ciudades)
frecuencia_paises = joblib.load(ruta_paises)

# Diccionario de calidad del viento
calidad_viento_dict = {
    1: "Bueno",
    2: "Moderado",
    3: "Regular",
    4: "No Saludable",
    5: "Dañino",
    6: "Muy dañino"
}

# Título y subtítulo
st.title("Predicción Calidad del Aire")
st.subheader("Andrés Felipe Ardila Quiñones")

# Introducción
st.write("Esta aplicación permite predecir la calidad del aire en función de diversas variables ambientales y meteorológicas. Es una herramienta útil para evaluar la contaminación y tomar medidas preventivas.")

# Imagen
st.image("https://www.fundacionaquae.org/wp-content/uploads/2020/03/Como-se-mide-la-calidad-del-aire-2.jpg")

# Entrada de datos
st.markdown("**PM10**", help="")
pm10 = st.slider(" ", 10, 200, 50)
st.markdown("**NO2**", help="")
no2 = st.slider(" ", 5, 100, 30)
st.markdown("**SO2**", help="")
so2 = st.slider(" ", 1.0, 49.0, 10.0)
st.markdown("**CO**", help="")
co = st.slider(" ", 0.1, 10.0, 2.0)
st.markdown("**O3**", help="")
o3 = st.slider(" ", 10, 200, 70)
st.markdown("**Temperature**", help="")
temperature = st.slider(" ", -10, 40, 20)
st.markdown("**Humidity**", help="")
humidity = st.slider(" ", 10, 99, 50)
st.markdown("**Wind Speed**", help="")
wind_speed = st.slider(" ", 0.5, 200.0, 10.0)

st.markdown("**Día del mes**", help="")
day = st.number_input(" ", 1, 31, 15)

# Menú desplegable para el mes
meses = {"Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5, "Junio": 6,
         "Julio": 7, "Agosto": 8, "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12}
st.markdown("**Mes**", help="")
month_name = st.selectbox(" ", list(meses.keys()))
month = meses[month_name]

# Calcular sin_day y cos_month
sin_day = math.sin(2 * math.pi * day / 31)
cos_month = math.cos(2 * math.pi * month / 12)

# Menús desplegables para City_Frequency y Country_Frequency
# Menú desplegable para el país
st.markdown("**País**", help="")
country = st.selectbox(" ", list(frecuencia_paises.keys()))

# Definir ciudades según país
ciudades_por_pais = {
    "USA": ["Nueva York", "Los Ángeles"],
}

# Si el país es USA, permitir seleccionar la ciudad, de lo contrario asignar la única ciudad disponible
if country in ciudades_por_pais:
    st.markdown("**Ciudad**", help="")
    city = st.selectbox(" ", ciudades_por_pais[country])
else:
    city = list(frecuencia_ciudades.keys())[list(frecuencia_paises.keys()).index(country)]
    st.write(f"**Ciudad:** {city}")

# Convertir nombres a frecuencias
city_freq = frecuencia_ciudades.get(city, frecuencia_ciudades.get("New York", 0))

country_freq = frecuencia_paises[country]

# Crear DataFrame con el orden correcto
datos = pd.DataFrame([[pm10, no2, so2, co, o3, temperature, humidity, wind_speed, 0, sin_day, cos_month, city_freq, country_freq]],
                      columns=["PM10", "NO2", "SO2", "CO", "O3", "Temperature", "Humidity", "Wind Speed", "Calidad Viento", "sin_day", "cos_month", "City_Frequency", "Country_Frequency"])

# Normalizar datos
datos_normalizados = normalizador.transform(datos.drop(columns=["Calidad Viento"]))
datos_normalizados_df = pd.DataFrame(datos_normalizados, columns=datos.drop(columns=["Calidad Viento"]).columns)

# Predicción
prediccion = modelo.predict(datos_normalizados)[0]

# Interpretar predicción
calidad = calidad_viento_dict.get(prediccion, "Desconocido")
st.markdown(f"### La calidad del aire es: **{calidad}**")



# Línea separadora
st.markdown("---")

# Copyright
st.write("© UNAB 2025")
# st.write("**Número de predicción:**", prediccion)
# st.write("**Características normalizadas:**")
# st.dataframe(datos_normalizados_df)
# st.write("City:", city)
# st.write("Available city frequencies:", frecuencia_ciudades)

# city_freq = frecuencia_ciudades.get(city, 0)  # Usa .get() para evitar el KeyError
