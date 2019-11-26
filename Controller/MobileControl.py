import json, socket, sys, time, netifaces

class MobileControl:

    def __init__(self):
        self.mobilePort = 3020
        self.mobileServerAddress = ("192.168.43.57", self.mobilePort)
    

    """
    Retrieves all the Teas and Alarms for the Mobile Interface
    
    teas - All tea data in Tea table
    alarms - All alarm data in Alarm table
    sock - the Controller socket to send/receive the request/response
    """
    def retrieveTeaInfoAndAlarm(self, teas, alarms, sock):
        jdata = {
            "msgId": 2,
            "teas": teas,
            "alarms": alarms
        }
        self.sendData(jdata, sock)


    """
    Sends the teaId of the added custom tea to the Mobile Interface
    
    teaId - The teaId of the added custom tea
    sock - the Controller socket to send/receive the request/response 
    """
    def addCustomTeaInformation(self, teaId, sock):
        jdata = {
            "msgId": 9,
            "teaId": teaId
        }
        self.sendData(jdata, sock)


    """
    Sends the teaId of the removed custom tea to the Mobile Interface
    
    teaId - The teaId of the added custom tea
    sock - the Controller socket to send/receive the request/response
    """
    def removeCustomTeaInformation(self, teaId, sock):
        jdata = {
            "msgId": 10,
            "teaId": teaId
        }
        self.sendData(jdata, sock)
    
    
    """
    Acknowledge the msgId  4 request from the Mobile Interface

    sock - The Controller socket to send/receive the request/response
    """
    def ackSelect(self, sock):
        jdata = {
            "msgId": 40
        }
        self.sendData(jdata, sock)
        

    """
    Notify the Mobile Interface that the tea brewing process is complete

    sock - The Controller socket to send/receive the request/response
    """
    def notifyUser(self, sock):
        jdata = {
            "msgId": 4
        }
        self.sendData(jdata, sock)

    
    """
    Notifies user that cancel request has been processed

    sock - The Controller socket to send/receive the request/reponse
    """
    def notifyUserCancel(self, sock):
        jdata = {
            "msgId": 13
        }
        self.sendData(jdata,sock)


    """
    Notifies user that an error occured

    sock - The Controller socket to send/receive the request/reponse
    """
    def notifyUserError(self, sock):
        jdata = {
            "msgId": 14
        }
        self.sendData(jdata,sock)


    """
    Send the request to the Mobile Interface and wait for the expected response

    jdata - json message to send to the Mobile Interface
    sock - the controller socket to send to the Mobile Interface
    """
    def sendData(self, jdata, sock):
        data = json.dumps(jdata)
        print("MobileControl sending: " + data)
        sock.sendto(data.encode('utf-8'), self.mobileServerAddress)