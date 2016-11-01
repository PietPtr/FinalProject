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
const int PRIME_SIZE = 40;
const int MILLER_RABIN_ROUNDS = 10;
byte previous_uid[10];

unsigned long lastScanTime = 0;

bc_num rsaN = NULL;
bc_num rsaP = NULL;
bc_num rsaQ = NULL;
bc_num rsaD = NULL;
bc_num rsaE = NULL;
bc_num zero;
bc_num one;
bc_num two;


int DIGITS = 0;

void print_bignum(bc_num x) {
  char *s=bc_num2str(x);
  Serial.println(s);
  free(s); 
}

void setup() {
  Serial.begin(9600);	// Initialize serial communications with the PC
  SPI.begin();		// Init SPI bus

  mfrc522.PCD_Init();	// Init MFRC522 card
  bc_init_numbers ();     // Init bigNumber liberary
  
  bc_num a=NULL, b = NULL, c = NULL;
  bc_str2num(&rsaE, "65537", DIGITS);
  bc_str2num(&zero, "0",DIGITS);
  bc_str2num(&one, "1",DIGITS);
  bc_str2num(&two, "2",DIGITS);
  
  
  // test multiplication  
  bc_str2num(&a, "41", DIGITS);
  bc_str2num(&b, "18254546", DIGITS);
  bc_multiply(a,b,&c,DIGITS);
  
  if(isPrime(a)){
    Serial.print("prime\n");
  }else{
    Serial.print("not prime\n");
  }  

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

void genBigNum (bc_num num){
  int counter;
  String stringNumber;
  for(counter = 0; counter < PRIME_SIZE-1; counter++){
    stringNumber += String(random(10));
  }
  stringNumber += String(random(5)*2+1);  //last digit odd
  char charnumber[PRIME_SIZE];
  stringNumber.toCharArray(charnumber, PRIME_SIZE);
  bc_str2num(&num, charnumber, DIGITS);
}


bc_num extendedEuclidean(bc_num a, bc_num b){
  bc_num olda = a;
  bc_num oldb = b;
  bc_str2num(&one, "1",DIGITS);
  bc_str2num(&zero, "0",DIGITS);
  bc_num x0 = one, x1 = zero, y0 = zero, y1 = one;
  bc_num q;
  bc_num temp;
  
  while (b != 0){
    
    bc_divide(a, b, &q, DIGITS);
    bc_modulo(a, b, &b, DIGITS); //might need mod function
    a = b;
   
    bc_multiply(q, x1, &temp, DIGITS); 
    bc_sub(x0, temp, &x1, DIGITS);
    //x1 = x0 - temp;
    x0 = x1;
    bc_multiply(q, y1, &temp, DIGITS);
    bc_sub(y0, temp, &y1, DIGITS);
    //y1 = y0 - temp;
    y0 = y1;
  }
  bc_modulo(x0, oldb, &x0, DIGITS);
  //x0 = x0 % oldb;
  return x0;
}

bool tryMillerRabin(bc_num a, bc_num d, bc_num s, bc_num n){
  Serial.print("test\n");
  bc_num temp;
  bc_raisemod(a, d, n, &temp, DIGITS);
  print_bignum(a);
  print_bignum(d);
  print_bignum(n);
  if (bc_compare(temp, one) == 0){
    return false;
  }
  bc_num i;
  bc_str2num(&i, "0",DIGITS);
  print_bignum(n);
  Serial.print("test3\n");
  for(; i < s; bc_add(i, one, &i, DIGITS)){
    Serial.print("test2\n");
    bc_num temp2;
    bc_raise(two, i, &temp, DIGITS);
    bc_multiply(temp, d, &temp, DIGITS);
    bc_sub(n, one, &temp2, DIGITS);
    bc_raisemod(a, temp, n, &temp, DIGITS);
    if(bc_compare(temp, temp2) == 0){
      return false;
    }  
  }
  return true;  
}


bool isPrime(bc_num n) {
  
  if ( n == two){
    return false;
  }
  bc_num mod = NULL;
  bc_modulo(n, two, &mod, DIGITS);
  if( mod == two){
    return false;
  }
  
  bc_num s;
  bc_num one;
  bc_num two;
  bc_num d;
  bc_num temp;
  bc_str2num(&s, "0",DIGITS);
  bc_str2num(&one, "1",DIGITS);
  bc_str2num(&two, "2",DIGITS);
  bc_sub(n, one, &d, DIGITS);
  while (true){
    bc_num quot;
    bc_num remainder;
    bc_divmod(d, two, &quot, &remainder, DIGITS);
    if(bc_compare(remainder, one) == 0){
      break;
    }
    s += 1;
    d = quot;
  }


  for(int i = 0; i < MILLER_RABIN_ROUNDS; i++) {
    bc_num a;
    bc_int2num(&a, random(10000));
    if (tryMillerRabin(a, d, s, n)){
      return false;
    }  
  }    
  return true;
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
