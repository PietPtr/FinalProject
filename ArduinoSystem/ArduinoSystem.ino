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

byte KEY[8] = {0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xFF};
const int NUMROUNDS = 32;

byte previous_uid[10];

unsigned long lastScanTime = 0;


byte sbox[] =
{ 0x02, 0x03, 0x05, 0x07, 0x0B, 0x0D, 0x11, 0x13,
  0x17, 0x1D, 0x1F, 0x25, 0x29, 0x2B, 0x2F, 0x35,
  0x3B, 0x3D, 0x43, 0x47, 0x49, 0x4F, 0x53, 0x59,
  0x61, 0x65, 0x67, 0x6B, 0x6D, 0x71, 0x7F, 0x83,
  0x89, 0x8B, 0x95, 0x97, 0x9D, 0xA3, 0xA7, 0xAD,
  0xB3, 0xB5, 0xBF, 0xC1, 0xC5, 0xC7, 0xD3, 0xDF,
  0xE3, 0xE5, 0xE9, 0xEF, 0xF1, 0xFB, 0x01, 0x07,
  0x0D, 0x0F, 0x15, 0x19, 0x1B, 0x25, 0x33, 0x37,
  0x39, 0x3D, 0x4B, 0x51, 0x5B, 0x5D, 0x61, 0x67,
  0x6F, 0x75, 0x7B, 0x7F, 0x85, 0x8D, 0x91, 0x99,
  0xA3, 0xA5, 0xAF, 0xB1, 0xB7, 0xBB, 0xC1, 0xC9,
  0xCD, 0xCF, 0xD3, 0xDF, 0xE7, 0xEB, 0xF3, 0xF7,
  0xFD, 0x09, 0x0B, 0x1D, 0x23, 0x2D, 0x33, 0x39,
  0x3B, 0x41, 0x4B, 0x51, 0x57, 0x59, 0x5F, 0x65,
  0x69, 0x6B, 0x77, 0x81, 0x83, 0x87, 0x8D, 0x93,
  0x95, 0xA1, 0xA5, 0xAB, 0xB3, 0xBD, 0xC5, 0xCF,
  0xD7, 0xDD, 0xE3, 0xE7, 0xEF, 0xF5, 0xF9, 0x01,
  0x05, 0x13, 0x1D, 0x29, 0x2B, 0x35, 0x37, 0x3B,
  0x3D, 0x47, 0x55, 0x59, 0x5B, 0x5F, 0x6D, 0x71,
  0x73, 0x77, 0x8B, 0x8F, 0x97, 0xA1, 0xA9, 0xAD,
  0xB3, 0xB9, 0xC7, 0xCB, 0xD1, 0xD7, 0xDF, 0xE5,
  0xF1, 0xF5, 0xFB, 0xFD, 0x07, 0x09, 0x0F, 0x19,
  0x1B, 0x25, 0x27, 0x2D, 0x3F, 0x43, 0x45, 0x49,
  0x4F, 0x55, 0x5D, 0x63, 0x69, 0x7F, 0x81, 0x8B,
  0x93, 0x9D, 0xA3, 0xA9, 0xB1, 0xBD, 0xC1, 0xC7,
  0xCD, 0xCF, 0xD5, 0xE1, 0xEB, 0xFD, 0xFF, 0x03,
  0x09, 0x0B, 0x11, 0x15, 0x17, 0x1B, 0x27, 0x29,
  0x2F, 0x51, 0x57, 0x5D, 0x65, 0x77, 0x81, 0x8F,
  0x93, 0x95, 0x99, 0x9F, 0xA7, 0xAB, 0xAD, 0xB3,
  0xBF, 0xC9, 0xCB, 0xCF, 0xD1, 0xD5, 0xDB, 0xE7,
  0xF3, 0xFB, 0x07, 0x0D, 0x11, 0x17, 0x1F, 0x23,
  0x2B, 0x2F, 0x3D, 0x41, 0x47, 0x49, 0x4D, 0x53 
};

void treyfer_enc (byte text[9], byte key[8]);
void treyfer_dec (byte text[9], byte key[8]);

void setup() {
  Serial.begin(9600);	// Initialize serial communications with the PC
  SPI.begin();		// Init SPI bus

  mfrc522.PCD_Init();	// Init MFRC522 card

}

void beep() {
  tone(3, 540, 80);
  delay(100);
  tone(3, 540, 80);
}

void signal() {
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
  beep();
  
  byte temp[9];
  temp[2] = mfrc522.uid.uidByte[0];
  temp[3] = mfrc522.uid.uidByte[1];
  temp[4] = mfrc522.uid.uidByte[2];
  temp[5] = mfrc522.uid.uidByte[3];
  treyfer_enc(temp, KEY);
  dump("ENC", temp, 8);
  for (int i = 0; i < mfrc522.uid.size; i++) {
    previous_uid[i] = mfrc522.uid.uidByte[i];
  }

  signal();

  lastScanTime = micros();
}

byte rotl(byte x) {
  return (x << 1) | (x >> 7);
}

byte rotr(byte x) {
  return (x >> 1) | (x << 7);
}



void treyfer_enc (byte text[9], byte key[8])
{
  text[0] = random(256);
  text[1] = random(256);
  
  text[6] = random(256);
  text[7] = random(256);
  dump("TEXT", text, 8);
  
  int i;
  byte t;

  t = text[0];
  for (i = 0; i < 8*NUMROUNDS; i++) {
    t += key[i%8];
    t = sbox[t] + text[(i+1)%8];
    text[(i+1) % 8] = t = rotl(t);
  }
}

void dump (char txt[], byte in[], int len) {
  int i;
  Serial.print(txt);
  Serial.print(" ");
  char buffer[50];
  for (i=0; i<len; i++) {
    sprintf(buffer, "%02X", in[i]);
    Serial.print(buffer);
  }
  Serial.println();
}

void treyfer_dec (byte text[9], uint8_t key[8])
{
  int i;
  byte t;

  for (i=(8*NUMROUNDS)-1; i>=0; i--) {
    t = text[(i)%8];
    t += key[i%8];
    text[(i+1) % 8] = rotr(text[(i+1) % 8]);
    text[(i+1) % 8] = text[(i+1) % 8] - sbox[t];
  }
}





