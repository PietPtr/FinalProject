# Final Project

## Requirements

Hardware requirements:
- Server
- 2 Arduinos 
- 2 MFRC522 RFID readers
- Several PICC cards
- 2 Buzzers
- 2 Client computers

Software requirements:
- Server:
  - Python 3.5.2
  - Django 1.10.2
- Python client:
  - Python 3.5.2 or newer https://www.python.org/
  - urllib3 https://urllib3.readthedocs.io/en/latest/
  - json https://docs.python.org/3/library/json.html
  - pyserial https://pypi.python.org/pypi/pyserial
- Web interface:
  - Firefox
- Database:
  - None
- Arduino (building):
  - MFRC522
  - SPI
  - BigNumber http://www.gammon.com.au/Arduino/BigNumber.zip

## Running

### Client computers

1) Install the requirements for the python client and web interface.

2) Plug in the Arduino with RFID reader connected.

3) Run "arduino-communicator.py" with Python 3.5.2 and follow the instructions.

4) Navigate to the web address of the backend server in Firefox

### Server

1) Install the requirements for the server

2) Run "python3 manage.py runserver 0.0.0.0:8000" in a terminal

### Arduino card readers

1) Plug in the Arduino



