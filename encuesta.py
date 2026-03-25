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
                "type": st.secrets["service_account"],
                "project_id": st.secrets["pelagic-pager-491203-g4"],
                "private_key_id": st.secrets["b95be01d39a82f89dc8124412ed0680485a1a6e7"],
                # Reparamos los saltos de línea de la llave
                "private_key": st.secrets["-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCiZf+7Q5nhFJqL\nnGgSnmBg3Oj4F5lvS0z/WIndr5sBVWxCFrdbGyNS0/glr8Egh+7PNzl0SJGFvLRx\nJ6H0kZQuEmTMSJ60e8vV6rki7jPh4ynM1KuylabvPtGoUTVOhBMJN2UKYef0B3U4\nYK9UmpAWNCVbrv9cAjP5FNle9Ab1cM4D5bz64YP4ga2XFYYxJGc0NNG/ZVTtpu7T\n1wXEfx/KXo7wZq6zqCDm3CzgDWe4294CPZVAM/Ln7qf6xKwgVbXR3OfTawttHQ6G\n6qL77weuP7MsOlxLdGtpWfHFN9uSDBXsb7Lcpfs8Chql5PSN3YfX6F1aAJcTv6lG\n1kv3XpfzAgMBAAECggEAJeSe81cmxLpGBWWNcyq5WmCxi5IWHz32zW4fXTboeDsy\nc4lRZ1TBvUXwlPqZmbmeI4PDSDrWmdoaUHzq8WI2rTllg7U+Mubf/R4z7M6gFIko\n676EAbuhpBmIWjn4skVnG7NtRCrsMKi81VbaEmeuT0ADp40B0LpC3k/bGKjgJsy4\nXU5xyL/D26z5oi95ZhuusXJ48jA5kjzyZHIGVC9tbecRi+ZEc4zE1mn2c+jddlLd\nem3Il+Te2XOKRKtAkpGs+Tb1nIKMHEc9fyw9qyYxB2sKUbykFlt0KXwS2texi+Oq\nYCiyOlVDT1lVhR6wTS/Y74Pmk1TWTrFzgIGsynMMwQKBgQDNmR4JqAQKpipyNmGo\nIIP7HreoaOqp0pWeMBvTwK+4gThU0904I9q3kCGVDWxzFBJrQlv+uw82RNBO0vPd\nRNWUk+PBME+AdhOqc98LXCZgKm5/Id+4PFJE4byrqwxuaPVgjkE18JrX2N81R9sj\n3nFGefMuZZnT4fxi5T+3wSYsmwKBgQDKNcPmGGFhjyEalHJRSDAclG503HPovM7x\nqZ3z+FR/xaAb7ap4Vt0B5PqHQGSILVG4tE8WyxhvyqdcCAy4IF4v7PLxaQxDzYfJ\nnfb0HEVFDVu4jCVf6E1u99cw9cQYhq7PjayKIUmnftADMRpDqbp/69auIWkUKSDr\naZqkWQs7iQKBgEpCTrYgKG2MPPKJr9YhAGqYWq+KTY/PDtlW+QYPp6hVi/ofl9xq\nHtqERYznj081Zb219zJXcBQi4LZHvWsjLJ2AmRezElQM0eeT+HDK9NVxHf3vRzXt\nG63jdtjubAwI/u/EEcugvtzNaTl+Xalj87gH3gzZB6mfCyDROqVtLxOXAoGAThxe\nxC9+zpTfkMjvL/7WtvOPh4zxKWJl/mwrG+c9nO3WX3N7emjzjpvJOx3gt8np25Or\nSX7CvcxmweJKJ4Y5XAIIBsExf6+RWIywrLOO/pGecLeSaG3wG4GZmswVJ/Q+6uYr\nVGBvd0hBSjpZjvGtnWSY1UMKuEL6+HUey4WqFSECgYEAgYZNpbBj96YOCtxzgOcQ\nAdXyUvPKe+GHXwtIppWZTkHi66SXS1q01+gFTnpXypG7PsLgh9mtexdqpJARkwPM\nJrQ8bdkQ7B+B1/N/+jDUahGog01afQZKPPqCTGLnHCsZfS9ssOHOpVFpM+7163N4\nnclqOmlFCxPDc/JuiLZwVow=\n-----END PRIVATE KEY-----\n"].replace('\\n', '\n'),
                "client_email": st.secrets["encuesta-estadistica@pelagic-pager-491203-g4.iam.gserviceaccount.com"],
                "client_id": st.secrets["111353323689903883546"],
                "auth_uri": st.secrets["https://accounts.google.com/o/oauth2/auth"],
                "token_uri": st.secrets["https://oauth2.googleapis.com/token"],
                "auth_provider_x509_cert_url": st.secrets["https://www.googleapis.com/oauth2/v1/certs"],
                "client_x509_cert_url": st.secrets["https://www.googleapis.com/robot/v1/metadata/x509/encuesta-estadistica%40pelagic-pager-491203-g4.iam.gserviceaccount.com"]
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