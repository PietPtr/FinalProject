import serial
import urllib3
import json

#ser = serial.Serial('/dev/ttyACM0', 9600)
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

port = input("What port are you on? If you don't know, just press enter.")

ser = serial.Serial()

if (port == ""):
    for i in range(10):
        try:
            ser = serial.Serial('/dev/ttyACM' + str(i), 9600)
            break
        except serial.serialutil.SerialException:
            continue
else:
    try:
        ser = serial.Serial(port, 9600)
    except serial.serialutil.SerialException:
        pass

if (ser.port == None and port == ""):
    print("It looks like your card scanning device is not connected,"
          " please plug it in this computer. \nIf it is plugged in, "
          "try a different USB port or cable. \n\n\nERROR CODE 000")
    exit()
elif (ser.port == None and port != ""):
    print("The program cannot find the card scanning device at the"
          " given port. \nPlease try running the program again and"
          " entering a different port. \nIf you are sure the port is"
          " correct, try plugging in the card scanning device in a"
          " different USB port or using a different USB cable. \n\n"
          "\nERROR CODE 001")
    exit()

print("Succesfully established a connection with the card scanning device! \n"
      "You can start scanning now.")

def encrypt(text):
    return text

def serialize(data):
    return json.dumps({'id': data, 'type': terminal_type})

def sendData(data):
    r = http.request(
        'POST',
        '130.89.231.249:8000/restaurant/cardswiped',
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
