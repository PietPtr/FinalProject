import serial
import urllib3
import json
import sys

http = urllib3.PoolManager()

# This giant try except is used for loading the config file, and generating one
# if it doesn't exist. It also tries to provide solutions to the user for common
# errors.
try:
    file = open('relay.conf', 'r')
    server_address = file.readline().split('=')[1].replace('\n', '')
    terminal_type  = file.readline().split('=')[1].replace('\n', '')
except IndexError:
    # The file is not formatted correctly, so it's probably empty. By deleting
    # the file the next time the script is run a config file will be generated.
    print("An error occured while reading the config file.\n"
          "Please try deleting 'relay.conf' and try again.\n"
          "\n\n\nERROR CODE 003")
    exit()
except FileNotFoundError:
    file = open('relay.conf', 'w+')
    print("No config file was found. Let's create one now!")

    # Get and validate the server address from the user
    valid_server = False

    while (not valid_server):
        server_address = input("What is the IP address of the server? ")
        print("Hold on, I'm checking if this is indeed a "
              "server I am compatible with.")

        try:
            r = http.request('GET',
                server_address + ':8000/checkurl',
                timeout=1)
        except:
            print("This server doesn't seem to work... Please try another one.")
            continue

        if (not (r.data == b'Correct IP')):
            print("This server does respond, but something weird is going on.\n"
                  "Please contact the server administrator with the following "
                  "error code:\n\n\nERROR CODE 002: ", r.data)
        else:
            valid_server = True;

    print("Connected to a server!")

    # Get and validate the terminal_type from the user
    terminal_type = input("Is this the computer for the "
                          "waiter (1) or the cashier (2)? ")

    if (terminal_type is not "1" and terminal_type is not "2"):
        while(terminal_type is not "1" and terminal_type is not "2"):
            print("That is not a valid terminal type, please choose 1 or 2:")
            terminal_type = input("Is this the computer for the "
                                  "waiter (1) or the cashier (2)? ")

    if (terminal_type == "1"):
        terminal_type = "waiter"
    elif (terminal_type == "2"):
        terminal_type = "cashier"

    # Write data to config file
    file.write("server_address=" + str(server_address))
    file.write("\nterminal_type=" + str(terminal_type))

print("You are a", terminal_type)

port = input("What port are you on? If you don't know, just press enter and "
             "I'll look for one. ")

ser = serial.Serial()

# If the user didn't enter a port the script will look if /dev/ttyACM0 through
# /dev/ttyACM9 are valid ports.
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
          " please plug it in in this computer. \nIf it is plugged in, "
          "try a different USB port or cable. \n\n\nERROR CODE 000")
    exit()
elif (ser.port == None and port != ""):
    print("The program cannot find the card scanning device at the"
          " given port. \nPlease try running the program again and"
          " entering a different port. \nIf you are sure the port is"
          " correct, try plugging in the card scanning device in a"
          " different USB port or using a different USB cable, or on\n"
          " Linux, try 'chmod 777 /dev/$PORT', where $PORT is something"
          " like 'ttyACM0' or ttyUSB0"
          "\n\n\nERROR CODE 001")
    exit()

print("Succesfully established a connection with the card scanning device! \n"
      "You can start scanning now.")

def serialize(data):
    return json.dumps({'id': data, 'type': terminal_type})

def sendData(data):
    r = http.request(
        'POST',
        server_address + ':8000/cardswiped',
        headers={'Content-Type': 'application/json'},
        body=serialize(data))
    r.read()

def sendDataOverSerial(data):
    ser.write((data + "\n").encode())

# Infinite loop to read the serial data and send it to the backend.
while True:
    data = str(ser.readline())

    if (data[2:16].startswith('ENC')):
        encData = data.split(" ")[1].split("\\")[0]
        print("Succesfully scanned card!    ", encData)
        sendData(encData)
