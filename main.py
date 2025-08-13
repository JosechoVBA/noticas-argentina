import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import re

# Portales a scrapear
PORTALES = [
    "https://www.infobae.com/?noredirect",
    "https://tn.com.ar/",
    "https://www.lanacion.com.ar/",
    "https://www.c5n.com/"
]

# Categorías relevantes
CATEGORIAS = ["política", "economía", "policial", "judicial", "salud"]

def limpiar_titulo(titulo):
    titulo = titulo.strip()
    # Quitar "OPINION" aunque esté pegado
    titulo = re.sub(r"OPINION", "", titulo, flags=re.IGNORECASE)
    # Cortar todo desde "Por" (con o sin espacio antes)
    titulo = re.split(r"\b[Pp]or\b", titulo)[0]
    # Arreglar puntos pegados a mayúsculas
    titulo = re.sub(r"\.(?=[A-ZÁÉÍÓÚÑ])", ". ", titulo)
    # Quitar espacios extra
    titulo = " ".join(titulo.split())
    return titulo

def obtener_noticias():
    noticias = []
    for url in PORTALES:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            titulos = soup.find_all(["h1", "h2", "h3"])
            for t in titulos:
                texto = t.get_text(strip=True)
                texto_limpio = limpiar_titulo(texto)
                if any(cat in texto_limpio.lower() for cat in CATEGORIAS):
                    if texto_limpio not in noticias:
                        noticias.append(texto_limpio)
        except Exception as e:
            print(f"Error procesando {url}: {e}")
    return noticias

def enviar_email(noticias):
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    EMAIL_TO = os.getenv("EMAIL_TO")

    fecha = datetime.now().strftime("%d/%m/%Y")
    cuerpo = f"*Argentina ({fecha})*\n\n"
    for n in noticias:
        cuerpo += f"* {n}\n"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = f"Noticias Argentina - {fecha}"
    msg.attach(MIMEText(cuerpo, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_TO.split(","), msg.as_string())
        print("✅ Email enviado")
    except Exception as e:
        print(f"❌ Error enviando email: {e}")

if __name__ == "__main__":
    noticias = obtener_noticias()
    enviar_email(noticias)
