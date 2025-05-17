# 📽️ PowerPoint Controller

Controle apresentações de slides do PowerPoint diretamente pelo celular via rede Wi-Fi. Basta rodar o programa, escanear o QR code gerado, abrir a apresentação em tela cheia e usar o celular como controle remoto (Avançar/Voltar).

---

## 🧠 Como Funciona

1. Inicie o programa.
2. Será exibido um endereço local no terminal (ex: `http://192.168.1.5:5050`) e um QR Code.
3. Com seu celular conectado à mesma rede, escaneie o QR ou acesse o link manualmente.
4. Abra a apresentação no PowerPoint em **modo de tela cheia**.
5. Use os botões na tela do celular para **avançar (→)** ou **voltar (←)** os slides.

Para encerrar o programa, pressione `CTRL + C` no terminal.

---

## 🖥️ Requisitos

- Python 3.7+
- Estar na mesma rede Wi-Fi com o PC e o celular

### 📦 Instale as dependências

```bash
pip install -r requirements.txt
