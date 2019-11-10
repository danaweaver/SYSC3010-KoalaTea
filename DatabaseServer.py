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
        receivePort = 1050
        sendPort = 1051
        controllerAddr = ('localhost', receivePort)

        # Initialize database and logger
        connection = DatabaseConnection()
        connection.initDatabase()
        logger = Logger()

    """
    Receive database requests from the Controller to process
    """
    def receiveRequests(self):
        s_receive = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(controller_addr)

        while True:
            print ("Waiting to receive on port %d" % receivePort)
            buf, addr = s.recvfrom(receivePort)
            this.decipherReceivedPacket(buf)

        s.shutdown(1)

    """
    Execute desired actions by examining the received message contents
    """
    def decipherReceivedPacket(self, buf):
        print("Received: " + buf.decode('utf-8'))
        payload = json.loads(buf.decode('utf-8'))
        print("Converted to Python Dictionary: " + str(payload))
        print("\n\n")
        if payload['msgId'] == 3: # Retrieve all teas and alarm information
            logger.logGetTeaInformation()
            logger.logGetAlarmInformation()
            teaInfo = connection.getTeaInformation()
            alarmInfo = connection.getAlarmInformation()
            # Set up return payload

        elif payload['msgId'] == 11: # Add custom tea profile
            logger.logAddCustom()
        elif payload['msgId'] == 12: # Remove custom tea profile
            logger.logRemoveCustom()
        else: # Unexpected message type received - log and ignore
            logger.logUnexpectedMessage()

    """
    Send response message back to the Controller
    """
    def sendRequest(self):
        print("Send request function")

def main():
    dbServer = DatabaseServer()

if __name__ == "__main__":
    main()
