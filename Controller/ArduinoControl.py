import json, socket, sys, time, serial

class ArduinoControl:

    def __init__(self):
        self.ser = serial.Serial()
        # self.ser = serial.Serial('/dev/ttyACM0', 9600)
        # self.ser.open()
    

    """
    Request the Arduino to measure the temperature of the water water to the specified temperature
    
    temp - specified temperature (float)
    """
    def measureWater(self, temp):
        self.ser.write("tStart".encode('utf-8'))
        while True:
            data = ser.readline()
            measTemp = float(data.split("T")[1])
            if measTemp >= temp:
                break
        self.stopTemperature()
    

    """
    Request the Arduino to stop the measuring the temperature of the water
    """
    def stopTemperature(self):
        self.ser.write("tStop".encode('utf-8'))
    

    """
    Request the Arduino to lower the tea bag
    """
    def lowerTeaBag(self):
        self.sendReceive("50", "lowerTea")


    """
    Request the Arduino to raise the tea bag
    """
    def raiseTeaBag(self):
        self.sendReceive("51", "raiseTea")


    """
    Request the Arduino to start and display the timer to the LCD display

    time - the specified time in seconds (int)
    """
    def displayTimer(self, time):
        self.sendReceive("6" + str(time), "6Done")
    

    """
    Request the Arduino to stop the timer
    """
    def stopTimer(self):
        self.ser.write("6Stop".encode('utf-8'))


    """
    Request the Arduino to turn on the LED
    """
    def turnOnLED(self):
        self.ser.write("71".encode('utf-8'))


    """
    Request the Arduino to turn off the LED
    """
    def turnOffLED(self):
        self.ser.write("70".encode('utf-8'))


    """
    Reset the devices on the Arduino to its original state
    """
    def reset(self):
        self.stopTemperature()
        self.raiseTeaBag()
        self.stopTimer()
        self.turnOffLED()


    """
    Send the request to the Arduino and wait for the expected response

    send - message to send to the Arduino (string)
    response - the expected message from the Arduino (string)
    """
    def sendReceive(self, send, response):
        self.ser.write(send.encode('utf-8'))
        while True:
            data = ser.readline()
            if(data == response):
                break