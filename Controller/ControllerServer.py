import json, socket, sys, time, netifaces
from ArduinoControl import ArduinoControl
#from ArduinoControlTest import ArduinoControlTest #for testing only
from DatabaseControl import DatabaseControl
from MobileControl import MobileControl
from SpeakerControl import SpeakerControl
from SwitchControl import SwitchControl

class ControllerServer:
    def __init__(self):
        self.sMain = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sCancel = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket used for user to cancel
        self.serverPort = 1080
        self.server_address = ("localhost", self.serverPort) #netifaces.ifaddresses('eth0')[netifaces .AF_INET][0]['addr']
        self.cancel = False
        # Initialize the control objects
        self.arduinoControl = ArduinoControl()
        # self.arduinoControl = ArduinoControlTest() #for testing only
        self.databaseControl = DatabaseControl()
        self.mobileControl = MobileControl()
        self.speakerControl = SpeakerControl()
        self.switchControl = SwitchControl()

        self.cancel = Cancel() # Create Cancel object to allow user to cancel process
        cancelThread = Thread(target = cancel) # Create new thread to monitor user cancel requests
        cancelThread.start()


    """
    Cancels tea brewing process, resets Arduino controls and speaker and notifies
    user that cancel process is done
    """
    def cancel(self):
        self.sCancel.bind(('localhost', 1075))

        while self.cancel.getCancel() != 1:
            print("Waiting to receive on port 1075")
            buf, addr = self.sCancel.recvfrom(1024)
            payload = json.loads(buf.decode('utf-8'))
            if payload["msgId"] == 13:
                self.cancel.setCancel(1)
                self.arduinoControl.reset()
                self.reset() # I think we also need this call for the alarm
                self.mobileControl.notifyUserCanceL(self.sCancel)
                self.cancel.setCancel(0) # Re-enable cancel


    """
    Receive Controller requests from the other processes to process
    """
    def receiveRequests(self):
        self.sMain.bind(self.server_address)

        while True:
            print("Waiting to receive on port %d" % self.serverPort)
            buf, addr = self.s.recvfrom(1024)
            self.decipherReceivedPacket(buf)


    """
    Execute desired actions by examining the received message contents

    buf - Buffer of received message
    """
    def decipherReceivedPacket(self, buf):
        print("Received: " + buf.decode('utf-8'))
        payload = json.loads(buf.decode('utf-8'))
        if payload['msgId'] == 2: # Mobile requests preset tea and alarms
            responseData = self.databaseControl.getTeaAlarmInformation(self.s) #get tea and alarm from Database
            data = json.loads(responseData)
            self.mobileControl.retrieveTeaInfoAndAlarm(data['teas'], data['alarms'], self.sMain) #send tea and alarm to Mobile
        elif payload['msgId'] == 4: # Mobile selected a specified tea and alarm
            # self.arduinoControl.setSerialPort() #for testing only
            self.startTeaProcess(payload['tea'], payload['alarm'])
        elif payload['msgId'] == 8: # Mobile acknowledges the notification sent
            self.reset()
        elif payload['msgId'] == 9: # Mobile request to add custom tea information
            responseData = self.databaseControl.addCustomTeaInformation(payload['tea']['name'], payload['tea']["steepTime"], payload['tea']['temp'], self.sMain)
            data = json.loads(responseData)
            self.mobileControl.addCustomTeaInformation(data['teaId'], data['status'], self.sMain)
        elif payload['msgId'] == 10: # Mobile request to remove custom tea information
            responseData = self.databaseControl.removeCustomTeaInformation(payload['teaId'], self.sMain)
            data = json.loads(responseData)
            self.mobileControl.removeCustomTeaInformation(data['teaId'], data['status'], self.sMain)
        elif payload['msgId'] == 13: # Mobile request to cancel the brewing process
            self.cancel()


    """
    Execute the sequential actions for the brewing tea process

    tea - the specified tea
    alarm - the specified alarm
    """
    def startTeaProcess(self, tea, alarm):
        self.switchControl.turnOnKettle()
        self.arduinoControl.measureWater(tea['temp'])
        self.switchControl.turnOffKettle()
        self.arduinoControl.lowerTeaBag()
        self.arduinoControl.displayTimer(tea["steepTime"])
        self.arduinoControl.raiseTeaBag()
        self.arduinoControl.turnOnLED()
        self.speakerControl.playAlarm(alarm['fileLocation'])
        self.mobileControl.notifyUser(1, self.sMain)


    """
    Reset the process (ie. turn off the LED and stop the alarm)
    """
    def reset(self):
        self.arduinoControl.turnOffLED()
        self.speakerControl.stopAlarm()


def main():
    print("Starting ControllerServer")
    controller = ControllerServer()
    controller.receiveRequests()

if __name__ == "__main__":
    main()
