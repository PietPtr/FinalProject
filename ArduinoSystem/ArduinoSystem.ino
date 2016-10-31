/*
 * MFRC522 - Library to use ARDUINO RFID MODULE KIT 13.56 MHZ WITH TAGS SPI W AND R BY COOQROBOT.
 * The library file MFRC522.h has a wealth of useful info. Please read it.
 * The functions are documented in MFRC522.cpp.
 *
 * Based on code Dr.Leong   ( WWW.B2CQSHOP.COM )
 * Created by Miguel Balboa (circuitito.com), Jan, 2012.
 * Rewritten by Søren Thing Andersen (access.thing.dk), fall of 2013 (Translation to English, refactored, comments, anti collision, cascade levels.)
 * Released into the public domain.
 *
 * Sample program showing how to read data from a PICC using a MFRC522 reader on the Arduino SPI interface.
 *----------------------------------------------------------------------------- empty_skull
 * Aggiunti pin per arduino Mega
 * add pin configuration for arduino mega
 * http://mac86project.altervista.org/
 ----------------------------------------------------------------------------- Nicola Coppola
 * Pin layout should be as follows:
 * Signal     Pin              Pin               Pin
 *            Arduino Uno      Arduino Mega      MFRC522 board
 * ------------------------------------------------------------
 * Reset      9                5                 RST
 * SPI SS     10               53                SDA
 * SPI MOSI   11               51                MOSI
 * SPI MISO   12               50                MISO
 * SPI SCK    13               52                SCK1
 *
 * The reader can be found on eBay for around 5 dollars. Search for "mf-rc522" on ebay.com.
 */

#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);	// Create MFRC522 instance.

byte previous_uid[10];

unsigned long lastScanTime = 0;

void setup() {
	Serial.begin(9600);	// Initialize serial communications with the PC
	SPI.begin();			// Init SPI bus
	mfrc522.PCD_Init();	// Init MFRC522 card
}

void beep() {
  tone(3, 540, 80);
  delay(100);
  tone(3, 540, 80);
}

void loop() {
  if (micros() - lastScanTime >= 10000000) {
    for (int i = 0; i < 10; i++) {
      previous_uid[i] = 0;
    }
  }

	// Look for new cards
	if ( ! mfrc522.PICC_IsNewCardPresent()) {
		return;
	}

	// Select one of the cards
	if ( ! mfrc522.PICC_ReadCardSerial()) {
		return;
	}

  // Check if this card has been scanned before
  // by comparing its ID to previous_uid
  bool equal = false;
  for (int i = 0; i < mfrc522.uid.size; i++) {
    equal = mfrc522.uid.uidByte[i] == previous_uid[i];
    if (!equal) {
      break;
    }
  }
  if (equal) {
    return;
  }


  Serial.print("ID ");

  for (int i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(String(mfrc522.uid.uidByte[i], HEX));
    Serial.print(" ");
  }
  Serial.print("\n");

  for (int i = 0; i < mfrc522.uid.size; i++) {
    previous_uid[i] = mfrc522.uid.uidByte[i];
  }

  beep();

  lastScanTime = micros();
}
