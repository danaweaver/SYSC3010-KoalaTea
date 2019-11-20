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

int timer, startTime;
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

void loop() {
  if(Serial.available()){
    read = Serial.readString();  
    // temperature reading
    if(read == "tStart") {
      while(read != "tStop"){
        temperatureRead();
        delay(1000); //wait one second before rereading
        if(Serial.available()){
          read = Serial.readString();
        }
      }
    }
    // lower and raise teabag
    else if(read == "50") {
      rotation(1);
      Serial.print("lowerTea");
    }
    else if(read == "51") {
      rotation(0);
      Serial.print("raiseTea");
    }
    // timer 
    else if(read.charAt(0) == '6') {
      lcd.setCursor(0, 1);  // column 0 of line 1 (2nd row)
      lcd.print("Time:");
      lcd.setCursor(7, 1);
      timer = read.substring(1).toInt(); // value after the 6 is the time in seconds
      startTime = millis(); 
      while(timer != 0){
        lcd.print(timer - (millis() - startTime / 1000));
        timer--;
      }
      digitalWrite(7, HIGH);  // turn on led 
      Serial.print("6Done");
    }
  }
}

void temperatureRead(){
  sensors.requestTemperatures();
  Serial.println(sensors.getTempCByIndex(0)); 
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
