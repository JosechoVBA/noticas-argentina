📰 Noticias Argentina Diario

Este repositorio contiene un script automatizado en Python que realiza un scraping diario de noticias argentinas y envía un resumen por correo electrónico. El proyecto está diseñado para ejecutarse automáticamente mediante GitHub Actions, sin necesidad de mantener una computadora encendida, garantizando puntualidad y eficiencia en la entrega de información.

⚙️ Funcionalidades

🔹 Scraping de portales de noticias argentinos:
Captura titulares de los principales medios:

Infobae

TN

La Nación

C5N

🔹 Filtrado temático de noticias:

Se seleccionan titulares relevantes dentro de las siguientes categorías:

Política

Economía

Policiales

Judiciales

Salud

🔹 Limpieza de contenido:
Se eliminan firmas, subtítulos excesivos y etiquetas de opinión para asegurar un formato conciso y profesional.

🔹 Envío de correo electrónico automático:
El correo incluye el resumen diario de titulares con formato limpio y uniforme.

Configuración de remitente y destinatarios mediante GitHub Secrets para máxima seguridad.

🔹 Ejecución programada:

Configurable con GitHub Actions para enviarse automáticamente de lunes a viernes a las 08:00 horas (Colombia).

Permite ejecución manual para pruebas y ajustes rápidos.

📝 Requisitos

Python 3.10 o superior

Librerías de Python (listadas en requirements.txt):

requests
beautifulsoup4
🔧 Configuración

Clonar el repositorio:

bash
Copiar
Editar
git clone https://github.com/tu-usuario/noticias-argentina.git
cd noticias-argentina

Configurar los Secrets en GitHub:

EMAIL_USER: Dirección de correo del remitente.
EMAIL_PASS: Contraseña de aplicación (Gmail).
EMAIL_TO: Correo(s) de destino (separados por coma si son varios).
Verificar el workflow en .github/workflows/noticias.yml para confirmar la programación deseada.

🚀 Uso

Prueba local / Colab:

Ejecutar main.py en modo DEBUG_ONLY = True para visualizar titulares sin enviar correo.
Producción:

Cambiar DEBUG_ONLY = False y dejar que GitHub Actions ejecute automáticamente.

📈 Beneficios

Información diaria resumida de noticias argentinas relevantes.
Automatización completa sin necesidad de intervención manual.
Formato profesional listo para lectura rápida y análisis.

⚠️ Notas importantes

La cuenta de correo del remitente debe permitir acceso mediante contraseña de aplicación (Gmail).
Los titulares se filtran según palabras clave; ajustes futuros pueden ampliar o refinar la selección de noticias.

🧰 Tecnologías

Python 3
GitHub Actions
BeautifulSoup
SMTP para envío de emails

📄 Licencia

Este proyecto es open source y puede ser adaptado y utilizado libremente, respetando la atribución al autor.

