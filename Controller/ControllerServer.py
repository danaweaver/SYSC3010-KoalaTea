import json
import socket
import sys
import time
from Controller.ArduinoControl import ArduinoControl
from Controller.DatabaseControl import DatabaseControl
from Controller.MobileControl import MobileControl
from Controller.SpeakerControl import SpeakerControl
from Controller.SwitchControl import SwitchControl

class ControllerServer:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serverPort = 1080
        self.server_address = ("localhost", self.serverPort)
        self.cancel = False
        # Initializa the control objects
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
            buf, addr = self.s.recvfrom(self.serverPort)

            # print("Received: " + buf.decode('utf-8'))
            # data = "ACK: " + buf.decode('utf-8')
            # self.s.sendto(data.encode('utf-8'), addr)

            self.decipherReceivedPacket(buf)

    def decipherReceivedPacket(self, buf):
        print("Received: " + buf.decode('utf-8'))
        payload = json.loads(buf.decode('utf-8'))
        if payload['msgId'] == 2: # Mobile requests preset tea and alarms
            responseData = self.databaseControl.getTeaAlarmInformation() #get tea and alarm from Database
            data = json.loads(responseData.decode('utf-8'))
            self.mobileControl.retrieveTeaInfoAndAlarm(data['teas'], data['alarms'])

def main():
    print("Starting ControllerServer")
    controller = ControllerServer()
    controller.receiveRequests()

if __name__ == "__main__":
    main()

         