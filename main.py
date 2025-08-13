import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os

# URLs de noticias
urls = [
    "https://www.infobae.com/?noredirect",
    "https://tn.com.ar/",
    "https://www.lanacion.com.ar/",
    "https://www.c5n.com/"
]

def limpiar_titulo(titulo):
    # Eliminar texto después de "Por" (firmas de periodistas)
    if "Por" in titulo:
        titulo = titulo.split("Por")[0]
    # Eliminar "OPINION" o etiquetas similares
    titulo = titulo.replace("OPINION", "").strip()
    # Quitar saltos de línea y espacios extra
    return " ".join(titulo.split())

titulos_unicos = []
vistos = set()

for url in urls:
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        for h in soup.find_all(["h1", "h2", "h3"]):
            texto = limpiar_titulo(h.get_text())
            if texto and texto not in vistos and len(texto.split()) > 4:
                vistos.add(texto)
                titulos_unicos.append(texto)
    except Exception as e:
        print(f"Error en {url}: {e}")

# Formatear el correo
hoy = datetime.now().strftime("%d/%m/%Y")
cuerpo = f"*Argentina ({hoy})*\n\n" + "\n".join(f"* {t}" for t in titulos_unicos[:7])

# Enviar email
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

msg = MIMEText(cuerpo, "plain", "utf-8")
msg["Subject"] = f"Noticias Argentina - {hoy}"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_TO

try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_TO.split(","), msg.as_string())
    print("✅ Email enviado correctamente")
except Exception as e:
    print(f"❌ Error enviando email: {e}")
