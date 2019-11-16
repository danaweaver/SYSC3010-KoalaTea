import json, socket, sys, time

class MobileControl:

    def __init__(self):
        self.mobilePort = 1060
        self.mobileServerAddress = ("localhost", 1060)
    

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
        data = json.dumps(jdata)
        sock.sendto(data.encode('utf-8'), self.mobileServerAddress)


    """
    Sends the teaId and status of the added custom tea to the Mobile Interface
    
    teaId - The teaId of the added custom tea
    status - The success/failure status of the request
    sock - the Controller socket to send/receive the request/response 
    """
    def addCustomTeaInformation(self, teaId, status, sock):
        jdata = {
            "msgId": 9,
            "teaId": teaId,
            "status": status
        }
        data = json.dumps(jdata)
        sock.sendto(data.encode('utf-8'), self.mobileServerAddress)


    """
    Sends the teaId and status of the removed custom tea to the Mobile Interface
    
    teaId - The teaId of the added custom tea
    status - The success/failure status of the request
    sock - the Controller socket to send/receive the request/response
    """
    def removeCustomTeaInformation(self, teaId, status, sock):
        jdata = {
            "msgId": 10,
            "teaId": teaId,
            "status": status
        }
        data = json.dumps(jdata)
        sock.sendto(data.encode('utf-8'), self.mobileServerAddress)
    

    """
    Notify the Mobile Interface that the tea brewing process is complete

    status - The success/failure status of the request
    sock - The Controller socket to send/receive the request/response
    """
    def notifyUser(self, status, sock):
        jdata = {
            "msgId": 4,
            "status": status
        }
        data = json.dumps(jdata)
        sock.sendto(data.encode('utf-8'), self.mobileServerAddress)
