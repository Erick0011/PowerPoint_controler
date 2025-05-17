import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode
import threading
import subprocess
import socket
import os
import signal
import webbrowser

APP_TITLE = "Controle de Slides"
AUTHOR = "Desenvolvido por Erick @ NextKode © 2025"
GITHUB_URL = "https://github.com/Erick0011/PowerPoint_controler"

server_process = None



def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def encontrar_porta_livre():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    porta_livre = s.getsockname()[1]
    s.close()
    return porta_livre


def iniciar_servidor(porta):
    global server_process
    server_process = subprocess.Popen([sys.executable, "app.py", str(porta)])



def parar_servidor():
    global server_process
    if server_process:
        server_process.terminate()
        server_process = None
        qr_label.config(image="")  # limpa o QR code
        messagebox.showinfo("Servidor Parado", "O servidor foi finalizado.")
    else:
        messagebox.showwarning("Servidor não iniciado", "Nenhum servidor está em execução.")



def gerar_qr_code(url):
    img = qrcode.make(url)
    img.save("qrcode.png")


def mostrar_qr_code(url):
    gerar_qr_code(url)
    img = Image.open("qrcode.png").resize((200, 200))
    img_tk = ImageTk.PhotoImage(img)
    qr_label.config(image=img_tk)
    qr_label.image = img_tk


def iniciar_app():
    porta = entry_porta.get()

    if not porta.isdigit():
        porta = encontrar_porta_livre()
    else:
        porta = int(porta)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', porta)) == 0:
                porta = encontrar_porta_livre()

    entry_porta.delete(0, tk.END)
    entry_porta.insert(0, str(porta))

    url = f"http://{get_ip()}:{porta}"
    threading.Thread(target=iniciar_servidor, args=(porta,), daemon=True).start()
    mostrar_qr_code(url)
    messagebox.showinfo("Servidor Iniciado", f"Acesse {url} no navegador do celular.")


def abrir_github():
    webbrowser.open(GITHUB_URL)


# GUI
janela = tk.Tk()
janela.title(APP_TITLE)
janela.geometry("360x540")
janela.resizable(False, False)


# Título
tk.Label(janela, text=APP_TITLE, font=("Arial", 18, "bold"), pady=10).pack()

# Campo de porta
tk.Label(janela, text="Porta:", font=("Arial", 12)).pack()
entry_porta = tk.Entry(janela, font=("Arial", 12), justify="center")
entry_porta.insert(0, "5050")
entry_porta.pack(pady=5)

# Botões de controle
tk.Button(janela, text="Iniciar Controle", command=iniciar_app,
          bg="#2e7d32", fg="white", font=("Arial", 12), padx=10, pady=5).pack(pady=5)

tk.Button(janela, text="Parar Servidor", command=parar_servidor,
          bg="#c62828", fg="white", font=("Arial", 12), padx=10, pady=5).pack(pady=5)

# QR code
qr_label = tk.Label(janela)
qr_label.pack(pady=10)

# Link do GitHub
tk.Button(janela, text="🔗 Ver projeto no GitHub", command=abrir_github,
          fg="#4CAF50", font=("Arial", 10, "underline"), relief="flat", cursor="hand2").pack(pady=5)

# Rodapé
tk.Label(janela, text=AUTHOR, font=("Arial", 9), fg="gray").pack(side="bottom", pady=10)

janela.mainloop()
