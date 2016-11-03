import urllib3
import json

http = urllib3.PoolManager()

def encrypt(text):
    return text

def serialize(data, origin):
    return json.dumps({'id': data, 'type': origin})

def sendData(data, origin):
    packet=encrypt(serialize(data, origin))
    print(packet)
    r = http.request(
        'POST',
        'localhost:8000/cardswiped',
        headers={'Content-Type': 'application/json'},
        body=packet)
    r.read()
while True:
    icid   = input("ID  : ")
    ictype = input("Type: ")
    if ictype == "c":
        ctype = "cashier"
    elif ictype == "w":
        ctype = "waiter"
    if icid == "1":
        cid = "16515230"
    elif icid == "2":
        cid = "22321131"
    sendData(cid, ctype)

sendData("1048534", "cashier")
sendData("5763844", "cashier")
sendData("1347534", "waiter")
sendData("9853634", "waiter")
