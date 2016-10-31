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
#include "BigNumber.h"
#include "number.h"
//http://www.gammon.com.au/Arduino/BigNumber.zip

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);	// Create MFRC522 instance.

byte previous_uid[10];

unsigned long lastScanTime = 0;

bc_num rsaN = NULL;
bc_num rsaP = NULL;
bc_num rsaQ = NULL;
bc_num rsaD = NULL;
bc_num rsaE = NULL;
bc_num two = NULL;


int DIGITS = 0;

void print_bignum(bc_num x) {
  char *s=bc_num2str(x);
  Serial.println (s);
  free(s); 
}

void setup() {
  Serial.begin(9600);	// Initialize serial communications with the PC
  SPI.begin();			// Init SPI bus
  mfrc522.PCD_Init();	// Init MFRC522 card
  bc_init_numbers ();     // Init bigNumber liberary
  
  bc_num a=NULL, b = NULL, c = NULL;
  bc_str2num(&rsaE, "65537", DIGITS);
  bc_str2num(&two, "2",DIGITS);
  
  // test multiplication  
  bc_str2num(&a, "41", DIGITS);
  bc_str2num(&b, "18254546", DIGITS);
  bc_multiply(a,b,&c,DIGITS);
  
  isPrime(a);
  // get results as string
  print_bignum (c);
  
  bc_free_num (&b);
  bc_free_num (&c);

}

void beep() {
  tone(3, 540, 80);
  delay(100);
  tone(3, 540, 80);
}

void genBigNum (bn_num num, int s){
  int counter;
  stringNUmber = "";
  for(counter = 0; counter < s; counter++){
    stringNumber += random(10).toString();
  }
  bc_str2num(&num, stringNumber, DIGITS);
}


bn_num extendedEuclidean(bn_num a, bn_num b){
  bn_num olda = a;
  bn_num oldb = b;
  bn_num x0 = 1, x1 = 0; y0 = 0; y1 = 1;
  while (b != 0){
    
    q = a / b;
    b = a % b; //might need mod function
    a = b;
   
    x1 = x0 - q * x1;
    x0 = x1;
    y1 = y0 - q * y1;
    y0 = y1;
  }
  x0 = x0 % oldb;
  y0 = y0 % olda;
  return a, x0, y0 //yeah get creative bitch, only need x0 probs
}


bool isPrime(bc_num test) {
  
  if ( test == two){
    return false;
  }
  bc_num mod = NULL;
  bc_modulo(test, two, &mod, DIGITS);
  if( mod == two){
    return false;
  }
  
  
  //TODO: add miller rabin test
    a.powMod(power, mod);
  //print_bignum(mod);
}  

void genPrime() {
   
}

void genKey(){
  
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
