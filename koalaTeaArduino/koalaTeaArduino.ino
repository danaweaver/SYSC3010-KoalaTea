#include <OneWire.h>
#include <DallasTemperature.h>
#include <LiquidCrystal.h>
#include <Stepper.h>

#define ONE_WIRE_BUS 2
#define STEPS 2048

// initialize the temperature sensor to pin 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
// initialize the lcd with the pins 3-6, 12, 13
LiquidCrystal lcd(13, 12, 6, 5, 4, 3);
// initialize the stepper motor with pins 8-11
Stepper stepper (STEPS, 8, 10, 9, 11);

String read;
int timer = 0;
int secondsPassed = 0;
bool cancel = false;
bool lowered = false;

void setup() {
  Serial.begin(9600);
  // initialize LED to pin 7
  pinMode(7, OUTPUT);
  stepper.setSpeed(15);
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
    if(data == "tStop" || data == "444") {  // stops temperature reading if received stop or cancel
      if(data == "444") {
        Serial.println("444");  
      }
      return true;
    }
  }
  return false;
}

void loop() {
  cancel = false;
  if(Serial.available() > 0){
    lcd.setCursor(0, 1);  // column 0 of line 1 (2nd row)
    lcd.print("              ");  //clear bottom line
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
      rotation(1);
      delay(1000);
      Serial.println("lowerTea");
    }
    else if(read == "51") {
      delay(1000);
      rotation(0);
      Serial.println("raiseTea"); 
    }
    // timer 
    else if(read.charAt(0) == '6') {
      lcd.setCursor(0, 1);
      lcd.print("Time:");
      timer = read.substring(1).toInt(); // value after the 6 is the time in seconds
      Serial.println(timer);
      secondsPassed = 0;
      unsigned long startTime = millis(); 
      while(timer != 0) {
        lcd.setCursor(7, 1);
        if(Serial.available() > 0) {
          read = Serial.readStringUntil('\n');
          if(read == "444") {
            cancel = true;
            break;  
          }
        }
        if((millis() - startTime) / 1000 > secondsPassed ){
          timer--;
          secondsPassed++;
          Serial.println(timer);
          lcd.print("   ");
          lcd.setCursor(7, 1);
        }
        lcd.print(timer);
      }
      lcd.setCursor(0, 1);
      if(cancel){
        lcd.print("Cancelled");
      }
      else{
        lcd.print("Tea is ready");
        digitalWrite(7, HIGH);  // turn on led to signify finishing
      }
      Serial.println("6Done");  
    }
    // led
    else if(read == "70") {
      digitalWrite(7, LOW);
    }
    // error
    else if(read == "888"){
      lcd.setCursor(0, 1);
      lcd.print("Error occurred");
    }
    // cancel / reset
    if(read == "444" || cancel) {
      if(lowered){  // prevents raising tea when already raised
        rotation(0);
      }
      digitalWrite(7, LOW);
    }
  }
}

void rotation(bool direction){  
  // lower tea bag if 1 raise tea bag if 0
  if (direction) {
    lowered = true;
    stepper.step(2048);
  }
  else {
    lowered = false;
    stepper.step(-2048);
  }
}
