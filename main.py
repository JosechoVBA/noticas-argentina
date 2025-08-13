import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import os

# ==== CONFIGURACIÓN DESDE GITHUB SECRETS ====
EMAIL_USER = os.environ.get("EMAIL_USER")
EMAIL_PASS = os.environ.get("EMAIL_PASS")
EMAIL_TO = os.environ.get("EMAIL_TO")
# ============================================

# Portales de noticias
URLS = [
    "https://www.infobae.com/?noredirect",
    "https://tn.com.ar/",
    "https://www.lanacion.com.ar/",
    "https://www.c5n.com/"
]

# Palabras clave por categoría
PALABRAS_CLAVE = [
    "politica", "diputado", "gobierno", "eleccion",
    "economia", "finanzas", "empresario", "caputo",
    "policial", "delito", "detenido", "comisaria", "captura", 
    "judicial", "tribunal", "condena", "fallo",
    "salud", "hospital", "vacuna", "medico"
]

def limpiar_titulo(titulo):
    titulo = titulo.strip()
    titulo = re.sub(r"Por\s+\w+.*", "", titulo)
    titulo = re.sub(r"OPINION", "", titulo, flags=re.IGNORECASE)
    titulo = re.sub(r"\s{2,}", " ", titulo)
    titulo = re.sub(r"\.(?=[A-ZÁÉÍÓÚÑ])", ". ", titulo)
    return titulo

def es_relevante(titulo):
    t = titulo.lower()
    return any(palabra in t for palabra in PALABRAS_CLAVE)

def obtener_titulos(url):
    titulos = []
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup.find_all(["h1", "h2", "h3"]):
            t = tag.get_text(strip=True)
            t = limpiar_titulo(t)
            if 15 < len(t) < 180 and es_relevante(t):
                titulos.append(t)
    except Exception as e:
        print(f"Error al obtener de {url}: {e}")
    return titulos

def obtener_noticias():
    noticias = []
    for url in URLS:
        noticias.extend(obtener_titulos(url))
    noticias_limpias = list(dict.fromkeys(noticias))
    return noticias_limpias[:7]

def enviar_email(noticias):
    fecha = datetime.now().strftime("%d/%m/%Y")
    cuerpo = f"*Argentina ({fecha})*\n\n"
    for n in noticias:
        cuerpo += f"* {n}\n"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = f"Noticias Argentina - {fecha}"
    msg.attach(MIMEText(cuerpo, "plain", "utf-8"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print("✅ Email enviado correctamente")
    except Exception as e:
        print(f"❌ Error enviando email: {e}")

if __name__ == "__main__":
    noticias = obtener_noticias()
    enviar_email(noticias)
