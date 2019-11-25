from meross_iot.manager import MerossManager
from meross_iot.meross_event import MerossEventType
from meross_iot.cloud.devices.light_bulbs import GenericBulb
from meross_iot.cloud.devices.power_plugs import GenericPlug
from meross_iot.cloud.devices.door_openers import GenericGarageDoorOpener
import time

# Put Hao's credentials here
EMAIL = "abc"
PASSWORD = "123"

# Code based on https://github.com/albertogeniola/MerossIot

class SwitchControl:

    def __init__(self):
        # Initiates the Meross Cloud Manager. This is in charge of handling the communication with the remote endpoint
        self.manager = MerossManager(meross_email=EMAIL, meross_password=PASSWORD)
        # Starts the manager
        self.manager.start()
        self.smart_sw = self.manager.get_device_by_name("Living room lamp")
        #print("The smart switch is ")
        #print(self.smart_sw)

    def checkOnline(self):
        if not self.smart_sw.online:
            return False
        else:
            return True
    
    
    def turnOnKettle(self):
        channels = len(self.smart_sw.get_channels())
        for i in range(0, channels):
            print("Turning on channel %d of %s" % (i, self.smart_sw.name))
            self.smart_sw.turn_on_channel(i)


    def turnOffKettle(self):
        channels = len(self.smart_sw.get_channels())
        for i in range(0, channels):
            print("Turning off channel %d of %s" % (i, self.smart_sw.name))
            self.smart_sw.turn_off_channel(i)


if __name__ == '__main__':
    # put thus in controller
    swtichControl = SwitchControl()
    if switchControl.checkOnline():
        switchControl.turnOnKettle()
        time.sleep(5)
        switchControl.turnOffKettle()
    # At this point, we are all done playing with the library, so we gracefully disconnect and clean resources.
    print("We are done playing. Cleaning resources...")
    #manager.stop()