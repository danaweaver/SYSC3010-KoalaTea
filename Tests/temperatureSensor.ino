#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into pin 2 on the Arduino
#define ONE_WIRE_BUS 2
// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);
// Pass oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

void setup(void)
{
  Serial.begin(9600); // Begin serial communication
  Serial.println("Arduino Digital Temperature // Serial Monitor Version"); //Print a message
  sensors.begin();
}

void loop(void)
{ 
  sensors.requestTemperatures();  // Send the command to get temperatures
  Serial.print("Temperature is: ");
  Serial.println(sensors.getTempCByIndex(0));
  delay(1000);  // Update value every 1 sec.
}
