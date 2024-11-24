import streamlit as st
import requests
import pandas as pd
from st_social_media_links import SocialMediaIcons
from concurrent.futures import ThreadPoolExecutor

# Claves de API
API_KEY = '6918168bd90cd569f3e2dba938c13a5c'
NEWS_API_KEY = '2cd906fab8e24eec869940190e33b6d0'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'

# URL de la imagen
imagen_url = "https://www.ahiva.info/gifs-animados/astronomia/Sol/Sol-50.gif"

# Mostrar la imagen encima del título
st.image(imagen_url, use_container_width=True)

def obtener_clima_y_coordenadas(ciudad):
    URL = f"{BASE_URL}q={ciudad}&appid={API_KEY}&units=metric&lang=es"
    return requests.get(URL).json()

def obtener_calidad_aire(lat, lon):
    url_calidad_aire = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    return requests.get(url_calidad_aire).json()

def obtener_indice_uv(lat, lon):
    url_uv = f"http://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={API_KEY}"
    return requests.get(url_uv).json()

def obtener_noticias_locales(ciudad):
    url_noticias = (
        f"https://newsapi.org/v2/everything?"
        f"q={ciudad}&apiKey={NEWS_API_KEY}&language=es&sortBy=popularity&pageSize=2"
    )
    return requests.get(url_noticias).json()

def mostrar_mapa(lat, lon):
    st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))

def procesar_datos(ciudad):
    try:
        with ThreadPoolExecutor() as executor:
            # Solicitudes concurrentes
            clima_future = executor.submit(obtener_clima_y_coordenadas, ciudad)
            noticias_future = executor.submit(obtener_noticias_locales, ciudad)
            
            # Esperar resultados
            clima_data = clima_future.result()
            noticias_data = noticias_future.result()

            if clima_data.get("cod") != "404":
                main, weather, wind, coord = clima_data['main'], clima_data['weather'][0], clima_data['wind'], clima_data['coord']
                st.write(f"### Información climática para {ciudad.capitalize()}:")
                st.write(f"**Temperatura:** {main['temp']}°C")
                st.write(f"**Descripción del clima:** {weather['description'].capitalize()}")
                st.write(f"**Velocidad del viento:** {wind['speed']} m/s, **Dirección:** {wind['deg']}°")

                # Solicitudes concurrentes adicionales
                calidad_aire_future = executor.submit(obtener_calidad_aire, coord['lat'], coord['lon'])
                indice_uv_future = executor.submit(obtener_indice_uv, coord['lat'], coord['lon'])

                calidad_aire_data = calidad_aire_future.result()
                if "list" in calidad_aire_data:
                    aqi = calidad_aire_data['list'][0]['main']['aqi']
                    calidad_aire = ["Buena", "Moderada", "Dañina para grupos sensibles", "Dañina", "Muy dañina"]
                    st.write(f"**Calidad del aire:** {calidad_aire[aqi-1]}")
                else:
                    st.write("No se pudo obtener la calidad del aire.")

                indice_uv_data = indice_uv_future.result()
                if "value" in indice_uv_data:
                    st.write(f"**Índice UV:** {indice_uv_data['value']}")
                else:
                    st.write("No se pudo obtener el índice UV.")

                # Mostrar mapa
                mostrar_mapa(coord['lat'], coord['lon'])
            else:
                st.write("Ciudad no encontrada.")

            # Mostrar noticias
            if noticias_data.get("status") == "ok" and "articles" in noticias_data:
                st.write("### Noticias locales más importantes:")
                for article in noticias_data['articles']:
                    if article.get("title") and article.get("description"):
                        st.write(f"**{article['title']}**")
                        st.write(article['description'])
                        st.write(f"[Leer más]({article['url']})")
                    else:
                        st.write("Noticia no tiene contenido válido.")
            else:
                st.write("No se encontraron noticias relevantes.")
    except Exception as e:
        st.error(f"Error al procesar los datos: {e}")

# Interfaz de usuario
st.title("Eco Explorer")
ciudad = st.text_input("Ingresa el nombre de una ciudad")

if st.button("Obtener información"):
    if ciudad:
        with st.spinner("Cargando información..."):
            procesar_datos(ciudad)
    else:
        st.warning("Por favor, ingresa el nombre de una ciudad.")

# Pie de página con información del desarrollador y redes sociales
st.markdown("""
---
**Desarrollador:** Edwin Quintero Alzate<br>
**Email:** egqa1975@gmail.com<br>
""", unsafe_allow_html=True)

social_media_links = [
    "https://www.facebook.com/edwin.quinteroalzate",
    "https://www.linkedin.com/in/edwinquintero0329/",
    "https://github.com/Edwin1719"]

social_media_icons = SocialMediaIcons(social_media_links)
social_media_icons.render()