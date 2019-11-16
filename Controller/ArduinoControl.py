import json, socket, sys, time, serial

class ArduinoControl:

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        self.ser.open()
    
    def measureWater(self, temp):
        self.ser.write("tStart".encode('utf-8'))
        while True:
            data = ser.readline()
            measTemp = float(data.split("T")[1])
            if measTemp >= temp:
                break
        self.stopTemperature()
    
    def stopTemperature(self):
        self.ser.write("tStop".encode('utf-8'))
    
    def lowerTeaBag(self):
        self.sendReceive("50", "lowerTea")

    def raiseTeaBag(self):
        self.sendReceive("51", "raiseTea")

    def displayTimer(self, time):
        self.sendReceive("6" + str(time), "6Done")
    
    def stopTimer(self):
        self.ser.write("6Stop".encode('utf-8'))

    def turnOnLED(self):
        self.ser.write("71".encode('utf-8'))

    def turnOffLED(self):
        self.ser.write("70".encode('utf-8'))

    def reset(self):
        self.stopTemperature()
        self.raiseTeaBag()
        self.stopTimer()
        self.turnOffLED()

    def sendReceive(self, send, response):
        self.ser.write(send.encode('utf-8'))
        while True:
            data = ser.readline()
            if(data == response):
                break