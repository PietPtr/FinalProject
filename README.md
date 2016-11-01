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
- Java server:
  - Gson https://mvnrepository.com/artifact/com.google.code.gson/gson/2.7
  - SQLLite connector https://mvnrepository.com/artifact/org.xerial/sqlite-jdbc
- Python client:
  - Python 3.5.2 or newer https://www.python.org/
  - urllib3 https://urllib3.readthedocs.io/en/latest/
  - json https://docs.python.org/3/library/json.html
  - pyserial https://pypi.python.org/pypi/pyserial
- Web interface:
  - Firefox
- Database:
  [- TODO]
- Arduino (building):
  - MFRC522
  - SPI
  - BigNumber http://www.gammon.com.au/Arduino/BigNumber.zip

## Running

### Client computers

1) Install the requirements for the python client and web interface.

2) Plug in the Arduino with RFID reader connected.

3) Run "arduino-communicator.py" with Python 3.5.2

4) Navigate to the web address of the backend server in Firefox
