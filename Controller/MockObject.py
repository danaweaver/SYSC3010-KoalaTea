import socket, sys, time, json

#Database Server Socket
sData = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sData.settimeout(20)
dbPort = 1050
dbServer_address = ("localhost", dbPort)
sData.bind(dbServer_address)

#Mobile Interface Socket
sMobile = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sMobile.settimeout(20)
mobilePort = 1060
mobileServerAddress = ("localhost", 1060)
sMobile.bind(mobileServerAddress)

#Controller Address
contPort = 1080
contServer_address = ("localhost", contPort)

#Variables
testOne = {
        "msgId" : 3,
        "teas" : [
            {
                "name": "green tea",
                "time": 13, 
                "temp": 30.0
            },
            {
                "name": "oolong tea",
                "time": 10, 
                "temp": 82.3
            },
        ],
        "alarms" : [
            {
                "name": "Taeyeon",
                "fileLocation": "Girls Generation"
            },
            {
                "name": "BoA",
                "fileLocation": "SMTOWN"
            },
        ]
            
}

testAddRequest = {
    "msgId": 9, 
    "tea": {
        "name": "jasmine tea",
        "time": 50,
        "temp": 79.6
    }
}

testAddRepsonse = {
    "msgId": 11,
    "teaId": 13,
    "status": 1
}

testRemoveRequest = {
    "msgId": 10,
    "teaId": 13
}

testRemoveResponse = {
    "msgId": 12,
    "teaId": 13,
    "status": 1
}

# TestID 1 & 2: 
# Requesting to get the preset teas and alarm for the Mobile Interface
print("Test # 1 & 2: Requesting to get the preset teas and alarm for the Mobile Interface")
print("MB requests preset teas and alarms from CT")
jdata = {"msgId": 2}
data = json.dumps(jdata)
print("Sending: " + data)
sMobile.sendto(data.encode('utf-8'), contServer_address) #MB send CT
print("DB receives the request from CT")
buf, address = sData.recvfrom(1024) #DB receive from CT
print("Received: " + buf.decode('utf-8'))
print("DB sends acknowlegement to CT")
data = json.dumps(testOne)
print("Sending: " + data)
sData.sendto(data.encode('utf-8'), contServer_address) #DB send to CT
print("MB receives the acknowledgement from CT")
buf, address = sMobile.recvfrom(1024)
print("Received: " + buf.decode('utf-8') + "\n\n")

# Test :
# Adding custom tea information
print("Test: Adding custom tea information")
print("MB requesting CT to add custom tea info")
data = json.dumps(testAddRequest)
print("Sending: " + data)
sMobile.sendto(data.encode('utf-8'), contServer_address)
print("DB receives the request from CT")
buf, address = sData.recvfrom(1024)
print("Received: " + buf.decode('utf-8'))
print("DB sends acknowlegement to CT")
data = json.dumps(testAddRepsonse)
print("Sending: " + data)
sData.sendto(data.encode('utf-8'), contServer_address)
print("MB receives the acknowledgement from CT")
buf, address = sMobile.recvfrom(1024)
print("Received: " + buf.decode('utf-8') + "\n\n")

# Test :
# Removing custom tea information
print("Test: Removing custom tea information")
print("MB requesting CT to remove custom tea info")
data = json.dumps(testRemoveRequest)
print("Sending: " + data)
sMobile.sendto(data.encode('utf-8'), contServer_address)
print("DB receives the request from CT")
buf, address = sData.recvfrom(1024)
print("Received: " + buf.decode('utf-8'))
print("DB sends acknowlegement to CT")
data = json.dumps(testRemoveResponse)
print("Sending: " + data)
sData.sendto(data.encode('utf-8'), contServer_address)
print("MB receives the acknowledgement from CT")
buf, address = sMobile.recvfrom(1024)
print("Received: " + buf.decode('utf-8') + "\n\n")

# Clean up
print("Clean up" + "\n\n")
sData.shutdown(1)
sMobile.shutdown(1)