import json
import socket
import sys
import time
from Logger import Logger
from DatabaseConnection import DatabaseConnection

"""
DataServer class receives and processes requests from the Controller and will
send back the corresponding response message
"""
class DatabaseServer:
    def  __init__(self):
        self.receivePort = 1050
        self.controllerAddr = ('localhost', self.receivePort)
        # Initialize database and logger
        self.connection = DatabaseConnection()
        self.logger = Logger()

    """
    Receive database requests from the Controller to process
    """
    def receiveRequests(self):
        self.connection.initDatabase()
        sReceive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sReceive.bind(self.controllerAddr)

        while True:
            print ("Waiting to receive on port %d" % self.receivePort)
            buf, addr = sReceive.recvfrom(self.receivePort)
            self.decipherReceivedPacket(buf)

        s.shutdown(1)

    """
    Execute desired actions by examining the received message contents
    
    buf - Buffer of received message
    """
    def decipherReceivedPacket(self, buf):
        print("Received: " + buf.decode('utf-8'))
        payload = json.loads(buf.decode('utf-8'))
        if payload['msgId'] == 3: # Retrieve all teas and alarm information
            self.logger.logGetTeaInformation()
            self.logger.logGetAlarmInformation()
            teaInfo = self.connection.getTeaInformation()
            alarmInfo = self.connection.getAlarmInformation()
            responseData = self.getAllInfoResponseFormat(teaInfo, alarmInfo)
            self.sendResponse(responseData)
        elif payload["msgId"] == 11: # Add custom tea profile
            self.logger.logAddCustom(payload["name"], payload["time"], payload["temp"])
            self.connection.addCustomTeaProfile(payload["name"], payload["time"], payload["temp"])
            responseData = self.getAddProfileResponseFormat()
            self.sendResponse(responseData)  
        elif payload["msgId"] == 12: # Remove custom tea profile
            self.logger.logRemoveCustom(payload["teaId"])
            self.connection.removeCustomTeaProfile(payload["teaId"])
            responseData = self.getRemoveProfileResponseFormat()
            self.sendResponse(responseData)
        else: # Unexpected message type received - log and ignore
            self.logger.logUnexpectedMessage(payload["msgId"])
    
    """
    Get response format for retrieve information request
    
    teas - All tea data in Tea table
    alarms - All alarm data in Alarm table
    """
    def getAllInfoResponseFormat(self, teas, alarms):
        x = {
                "msgId": 3,
                "teas": teas,
                "alarms": alarms
            }
        return json.dumps(x)
    
    """
    Get response format for adding profile request
    """
    def getAddProfileResponseFormat(self):
        x = {
                "msgId": 11,
                "status": 1
            }
        return json.dumps(x)
    
    """
    Get response format for removing profile request
    """
    def getRemoveProfileResponseFormat(self):
        x = {
                "msgId": 12,
                "status": 1
            }
        return json.dumps(x)

    """
    Send response message back to the Controller
    
    payload - message to add to packet
    """
    def sendResponse(self, payload):
        sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.logger.logSendResponse(payload)
        sendSocket.sendto(payload.encode('utf-8'), ('localhost', 1051))

def main():
    dbServer = DatabaseServer()
    dbServer.receiveRequests()

if __name__ == "__main__":
    main()
