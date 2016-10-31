import urllib3
import json

http = urllib3.PoolManager()

def encrypt(text):
    return text

def serialize(data, origin):
    return json.dumps({'cardId': data, 'cardData': "", 'originName': origin})

def sendData(data, origin):
    packet=encrypt(serialize(data, origin))
    print(packet)
    r = http.request(
        'POST',
        'localhost:8080/Restaurant/PythonReceiver',
        headers={'Content-Type': 'application/json'},
        body=packet)
    r.read()

sendData("10485", "Terminal1")
sendData("576384", "Terminal1")
sendData("134753", "Terminal2")
sendData("9853634", "Terminal2")
