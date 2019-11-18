import json, socket, sys, time, netifaces

class DatabaseControl:

    def __init__(self):
        self.dbPort = 1050
        self.dbServerAddress = ("localhost", 1050) #netifaces.ifaddresses('eth0')[netifaces .AF_INET][0]['addr']
    
    """
    Retrieves all the Teas and Alarms from the Database Server 
    
    sock - the Controller socket to send/receive the request/response
    return - the retrieves teas and alarms
    """
    def getTeaAlarmInformation(self, sock):
        #should I do checks of the msgId when receiving from the DB?
        jdata = {"msgId": 3}
        return self.sendReceive(jdata, sock)


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
        return self.sendReceive(jdata, sock)


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
        return self.sendReceive(jdata, sock)


    """
    Send the request to the Database Server and wait for the expected response

    jdata - json message to send to the Database
    sock - the controller socket to send to the Database
    """
    def sendReceive(self, jdata, sock):
        data = json.dumps(jdata)
        print("DatabaseControl sending: " + data)
        sock.sendto(data.encode('utf-8'), self.dbServerAddress)
        buf, address = sock.recvfrom(1024)
        response = buf.decode('utf-8')
        print("DatabaseControl received: " + response)
        return response