import json, socket, sys, time, serial

class ArduinoControl:

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
    

    """
    Request the Arduino to measure the temperature of the water water to the specified temperature
    
    temp - specified temperature (float)
    """
    def measureWater(self, temp):
        print("ArduinoControl sending tStart")
        self.ser.write("tStart".encode('utf-8'))
        while True:
            data = ser.readline().decode('utf-8').strip('\r\n')
            print("ArduinoControl received " + data)
            measTemp = float(data.split("T")[1])
            if measTemp >= temp:
                break
        self.stopTemperature()
    

    """
    Request the Arduino to stop the measuring the temperature of the water
    """
    def stopTemperature(self):
        print("ArduinoControl sending tStop")
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
        print("ArduinoControl sending 6Stop")
        self.ser.write("6Stop".encode('utf-8'))


    """
    Request the Arduino to turn on the LED
    """
    def turnOnLED(self):
        print("ArduinoControl sending 71")
        self.ser.write("71".encode('utf-8'))


    """
    Request the Arduino to turn off the LED
    """
    def turnOffLED(self):
        print("ArduinoControl sending 70")
        self.ser.write("70".encode('utf-8'))


    """
    Request the Arduino to reset the IO devices to its original state 
    (ie. stop the temperature measurement, raise the teabag, stop the timer, turn off the LED)
    """
    def reset(self):
        print("ArduinoControl sending 444")
        self.ser.write("444".encode('utf-8'))


    """
    Notify the Arduino that an error had occur in the system
    """
    def error(self):
        print("ArduinoControl sending 888")
        self.ser.write("888".encode('utf-8'))


    """
    Send the request to the Arduino and wait for the expected response
    
    send - message to send to the Arduino (string)
    response - the expected message from the Arduino (string)
    """
    def sendReceive(self, send, response):
        print("ArduinoControl sending " + send.encode('utf-8'))
        self.ser.write(send.encode('utf-8'))
        while True:
            data = ser.readline().decode('utf-8').strip('\r\n')
            print("ArduinoControl received " + data)
            if(data == response):
                break