import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# --- CONFIGURACIÓN PROTEGIDA ---
# os.getenv busca las variables que configuraremos luego en el servidor
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_a_telegram(datos):
    # Verificamos que las variables existan antes de intentar enviar
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Variables de entorno no configuradas.")
        return False
        
    mensaje = (
        f"🔔 *NUEVA COTIZACIÓN*\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 *Cliente:* {datos['nombre']}\n"
        f"📧 *Correo:* {datos['email']}\n"
        f"📞 *Teléfono:* {datos['telefono']}\n"
        f"🛡️ *Ramo:* {datos['seguro'].capitalize()}\n"
        f"💬 *Mensaje:* {datos['mensaje']}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🚀 _Agencia Rafael Diaz_"
    )
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, data=payload)
        return response.ok
    except Exception as e:
        print(f"Error: {e}")
        return False

# El resto de tus rutas (@app.route) se mantienen igual...