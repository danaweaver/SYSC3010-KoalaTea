import json, socket, sys, time
from ArduinoControl import ArduinoControl
from DatabaseControl import DatabaseControl
from MobileControl import MobileControl
from SpeakerControl import SpeakerControl
from SwitchControl import SwitchControl

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# serverPort = 1080

class ControllerServer:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(20) #TODO: need to remove this
        self.serverPort = 1080
        self.server_address = ("localhost", self.serverPort)
        self.cancel = False
        # Initialize the control objects
        self.arduinoControl = ArduinoControl()
        self.databaseControl = DatabaseControl()
        self.mobileControl = MobileControl()
        self.speakerControl = SpeakerControl()
        self.switchControl = SwitchControl()


    """
    Receive Controller requests from the other processes to process
    """
    def receiveRequests(self):
        self.s.bind(self.server_address)

        while True:
            print("Waiting to receive on port %d" % self.serverPort)
            buf, addr = self.s.recvfrom(1024)

            # print("Received: " + buf.decode('utf-8'))
            # data = "ACK: " + buf.decode('utf-8')
            # self.s.sendto(data.encode('utf-8'), addr)

            self.decipherReceivedPacket(buf)


    """
    Execute desired actions by examining the received message contents
    
    buf - Buffer of received message
    """
    def decipherReceivedPacket(self, buf):
        print("Received: " + buf.decode('utf-8'))
        payload = json.loads(buf.decode('utf-8'))
        if payload['msgId'] == 2: # Mobile requests preset tea and alarms
            responseData = self.databaseControl.getTeaAlarmInformation(self.s) #get tea and alarm from Database
            data = json.loads(responseData)
            self.mobileControl.retrieveTeaInfoAndAlarm(data['teas'], data['alarms'], self.s) #send tea and alarm to Mobile
        elif payload['msgId'] == 4: # Mobile selected a specified tea and alarm
            self.startTeaProcess(payload['tea'], payload['alarm'])
        elif payload['msgId'] == 8: # Mobile acknowledges that the tea is ready
            self.reset
        elif payload['msgId'] == 9: # Mobile request to add custom tea information
            responseData = self.databaseControl.addCustomTeaInformation(payload['tea']['name'], payload['tea']['time'], payload['tea']['temp'], self.s)
            data = json.loads(responseData)
            self.mobileControl.addCustomTeaInformation(data['teaId'], data['status'], self.s)
        elif payload['msgId'] == 10: # Mobile request to remove custom tea information
            responseData = self.databaseControl.removeCustomTeaInformation(payload['teaId'], self.s)
            data = json.loads(responseData)
            self.mobileControl.removeCustomTeaInformation(data['teaId'], data['status'], self.s)


    """
    Execute the sequential actions for the brewing tea process
    
    tea - the specified tea
    alarm - the specified alarm
    """
    def startTeaProcess(self, tea, alarm):
        self.switchControl.turnOnKettle
        self.arduinoControl.measureWater(tea['temp'])
        self.switchControl.turnOffKettle
        self.arduinoControl.lowerTeaBag
        self.arduinoControl.displayTimer(tea['steepTime'])
        self.arduinoControl.raiseTeaBag
        self.speakerControl.playAlarm(alarm['fileLocation'])
        self.mobileControl.notifyUser
        self.reset


    """
    Reset the process (ie. turn off the LED and stop the alarm)
    """
    def reset(self):
        self.arduinoControl.turnOffLED
        self.speakerControl.stopAlarm



def main():
    print("Starting ControllerServer")
    controller = ControllerServer()
    controller.receiveRequests()

if __name__ == "__main__":
    main()

         