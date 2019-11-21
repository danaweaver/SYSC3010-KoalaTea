#include <OneWire.h>
#include <DallasTemperature.h>
#include <LiquidCrystal.h>
#include <Stepper.h>

#define ONE_WIRE_BUS 2
#define STEPS 32

// initialize the temperature sensor to pin 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
// initialize the lcd with the pins 3-6, 12, 13
LiquidCrystal lcd(13, 12, 6, 5, 4, 3);
// initialize the stepper motor with pins 8-11
Stepper stepper (STEPS, 8, 10, 9, 11);

String read;

void setup() {
  Serial.begin(9600);
  // initialize LED to pin 7
  pinMode(7, OUTPUT);
  stepper.setSpeed(200);
  sensors.begin();
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("KOALATEA");

}

void temperatureRead(){
  sensors.requestTemperatures();
  Serial.println("T" + String(sensors.getTempCByIndex(0))); 
}

bool tempStop() {
  String data;
  if(Serial.available() > 0) {
    data = Serial.readStringUntil('\n');
    if(data == "tStop") {return true;}
  }
  return false;
}

void loop() {
  if(Serial.available() > 0){
    digitalWrite(7, HIGH);  // turn on led
    read = Serial.readStringUntil('\n'); 
    // temperature reading
    if(read == "tStart") {
      while (!tempStop()) {
        temperatureRead();
        delay(2000);
        //if (tempStop()) {break;}
      }
    }
    // lower and raise teabag
    else if(read == "50") {
      //rotation(1);
      delay(1000);
      Serial.println("lowerTea");
    }
    else if(read == "51") {
      delay(1000);
      //rotation(0);
      Serial.println("raiseTea"); 
    }
    // timer 
    else if(read.charAt(0) == '6') {
      lcd.setCursor(0, 1);  // column 0 of line 1 (2nd row)
      lcd.print("Time:");
      lcd.setCursor(7, 1);
      int timer = read.substring(1).toInt(); // value after the 6 is the time in seconds
      int startTime = millis(); 
      while(timer != 0){
        lcd.println(timer - (millis() - startTime / 1000));
        //timer--;
      }
      digitalWrite(7, HIGH);  // turn on led 
      Serial.println("6Done");
    }
  }
}

void rotation(bool direction){  
  // clockwise if 1 counterclockwise if 0
  if (direction) {
    stepper.step(2048);
  }
  else {
    stepper.step(-2048);
  }
}
