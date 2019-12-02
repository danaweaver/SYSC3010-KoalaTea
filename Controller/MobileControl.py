import json, socket, sys, time, netifaces

class MobileControl:

    """
    Retrieves all the Teas and Alarms for the Mobile Interface
    
    teas - All tea data in Tea table
    alarms - All alarm data in Alarm table
    sock - The Controller socket to send/receive the request/response
    addr - Address of the message that is sent to
    """
    def retrieveTeaInfoAndAlarm(self, teas, alarms, sock, addr):
        jdata = {
            "msgId": 2,
            "teas": teas,
            "alarms": alarms
        }
        self.sendData(jdata, sock, addr)


    """
    Sends the teaId of the added custom tea to the Mobile Interface
    
    teaId - The teaId of the added custom tea
    sock - The Controller socket to send/receive the request/response
    addr - Address of the message that is sent to 
    """
    def addCustomTeaInformation(self, teaId, sock, addr):
        jdata = {
            "msgId": 9,
            "teaId": teaId
        }
        self.sendData(jdata, sock, addr)


    """
    Sends the teaId of the removed custom tea to the Mobile Interface
    
    teaId - The teaId of the added custom tea
    sock - The Controller socket to send/receive the request/response
    addr - Address of the message that is sent to
    """
    def removeCustomTeaInformation(self, teaId, sock, addr):
        jdata = {
            "msgId": 10,
            "teaId": teaId
        }
        self.sendData(jdata, sock, addr)
    
    
    """
    Acknowledge the msgId  4 request from the Mobile Interface

    sock - The Controller socket to send/receive the request/response
    addr - Address of the message that is sent to
    """
    def ackSelect(self, sock, addr):
        jdata = {
            "msgId": 40
        }
        self.sendData(jdata, sock, addr)
        

    """
    Notify the Mobile Interface that the tea brewing process is complete

    sock - The Controller socket to send/receive the request/response
    addr - Address of the message that is sent to
    """
    def notifyUser(self, sock, addr):
        jdata = {
            "msgId": 4
        }
        self.sendData(jdata, sock, addr)

    
    """
    Notifies user that cancel request has been processed

    sock - The Controller socket to send/receive the request/reponse
    addr - Address of the message that is sent to
    """
    def notifyUserCancel(self, sock, addr):
        jdata = {
            "msgId": 13
        }
        self.sendData(jdata,sock, addr)


    """
    Notifies user that an error occured

    sock - The Controller socket to send/receive the request/reponse
    addr - Address of the message that is sent to
    """
    def notifyUserError(self, sock, addr):
        jdata = {
            "msgId": 14
        }
        self.sendData(jdata,sock, addr)


    """
    Send the request to the Mobile Interface and wait for the expected response

    jdata - json message to send to the Mobile Interface
    sock - the controller socket to send to the Mobile Interface
    addr - Address of the message that is sent to
    """
    def sendData(self, jdata, sock, addr):
        data = json.dumps(jdata)
        print("MobileControl sending: " + data)
        sock.sendto(data.encode('utf-8'), addr)