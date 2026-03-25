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


def enviar_datos(fila):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    try:
        # Si estamos en la nube (Streamlit Cloud), los secretos ya son un diccionario
        if "private_key" in st.secrets:
            creds_dict = {
              
    "type": st.secrets["type"],
    "project_id": st.secrets["project_id"],
    "private_key_id": st.secrets["private_key_id"],
    "private_key": st.secrets["private_key"].replace('\\n', '\n'),
    "client_email": st.secrets["client_email"],
    "client_id": st.secrets["client_id"],
    "auth_uri": st.secrets["auth_uri"],
    "token_uri": st.secrets["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["client_x509_cert_url"]
}
            
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        
        # Si estás probando localmente en tu Acer Nitro (Spyder)
        else:
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

        client = gspread.authorize(creds)
        # Asegúrate de que el nombre sea IDÉNTICO al de tu Google Sheet
        hoja = client.open("Encuesta_Florerias").sheet1
        hoja.append_row(fila)
        return True
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False

# --- INTERFAZ DE USUARIO CON STREAMLIT ---
st.set_page_config(page_title="Registro de Encuestas", page_icon="📊")

st.title("📋 Residuos florales")
st.markdown("Contestar cada pregunta que se indique")

with st.form("form_encuesta", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nombre = st.text_input("Nombre del alumno")
        numcta = st.number_input("Numero de Cuenta", min_value= 0, step= 1)
        ubicacion = st.selectbox("Municipio", ["Toluca", "Metepec", "Lerma", "Otro"])
    
    with col2:
        puno = st.selectbox("¿Con qué frecuencia compras flores?", ["Semanalmente", "Mensualmente", "Solo en fechas especiales", "Casi nunca"])
        pdos = st.selectbox("¿Qué sueles hacer con las flores cuando comienzan a marchitarse", ["Las tiro en la basura", "Las uso para composta", "Le doy otro uso"])
        ptres = st.selectbox("¿Qué flores de las siguiente lista prefieres comprar más?", ["Rosas", "Girasoles", "Gerbera", "Claveles", "Nube", "Gladiola", "Lirio"])
    
    with col3:                   
        bet = st.selectbox("¿Sabes qué es el bioetanol?", ["Si", "No"])
        if bet == "No":
            st.info("💡 **Dato rápido:** El bioetanol es un alcohol que se obtiene de plantas (como los tallos de las flores) y sirve como combustible ecológico.")
    compraria = st.radio("Sabiendo esto, ¿lo comprarías?", ["Sí", "No", "Tal vez"]) 
   

    
    comentarios = st.text_area("Observaciones adicionales")
    
    boton = st.form_submit_button("Enviar a Google Sheets")



if boton:
    if nombre and numcta > 0:
    
        datos_a_enviar = [nombre, numcta, ubicacion, puno, pdos, ptres, bet, compraria, comentarios]
        
        try:
            enviar_datos(datos_a_enviar)
            st.success("✅ ¡Datos guardados! Gracias.")
            st.balloons() # Un pequeño efecto visual de éxito
        except Exception as e:
            st.error(f"❌ Error de conexión: {e}")
    else:
        st.warning("⚠️ Por favor completa el nombre y la cantidad antes de enviar.")