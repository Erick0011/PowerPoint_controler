import qrcode

url = "http://192.168.20.251:5050"
img = qrcode.make(url)
img.show()
