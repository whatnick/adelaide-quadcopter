/*
  Physical Pixel
 
 An example of using the Arduino board to receive data from the 
 computer.  In this case, the Arduino boards turns on an LED when
 it receives the character 'H', and turns off the LED when it
 receives the character 'L'.
 
 The data can be sent from the Arduino serial monitor, or another
 program like Processing (see code below), Flash (via a serial-net
 proxy), PD, or Max/MSP.
 
 The circuit:
 * LED connected from digital pin 13 to ground
 
 created 2006
 by David A. Mellis
 modified 14 Apr 2009
 by Tom Igoe and Scott Fitzgerald
 
 http://www.arduino.cc/en/Tutorial/PhysicalPixel
 */
#include <Wire.h>

const int escPin[4] = {10,11,12,13}; // the pins that the ESCs is attached to
int incomingByte;      // a variable to read incoming serial data into
unsigned long previousMicros = 0; //Counter to blink LED
unsigned long period = 20000;    // total cycle time (microseconds)
const unsigned long minontime = 1000;
unsigned long ontime[4] = {minontime,minontime,minontime,minontime};    // ontime (postitive pulse min 1ms max 2ms)

int ledState[4] = {LOW,LOW,LOW,LOW}; //ledState
int motorChoice = 0; //Motor whose timing is being set

void setup() {
  // Wire.begin(5);                // join i2c bus with address #5
  // Wire.onReceive(receiveEvent); // register event
  // initialize serial communication:
  Serial.begin(115200);
  // initialize the ESC pins as an output:
  pinMode(escPin[0], OUTPUT);
  pinMode(escPin[1], OUTPUT);
  pinMode(escPin[2], OUTPUT);
  pinMode(escPin[3], OUTPUT);
}


void toggle(char motor)
{
   if (micros() - previousMicros > ontime[motor]) {
      // if the LED is on turn in off
      if(ledState[motor] == HIGH)
      {
        ledState[motor] = LOW;
        // set the LED with the ledState of the variable:
        digitalWrite(escPin[motor], ledState[motor]);
      }
  }
}


  
    //  Serial.println('2'); 
  //while (1 < Serial.available())
  //{
  //    char c = Serial.read();
  //}
  



void readSerial()
{
  if(Serial.available()>0)
  {
    int c = Serial.read();       
    if(c==0)
    {
      ontime[0] = minontime+c*4;
      ontime[1] = minontime+c*4;
      ontime[2] = minontime+c*4;
      ontime[3] = minontime+c*4;
    }
    else if(c<=250)
    {
      ontime[motorChoice] = minontime+c*4;    // receive byte as an integer
    }
    else
    {
      motorChoice = c-251;
    }
  } 
}

void loop() {
  

  
  if (micros() - previousMicros > period) {
      // Reset for period 
      previousMicros = micros();   
      ledState[0] = HIGH;
      ledState[1] = HIGH;
      ledState[2] = HIGH;
      ledState[3] = HIGH;
      // set the LED with the ledState of the variable:
      digitalWrite(escPin[0], HIGH);
      digitalWrite(escPin[1], HIGH);
      digitalWrite(escPin[2], HIGH);
      digitalWrite(escPin[3], HIGH);
     
  }
  
  
  readSerial();
   
  toggle(0);
  //toggle(1);
  toggle(2);
  //toggle(3);
}



// function that executes whenever data is received from master
// this function is registered as an event, see setup()
/*
void receiveEvent(int howMany)
{
  while(1 < Wire.available()) // loop through all but the last
  {
    char c = Wire.receive(); // receive byte as a character
    //Serial.print(c);         // print the character
  }
  int c = Wire.receive();
  //Serial.println(c); 
  
  if(c==0)
  {
    ontime[0] = minontime+c*4;
    ontime[1] = minontime+c*4;
    ontime[2] = minontime+c*4;
    ontime[3] = minontime+c*4;
  //  Serial.println(minontime);
  }
  else if(c<=250)
  {
    ontime[motorChoice] = minontime+c*4;    // receive byte as an integer
   // Serial.println(ontime[motorChoice]);
  }
  else
  {
    motorChoice = c-251;
    //Serial.println(motorChoice);
  }
  
}
*/
