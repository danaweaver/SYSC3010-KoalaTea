import json, socket, sys, time, netifaces

class DatabaseControl:

    def __init__(self):
        self.dbPort = 1050
        self.dbServerAddress = ("10.0.0.22", 1050)
    
    """
    Retrieves all the Teas and Alarms from the Database Server 
    
    sock - the Controller socket to send/receive the request/response
    return - the retrieves teas and alarms
    """
    def getTeaAlarmInformation(self, sock):
        jdata = {"msgId": 3}
        return self.sendReceive(jdata, 3, sock)


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
                "steepTime": time,
                "temp": temp
            }
        }
        return self.sendReceive(jdata, 11, sock)


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
        return self.sendReceive(jdata, 12, sock)


    """
    Send the request to the Database Server and wait for the expected response

    jdata - json message to send to the Database
    expMsgId - the expected msgId received from the Database
    sock - the controller socket to send to the Database
    """
    def sendReceive(self, jdata, expMsgId, sock):
        sock.settimeout(5) #Set socket timeout for socket to check from dropped packets from the Database
        repeat = 0
        while repeat < 2: #Will send to the Database a max of 2 times
            data = json.dumps(jdata)
            print("DatabaseControl sending: " + data)
            sock.sendto(data.encode('utf-8'), self.dbServerAddress)
            try: 
                buf, address = sock.recvfrom(1024)
                response = buf.decode('utf-8')
                print("DatabaseControl received: " + response)
                actMsgId = json.loads(response)['msgId']
                if actMsgId == expMsgId:
                    sock.settimeout(None) #reset socket timeout
                    return response
                else:
                    print("Attempt #" + str(repeat + 1) + ": Recieved an unexpected msgId. Expected: " + str(expMsgId) + ". Actual: " + str(actMsgId) + ".")
            except socket.timeout:
                print("Attempt #" + str(repeat + 1) + ": Socket timeout out after 5 seconds while waiting for a response from the Database Server.")
            repeat += 1
        #If come out here, sendReceive has failed
        print("Failed to send/receive data to/from the Database.")
        sock.settimeout(None) #reset socket timeout
        return False