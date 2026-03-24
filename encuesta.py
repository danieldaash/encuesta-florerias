# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 21:06:49 2026

@author: ednld
"""

import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


# Función para conectar y enviar datos
import json

def enviar_datos(fila):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    try:
        if "google_sheets" in st.secrets:
            # Cargamos el string de los secrets
            raw_creds = st.secrets["google_sheets"]["credentials"]
            # Lo convertimos a diccionario de Python
            creds_dict = json.loads(raw_creds)
            # Usamos el diccionario para autenticar
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        else:
            # Para pruebas locales en Spyder
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
            
        client = gspread.authorize(creds)
        hoja = client.open("Encuesta_Bioetanol").sheet1
        hoja.append_row(fila)
        return True
    except Exception as e:
        st.error(f"Error técnico: {e}")
        return False

# --- INTERFAZ DE USUARIO CON STREAMLIT ---
st.set_page_config(page_title="Registro de Encuestas", page_icon="📊")

st.title("📋 Encuesta Desechos de Florerias")
st.markdown("Use este formulario para registrarse.")

with st.form("form_encuesta", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nombre = st.text_input("Nombre del Encuestador")
        numcta = st.number_input("Numero de Cuenta", min_value=0.0, step=0.1)
       
    
    with col2:
        edad = st.number_input("Edad", min_value=0.0, step=0.1)
        ubicacion = st.selectbox("Ubicacion", ["Toluca", "Metepec", "Lerma", "Otro"])

    with col3:                   
        funcionar = st.selectbox("Va a funcionar", ["Si", "No", "La neta no c"])
 
    comentarios = st.text_area("Observaciones adicionales")
    
    boton = st.form_submit_button("Enviar a Google Sheets")

if boton:
    if nombre and numcta > 0:
        # Creamos la fila con fecha y hora automática
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        datos_a_enviar = [ahora, nombre, numcta, edad, ubicacion, comentarios]
        
        try:
            enviar_datos(datos_a_enviar)
            st.success("✅ ¡Datos guardados! Revisa tu Google Sheet.")
            st.balloons() # Un pequeño efecto visual de éxito
        except Exception as e:
            st.error(f"❌ Error de conexión: {e}")
    else:
        st.warning("⚠️ Por favor completa el nombre y la cantidad antes de enviar.")