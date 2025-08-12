import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os

# =========================
# CONFIGURACIÓN DE SITIOS
# =========================
NEWS_SITES = {
    "Infobae": "https://www.infobae.com/?noredirect",
    "TN": "https://tn.com.ar/",
    "La Nación": "https://www.lanacion.com.ar/",
    "C5N": "https://www.c5n.com/"
}

# Palabras clave para filtrar noticias relevantes
KEYWORDS = ["política", "economía", "policial", "judicial", "salud"]

# =========================
# FUNCIÓN PARA EXTRAER NOTICIAS
# =========================
def get_headlines(url, site_name):
    headlines = []
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # Obtiene todos los textos de etiquetas <a> y <h2>
        for tag in soup.find_all(["a", "h2"]):
            text = tag.get_text(strip=True)
            if any(k in text.lower() for k in KEYWORDS):
                if len(text.split()) > 3:  # Evitar titulares muy cortos
                    headlines.append(text)
    except Exception as e:
        headlines.append(f"[Error obteniendo noticias de {site_name}: {e}]")
    return headlines

# =========================
# GENERAR FORMATO FINAL
# =========================
def build_report():
    today = datetime.now().strftime("%d/%m/%Y")
    report_lines = [f"*Argentina ({today})*\n"]
    for site, url in NEWS_SITES.items():
        headlines = get_headlines(url, site)
        for h in headlines[:3]:  # Solo 3 titulares por sitio para no saturar
            report_lines.append(f"* {h}")
    return "\n".join(report_lines)

# =========================
# ENVIAR EMAIL
# =========================
def send_email(subject, body):
    sender = os.environ["EMAIL_USER"]
    password = os.environ["EMAIL_PASS"]
    recipient = os.environ["EMAIL_TO"]

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())
        print("✅ Email enviado correctamente.")
    except Exception as e:
        print(f"❌ Error enviando email: {e}")

# =========================
# EJECUCIÓN PRINCIPAL
# =========================
if __name__ == "__main__":
    report = build_report()
    send_email("Noticias Argentina", report)
