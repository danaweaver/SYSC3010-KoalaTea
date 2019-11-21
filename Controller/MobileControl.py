import json, socket, sys, time, netifaces

class MobileControl:

    def __init__(self):
        self.mobilePort = 1060
        self.mobileServerAddress = ("localhost", 3020) #netifaces.ifaddresses('wlan0')[netifaces .AF_INET][0]['addr']


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
        self.sendData(jdata, sock)


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
        self.sendData(jdata, sock)


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
        self.sendData(jdata, sock)


    """
    Notifies user that cancel request has been processed
    sock - The Controller socket to send/receive the request/reponse
    """
    def notifyUserCanceL(self, sock):
        jdata = {
            "msgId": 13
        }
        self.sendData(jdata,sock) # NOTE: Right now we're sending back the cancel response on the normal socket, don't know if thats what we wants


    """
    Send the request to the Mobile Interface and wait for the expected response

    jdata - json message to send to the Mobile Interface
    sock - the controller socket to send to the Mobile Interface
    """
    def sendData(self, jdata, sock):
        data = json.dumps(jdata)
        print("MobileControl sending: " + data)
        sock.sendto(data.encode('utf-8'), self.mobileServerAddress)
