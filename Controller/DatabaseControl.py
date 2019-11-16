import json, socket, sys, time

class DatabaseControl:

    def __init__(self):
        self.dbPort = 1050
        self.dbServerAddress = ("localhost", 1050)
    
    """
    Retrieves all the Teas and Alarms from the Database Server 
    
    sock - the Controller socket to send/receive the request/response
    return - the retrieves teas and alarms
    """
    def getTeaAlarmInformation(self, sock):
        #should I do checks of the msgId when receiving from the DB?
        #send message to database with msgId = 3
        jdata = {"msgId": 3}
        data = json.dumps(jdata)
        sock.sendto(data.encode('utf-8'), self.dbServerAddress)
        #receive the teas and alarms from the database
        buf, address = sock.recvfrom(1024)
        return buf.decode('utf-8')


    """
    Add a custom tea to the Database Server 
    
    name - name of the custom tea
    time - custom steep time
    temp - custom temperature
    sock - the Controller socket to send/receive the request/response
    return - the response from the Database Server
    """
    def addCustomTeaInformation(self, name, time, temp, sock):
        jdata = {
            "msgId": 11,
            "tea": {
                "name": name,
                "time": time,
                "temp": temp
            }
        }
        data = json.dumps(jdata)
        sock.sendto(data.encode('utf-8'), self.dbServerAddress)
        buf, address = sock.recvfrom(1024)
        return buf.decode('utf-8')


    """
    Remove specified custom tea to the Database Server 
    
    teaId - unique ID of the tea that is being removed
    sock - the Controller socket to send/receive the request/response
    return - the response from the Database Server
    """
    def removeCustomTeaInformation(self, teaID, sock):
        jdata = {
            "msgId": 12,
            "teaId": teaID
        }
        data = json.dumps(jdata)
        sock.sendto(data.encode('utf-8'), self.dbServerAddress)
        buf, address = sock.recvfrom(1024)
        return buf.decode('utf-8')

    # def sendReceive(self, data, sock):
    #     sock.sendto(data.encode('utf-8'), self.dbServerAddress)
    #     buf, address = sock.recvfrom(1024)
    #     return buf.decode('utf-8')