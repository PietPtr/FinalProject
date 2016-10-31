import serial
import urllib3
import json

ser = serial.Serial('/dev/ttyACM0', 9600)
http = urllib3.PoolManager()

terminal_type = "Unknown"

response = input("Are you the waiter (1) or the cashier (2)? ")
if (response == '1'):
    terminal_type = "waiter"
elif (response == '2'):
    terminal_type = "cashier"
else:
    print("Invalid answer")
    exit()


def encrypt(text):
    return text

def serialize(data):
    return json.dumps({'id': data, 'type': terminal_type})

def sendData(data):
    r = http.request(
        'POST',
        '130.89.228.250:8080/Restaurant/PythonReceiver',
        headers={'Content-Type': 'application/json'},
        body=serialize(encrypt(data)))
    r.read()

while True:
    data = str(ser.readline())
    data = data[2:16]

    if (data.startswith('ID')):
        id = data.split(' ')[1:5]

        # make sure that all bytes contain 2 hex numbers
        for i in range(len(id)):
            if len(id[i]) == 1:
                id[i] = '0' + id[i]

        id = ''.join(id)

        # convert the hex ID to a number
        num_id = int(id, 16)

        print(num_id)

        sendData(num_id)
    elif (data.startwith('KEY')):
        sendData(data)        
