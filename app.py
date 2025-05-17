from flask import Flask, render_template, request, send_file
import pyautogui
import qrcode
import io
import socket
import sys

app = Flask(__name__)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# Pegamos a porta antes de tudo
porta = int(sys.argv[1]) if len(sys.argv) > 1 else 5050

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
    app.run(host="0.0.0.0", port=porta)
