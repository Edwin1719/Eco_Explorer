import streamlit as st
import requests
from datetime import datetime
import pandas as pd
from st_social_media_links import SocialMediaIcons

API_KEY = '6918168bd90cd569f3e2dba938c13a5c'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
NEWS_API_KEY = '2cd906fab8e24eec869940190e33b6d0'

def obtener_informacion_climatica(ciudad):
    URL = f"{BASE_URL}q={ciudad}&appid={API_KEY}&units=metric"
    data = requests.get(URL).json()

    if data.get("cod") != "404":
        main, weather, wind, coord = data['main'], data['weather'][0], data['wind'], data['coord']

        st.write(f"### Información climática para {ciudad.capitalize()}:")
        st.write(f"**Temperatura:** {main['temp']}°C")
        st.write(f"**Descripción del clima:** {weather['description'].capitalize()}")
        st.write(f"**Velocidad del viento:** {wind['speed']} m/s, **Dirección:** {wind['deg']}°")

        obtener_calidad_aire(coord['lat'], coord['lon'])
        obtener_indice_uv(coord['lat'], coord['lon'])
        obtener_noticias_locales(ciudad)
        mostrar_mapa(coord['lat'], coord['lon'])
    else:
        st.write("Ciudad no encontrada.")

def obtener_calidad_aire(lat, lon):
    url_calidad_aire = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    data = requests.get(url_calidad_aire).json()

    if "list" in data:
        aqi = data['list'][0]['main']['aqi']
        calidad_aire = ["Buena", "Moderada", "Dañina para grupos sensibles", "Dañina", "Muy dañina"]
        st.write(f"**Calidad del aire:** {calidad_aire[aqi-1]}")
    else:
        st.write("No se pudo obtener la calidad del aire.")

def obtener_indice_uv(lat, lon):
    url_uv = f"http://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={API_KEY}"
    data = requests.get(url_uv).json()

    if "value" in data:
        st.write(f"**Índice UV:** {data['value']}")
    else:
        st.write("No se pudo obtener el índice UV.")

def obtener_noticias_locales(ciudad):
    url_noticias = f"https://newsapi.org/v2/everything?q={ciudad}&apiKey={NEWS_API_KEY}"
    data = requests.get(url_noticias).json()

    if data.get("status") == "ok":
        st.write("### Noticias locales:")
        for article in data['articles'][:5]:
            st.write(f"**{article['title']}**")
            st.write(f"{article['description']}")
            st.write(f"Leer más")
    else:
        st.write("No se pudieron obtener noticias locales.")

def mostrar_mapa(lat, lon):
    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))

# Interfaz de usuario
st.title("Eco Explorer")
ciudad = st.text_input("Ingresa el nombre de una ciudad")

if st.button("Obtener información"):
    if ciudad:
        obtener_informacion_climatica(ciudad)
    else:
        st.write("Por favor, ingresa el nombre de una ciudad.")

# Pie de página con información del desarrollador y logos de redes sociales
st.markdown("""
---
**Desarrollador:** Edwin Quintero Alzate<br>
**Email:** egqa1975@gmail.com<br>
""")

social_media_links = [
    "https://www.facebook.com/edwin.quinteroalzate",
    "https://www.linkedin.com/in/edwinquintero0329/",
    "https://github.com/Edwin1719"]

social_media_icons = SocialMediaIcons(social_media_links)
social_media_icons.render()