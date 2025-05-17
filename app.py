from flask import Flask, render_template, request, send_file
import pyautogui
import qrcode
import io
import socket

app = Flask(__name__)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))  # bind em porta 0 escolhe porta livre
    port = s.getsockname()[1]
    s.close()
    return port

# Escolhe porta livre
porta = find_free_port()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'next':
            pyautogui.press('right')
        elif action == 'prev':
            pyautogui.press('left')
    return render_template('index.html')

@app.route('/qr')
def qr():
    ip = get_local_ip()
    url = f"http://{ip}:{porta}"
    qr_img = qrcode.make(url)

    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == "__main__":
    ip = get_local_ip()
    print("=" * 50)
    print("✅ Controle Remoto de Slides Iniciado!")
    print(f"📱 Escaneie o QR code em: http://{ip}:{porta}/qr")
    print(f"🌐 Ou copie este endereço no celular: http://{ip}:{porta}")
    print()
    print("📤 Depois de acessar, abra a apresentação em tela cheia no PC")
    print("📲 E controle os slides direto do celular")
    print()
    print("⛔ Para fechar o servidor, pressione Ctrl + C")
    print("=" * 50)
    app.run(host="0.0.0.0", port=porta, debug=False, use_reloader=False)
