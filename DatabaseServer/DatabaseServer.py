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
        self.databaseAddr = ('172.17.75.4', 1050)
        self.controllerAddr = ('172.17.81.32', 1080) # netifaces.ifaddresses('eth0')[netifaces .AF_INET][0]['addr']
        # Initialize Connection and Logger objects
        self.connection = DatabaseConnection()
        self.logger = Logger()


    """
    Receive database requests from the Controller to process
    """
    def receiveRequests(self):
        self.connection.checkDatabaseState()
        sReceive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sReceive.bind(self.databaseAddr)

        while True:
            print ("Waiting to receive")
            buf, addr = sReceive.recvfrom(1024)
            self.decipherReceivedPacket(buf)

        s.shutdown(1)


    """
    Execute desired actions by examining the received message contents

    buf - Buffer of received message
    """
    def decipherReceivedPacket(self, buf):
        # TODO: remove print below - for testing
        print("Received: " + buf.decode('utf-8'))
        payload = json.loads(buf.decode('utf-8'))
        if "msgId" in payload:
            if payload['msgId'] == 3: # Retrieve all teas and alarm information
                #Logging
                self.logger.logGetTeaInformation()
                self.logger.logGetAlarmInformation()
                # Retrieve information from database
                teaInfo = self.connection.getTeaInformation()
                alarmInfo = self.connection.getAlarmInformation()
                # Response
                responseData = self.getAllInfoResponseFormat(payload["msgId"], teaInfo, alarmInfo)
                self.sendResponse(responseData)
            elif payload["msgId"] == 11: # Adding custom tea profile
                if payload["tea"]["name"] and payload["tea"]["steepTime"] and payload["tea"]["temp"]:
                    self.logger.logAddCustom(payload["tea"]["name"], payload["tea"]["steepTime"], payload["tea"]["temp"])
                    # Adding to database
                    teaId = self.connection.addCustomTeaProfile(payload["tea"]["name"], payload["tea"]["steepTime"], payload["tea"]["temp"])
                    # Reponse Message
                    responseData = self.getAddRemoveProfileResponseFormat(payload["msgId"], teaId)
                    self.sendResponse(responseData)
                else: # Incorrect message format
                    self.logger.logErrorMessage()
            elif payload["msgId"] == 12: # Remove a custom tea profile
                if payload["teaId"]:
                    self.logger.logRemoveCustom(payload["teaId"])
                    # Remove from database
                    teaId = self.connection.removeCustomTeaProfile(payload["teaId"])
                    # Reponse Message
                    responseData = self.getAddRemoveProfileResponseFormat(payload["msgId"], teaId)
                    self.sendResponse(responseData)
                else: # Incorrect message format
                    self.logger.logErrorMessage()
            else: # Unexpected message ID received - log and ignore
                self.logger.logErrorMessage()
        else: # Could not find 'msgId' in payload - log and ignore
            self.logger.logErrorMessage()


    """
    Get response format for retrieve information request

    teas - All tea data in Tea table
    alarms - All alarm data in Alarm table
    """
    def getAllInfoResponseFormat(self, msgId, teas, alarms):
        x = {
                "msgId": msgId,
                "teas": teas,
                "alarms": alarms
            }
        return json.dumps(x)


    """
    Get response format for adding profile request / removing profile request
    """
    def getAddRemoveProfileResponseFormat(self, msgId, teaId):
        x = {
                "msgId": msgId,
                "teaId": teaId
            }
        return json.dumps(x)


    """
    Send response message back to the Controller

    payload - message to add to packet
    """
    def sendResponse(self, payload):
        sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.logger.logSendResponse(payload)
        sendSocket.sendto(payload.encode('utf-8'), self.controllerAddr)


def main():
    dbServer = DatabaseServer()
    dbServer.receiveRequests()

if __name__ == "__main__":
    main()
