import os
import qrcode

# Lee la URL base de la app desde variables de entorno
# Ejemplos:
# - Local: http://127.0.0.1:8000/
# - Railway: https://<tu-subdominio>.up.railway.app/
BASE_URL = os.getenv("APP_URL", "http://127.0.0.1:8000/")

# Ruta de destino del formulario de asistencia (por defecto QR general)
DEST_PATH = os.getenv("APP_ENTRY_PATH", "/auto/")

url = f"{BASE_URL.rstrip('/')}{DEST_PATH}"

img = qrcode.make(url)
img.save("qr_asistencia.png")
