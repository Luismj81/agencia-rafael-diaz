import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# --- 1. CONFIGURACIÓN PROTEGIDA ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- 2. FUNCIÓN PARA ENVIAR A TELEGRAM ---
def enviar_a_telegram(datos):
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
        print(f"Error enviando a Telegram: {e}")
        return False

# --- 3. RUTAS DE LA PÁGINA ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cotizar', methods=['POST'])
def cotizar():
    datos = {
        'nombre': request.form.get('nombre'),
        'email': request.form.get('email'),
        'telefono': request.form.get('telefono'),
        'seguro': request.form.get('seguro'),
        'mensaje': request.form.get('mensaje')
    }
    
    exito = enviar_a_telegram(datos)
    
    if exito:
        return jsonify({"status": "success", "message": "¡Cotización enviada!"})
    else:
        return jsonify({"status": "error", "message": "Error al enviar"}), 500

# --- 4. ARRANQUE DEL SERVIDOR ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
