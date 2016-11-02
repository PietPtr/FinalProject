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
const int MILLER_RABIN_ROUNDS = 40;

byte previous_uid[10];

unsigned long lastScanTime = 0;

bc_num rsaN = NULL;
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
  
  bc_str2num(&rsaE, "17", DIGITS);
  bc_str2num(&zero, "0",DIGITS);
  bc_str2num(&one, "1",DIGITS);
  bc_str2num(&two, "2",DIGITS);
  
  char number[PRIME_SIZE];
  number[0] = '\0';
  while(number[0] == '\0'){
    Serial.println("KEY PLEASE ");
    Serial.readString().toCharArray(number, PRIME_SIZE);
    delay(100);
  }
  Serial.println("GOT KEY START SCANNING");
  bc_str2num(&rsaN, number, DIGITS);
  print_bignum(rsaN);
  //bc_str2num(&rsaN, "12", DIGITS);
  //genKey();
}

void beep() {
  tone(3, 540, 80);
  delay(100);
  tone(3, 540, 80);
}

bc_num genBigNum (bc_num num){
  int counter;
  char stringNumber[PRIME_SIZE+1];
  for(counter = 0; counter < PRIME_SIZE-1; counter++){
    stringNumber[counter]= random(10)+'0';
  }
  stringNumber[PRIME_SIZE-1] = random(4)*2+'1';  //last digit odd
  stringNumber[PRIME_SIZE]= '\0';
  
  bc_str2num(&num, stringNumber, DIGITS);
  print_bignum(num);
  return num;
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
  for(; i < s; bc_add(i, one, &i, DIGITS)){
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
  if (bc_compare(n, two) == 0){
    return false;
  }
  bc_num remainder;
  bc_modulo(n, two, &remainder, DIGITS);
  if(bc_compare(remainder, two) == 0){
    return false;
  }
  bc_num s;
  bc_num d;
  bc_num temp;
  bc_str2num(&s, "0",DIGITS);
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



bc_num genPrime(){
   bc_num test;
   Serial.println("test next number");
   genBigNum(test);
   Serial.println("generated it");
   while(!isPrime(test)){
     Serial.println("test next prime");
     genBigNum(test);
   }
   Serial.print("PRIME!!!");
   return test;
}

void genKey(){
  bc_num test;
  test = genPrime();
  if(isPrime(test)){
    Serial.print("prime");
  }else{
    Serial.print("not prime");
  }  
}

void encrypt(unsigned long al, unsigned long bl, unsigned long cl, unsigned long dl){
  bc_num prepadding;
  bc_num postpadding;
  bc_num temp1;
  bc_num temp2;
  bc_num power;
  
  bc_num a;
  bc_num b;
  bc_num c;
  bc_num d;
  
  /*
  unsigned long modulusN = a * (2L << 24) + b * (2L << 16) + c * (2L << 8) + d;
  Serial.println(a);
  Serial.println(a * (2L << 24));
  Serial.println(b);
  Serial.println(b * (2L << 16));
  Serial.println(c);
  Serial.println(c * (2L << 8));
  Serial.println(d);
  Serial.println(modulusN);
  */
  bc_num n;
  
  int pre = random(256);
  int post = random(256);
  
  bc_int2num(&prepadding, pre);
  bc_int2num(&postpadding, post);
  
  bc_int2num(&a, al);
  bc_int2num(&b, bl);
  bc_int2num(&c, cl);
  bc_int2num(&d, dl);
  
  bc_str2num(&temp1, "256", DIGITS);
  bc_multiply(a, temp1, &a, DIGITS);
  
  bc_multiply(b, temp1, &b, DIGITS);
  bc_multiply(b, temp1, &b, DIGITS);
  
  bc_multiply(c, temp1, &c, DIGITS);
  bc_multiply(c, temp1, &c, DIGITS);
  bc_multiply(c, temp1, &c, DIGITS);

  bc_multiply(d, temp1, &d, DIGITS);
  bc_multiply(d, temp1, &d, DIGITS);
  bc_multiply(d, temp1, &d, DIGITS);
  bc_multiply(d, temp1, &d, DIGITS);
  
  bc_add(a, b, &b, DIGITS);
  bc_add(b, c, &c, DIGITS);
  bc_add(c, d, &n, DIGITS);
  
  print_bignum(n);
  
  bc_str2num(&temp2, "5", DIGITS);
  bc_raise(temp1, temp2, &power, DIGITS);
  bc_multiply(prepadding, power, &temp1, DIGITS);
  
  print_bignum(temp1);
  
  bc_add(temp1, n, &prepadding, DIGITS);
  
  print_bignum(prepadding);
  
  bc_add(postpadding, prepadding, &n, DIGITS);
  
  print_bignum(n);
  
  bc_raisemod(rsaE, n, rsaN, &temp1, DIGITS);
  
  Serial.print ("ENC ");
  print_bignum(temp1);
  
  
  free(prepadding);
  free(postpadding);
  free(temp1);
  free(temp2);
  free(n);
  
  free(a);
  free(b);
  free(c);
  free(d);
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


  encrypt(mfrc522.uid.uidByte[0], mfrc522.uid.uidByte[1], mfrc522.uid.uidByte[2], mfrc522.uid.uidByte[3]);

  for (int i = 0; i < mfrc522.uid.size; i++) {
    previous_uid[i] = mfrc522.uid.uidByte[i];
  }

  beep();

  lastScanTime = micros();
}
