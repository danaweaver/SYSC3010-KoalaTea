import socket, sys, time, json, netifaces, serial, pty, os

#Arduino Serial Port
masterC, slaveC = pty.openpty()
print("ArduinoControl serial: " + os.ttyname(slaveC))
ser = serial.Serial('/dev/pts/0')

#Database Server Socket
sData = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sData.settimeout(20)
dbPort = 1050
dbServer_address = ("localhost", dbPort) #10.0.0.23
sData.bind(dbServer_address)

#Mobile Interface Socket
sMobile = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sMobile.settimeout(20)
mobilePort = 3020
mobileServerAddress = ("localhost", 1060) #10.0.0.23
sMobile.bind(mobileServerAddress)

#Controller Address
contPort = 1080
contServer_address = ("localhost", contPort) #10.0.0.21

#Variables
testPreset = {
        "msgId" : 3,
        "teas" : [
            {
                "name": "green tea",
                "steepTime": 13, 
                "temp": 30.0
            },
            {
                "name": "oolong tea",
                "steepTime": 10, 
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
        "steepTime": 50,
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

testSelectTeaAlarm = {
    "msgId": 4,
    "tea": {
        "name": "Oolong",
        "steepTime": 300,
        "temp": 90.13
    },
    "alarm": {
        "name": "SNSD - Gee",
        "fileLocation": "C:/Desktop/SNSDGee.mp3"
    }
}

testAckNotification = {
    "msgId": 8
}

def checkTest(actual, expected):
    if (actual == expected):
        return "Pass"
    print("Expected: " + str(expected) + " | Actual: " + str(actual))
    return "Fail"

# TestID 1: 
# Controller receives Mobile Interface preset request and queries Database Server
print("Test 1: Controller receives Mobile Interface preset request and queries Database Server")
print("------------------------------------------------------------------------------------------")
print("MB requests preset teas and alarms from CT")
jdata = {"msgId": 2}
data = json.dumps(jdata)
print("Sending: " + data)
sMobile.sendto(data.encode('utf-8'), contServer_address) #MB send CT
print("DB receives the request from CT")
buf, address = sData.recvfrom(1024) #DB receive from CT
print("Received: " + buf.decode('utf-8'))
payload = json.loads(buf.decode('utf-8'))
print("Test 1: " + checkTest(payload['msgId'], 3) + "\n\n")

# Test 2: 
# Controller returns database information to Mobile Interface
print("Test 2: Controller returns database information to Mobile Interface")
print("------------------------------------------------------------------------------------------")
print("DB sends acknowlegement to CT")
data = json.dumps(testPreset)
print("Sending: " + data)
sData.sendto(data.encode('utf-8'), contServer_address) #DB send to CT
print("MB receives the acknowledgment from CT")
buf, address = sMobile.recvfrom(1024)
print("Received: " + buf.decode('utf-8'))
payload = json.loads(buf.decode('utf-8'))
print("Test 2: " + checkTest(payload['msgId'], 2) + "\n\n")

# Test 3: 
# Mobile Interface selects a tea and alarm and requests to start the brewing process
print("Test 3: Mobile Interface selects a tea and alarm and requests to start the brewing process")
print("------------------------------------------------------------------------------------------")
print("MB sends CT specified tea and alarm")
data = json.dumps(testSelectTeaAlarm)
print("Sending: " + data)
sMobile.sendto(data.encode('utf-8'), contServer_address)
print("AD receives request to start measuring the temperature of the water from the CT")
buf = os.read(masterC, 1024).decode('utf-8')
print("Received: " + buf)
print("Test 3: " + checkTest(buf, "tStart") + "\n\n")

# Test 4:
# Arduino sends a measured temperature to the Controller and if valid will stop measuring
print("Test 4: Arduino sends a measured temperature to the Controller and if valid will stop measuring")
print("------------------------------------------------------------------------------------------")
print("AD sends the measured water temperature to CT")
print("Sending T20.5")
ser.write("T20.5".encode('utf-8'))
print("Waiting 5 seconds to remeasure the water temperature")
time.sleep(5)
print("Sending T100.13")
ser.write("T100.13".encode('utf-8'))
print("AD receives request to stop measuring the water temperature")
buf = os.read(masterC, 1024).decode('utf-8')
print("Received: " + buf)
print("Test 4: " + checkTest(buf, "tStop") + "\n\n")

# Test 5:
# The Controller requests the Arduino to lower the teabag
print("Test 5: The Controller requests the Arduino to lower the tea bag. The Arduino sends a message to the Controller that the tea bag has been lowered.")
print("------------------------------------------------------------------------------------------")
print("AD receives request to lower tea bag from CT")
buf = os.read(masterC, 1024)
print("Received: " + buf.decode('utf-8'))
print("AD sends acknowledgment that tea bag has been lowered to CT")
print("Sending: lowerTea" + "\n\n")
ser.write("lowerTea".encode('utf-8'))

# Test 6:
# The Controller requests the Arduino to start the specified timer on the LCD display
print("Test 6: The Controller requests the Arduino to start the specified timer on the LCD display. The Arduino sends a message to the Controller that the timer has completed.")
print("------------------------------------------------------------------------------------------")
print("AD receives request to start the timer from CT")
buf = os.read(masterC, 1024)
print("Received: " + buf.decode('utf-8'))
print("Waiting 5 seconds to brew")
time.sleep(5)
print("AD sends acknowledgment that time timer is complete to CT")
print("Sending: 6Done" + "\n\n")
ser.write("6Done".encode('utf-8'))

# Test 7:
# The Controller requests the Arduino to raise the teabag
print("Test 7: The Controller requests the Arduino to raise the tea bag. The Arduino sends a message to the Controller that the tea bag has been raised.")
print("------------------------------------------------------------------------------------------")
print("AD receives request to raise tea bag from CT")
buf = os.read(masterC, 1024)
print("Received: " + buf.decode('utf-8'))
print("AD sends acknowledgment that tea bag has been raise to CT")
print("Sending: raiseTea" + "\n\n")
ser.write("raiseTea".encode('utf-8'))

# Test 8:
# The Controller requests the Arduino to turn on the light and notifies the Mobile Interface that the tea is complete
print("Test 8: The Controller requests the Arduino to turn on the LED light. The Controller sends a message to the Mobile Interface to notify the user that the tea is ready.")
print("------------------------------------------------------------------------------------------")
print("AD receives request to turn on the LED from CT")
buf = os.read(masterC, 1024)
print("Received: " + buf.decode('utf-8')) #71
print("MB receives a notification from CT that the brewing process is complete")
buf, address = sMobile.recvfrom(1024)
print("Received: " + buf.decode('utf-8'))
payload = json.loads(buf.decode('utf-8'))
print("Test 8: " + checkTest(payload['msgId'], 4) + "\n\n")

# TestID : 9
# The Mobile Interface acknowledges the notification which turns off the LED the alarm
print("Wait 10 seconds before acknowledging")
time.sleep(10)
print("Test 9: The Mobile Interface acknowledges the notification which turns off the LED the alarm")
print("------------------------------------------------------------------------------------------")
print("MB sends CT a acknowledgment from the notification")
data = json.dumps(testAckNotification)
print("Sending: " + data)
sMobile.sendto(data.encode('utf-8'), contServer_address)
print("AD receives request to turn off the LED from CT")
buf = os.read(masterC, 1024).decode('utf-8')
print("Received: " + buf)
print("Test 9: " + checkTest(buf, "70") + "\n\n")

# Test :
# Adding custom tea information
print("Test: Adding custom tea information")
print("------------------------------------")
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
print("MB receives the acknowledgment from CT")
buf, address = sMobile.recvfrom(1024)
print("Received: " + buf.decode('utf-8') + "\n\n")

# Test :
# Removing custom tea information
print("Test: Removing custom tea information")
print("-------------------------------------")
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
print("MB receives the acknowledgment from CT")
buf, address = sMobile.recvfrom(1024)
print("Received: " + buf.decode('utf-8') + "\n\n")

# Clean up
print("Clean up sockets" + "\n\n")
sData.close()
sMobile.close()