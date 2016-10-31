import urllib3
import json

http = urllib3.PoolManager()

def encrypt(text):
    return text

def serialize(data):
    return json.dumps({'id': data, 'data': ""})

def sendData(data):
    r = http.request(
        'POST',
        '130.89.228.250:8080/Restaurant/PythonReceiver',
        headers={'Content-Type': 'application/json'},
        body=serialize(encrypt(data)))
    r.read()

sendData("10485")
sendData("Hello")
sendData("13z753")
sendData("9853634")
