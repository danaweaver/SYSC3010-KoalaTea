'''
The temperature stub waits for the message "tStart". Once stub has received the message, it will send 
temperature readings starting from room temperature (25°C). After every 3 seconds, the temperature sensor’s
value will increase by 5 degrees until the message "tStop" is received and temperature measurements will stop.
'''

import os, pty, serial, fcntl, time

class TemperatureStub:

    def __init__(self):
        #Create the virtual serial port
        self.masterA, self.slaveA = pty.openpty()
        self.sA_name = os.ttyname(self.slaveA)
        print("Temperature Stub serial: " + self.sA_name)
        self.ser = serial.Serial()
        #set non-blocking flag
        flag = fcntl.fcntl(self.masterA, fcntl.F_GETFL)
        fcntl.fcntl(self.masterA, fcntl.F_SETFL, flag | os.O_NONBLOCK)
    
    '''
    Return slaveA port name
    '''
    def getSerialPort(self):
        return self.sA_name

    '''
    Return set the serial port it will write to

    port - the port the serial will write to
    '''
    def setSerialPort(self, port):
        self.ser = serial.Serial(port)

    '''
    Wait for tStart then start measuring the temperature
    '''
    def listenToStart(self):
        while True:
            try:
                data = os.read(self.masterA,1024).decode('utf-8')
                print("received: " + data)
                if (data == "tStart"):
                    self.measureTemperature()
            except:
                continue
    
    '''
    Simulate the temperature measurement starting at 25 then incrementing  by 3 every 3 seconds
    Once tStop has been received, stop measuring the temperature
    '''
    def measureTemperature(self):
        currentTemp = 25
        while True:
            data = "T" + str(currentTemp)
            self.ser.write(data.encode('utf'))
            currentTemp += 5 #increase temperature by 5
            try:
                #wait 3 seconds and check if the Controller wants to stop measuring the water
                time.sleep(3) 
                data = os.read(self.masterA,1024).decode('utf-8')
                if (data == 'tStop'):
                    break
            except OSError as e:
                print("Current temp = " + str(currentTemp))
        print("Temperature probe has stopped measuring.")

'''
Initialize the temperature stub and wait for the "tStart" message
'''
def main():
    ts = TemperatureStub()
    time.sleep(5) #give time to start the ArduinoControl class
    ts.setSerialPort("/dev/pts/1")
    ts.listenToStart()

if __name__ == "__main__":
    main()