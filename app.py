from flask import Flask, render_template, request, send_file
import pyautogui
import qrcode
import io
import socket

app = Flask(__name__)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Isso conecta com um IP externo só para obter o IP local, não envia dados
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

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
    url = f"http://{ip}:5050"
    qr_img = qrcode.make(url)

    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
