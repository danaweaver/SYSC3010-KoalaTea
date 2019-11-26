from meross_iot.manager import MerossManager
from meross_iot.meross_event import MerossEventType
from meross_iot.cloud.devices.light_bulbs import GenericBulb
from meross_iot.cloud.devices.power_plugs import GenericPlug
from meross_iot.cloud.devices.door_openers import GenericGarageDoorOpener

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


    """
    Check if the smart switch is online (ie. is plugged into a socket)

    return - true if online, else false
    """
    def checkOnline(self):
        if not self.smart_sw.online:
            return False
        else:
            return True
    
    
    """
    Turn on the smart switch (ie turn on the kettle)

    return - true if it successfully turned on the switch, else false
    """
    def turnOnKettle(self):
        if self.checkOnline():
            channels = len(self.smart_sw.get_channels())
            for i in range(0, channels):
                print("Turning on channel %d of %s" % (i, self.smart_sw.name))
                self.smart_sw.turn_on_channel(i)
            return True
        else:
            return False


    """
    Turn off the smart switch (ie turn off the kettle)

    return - true if it successfully turned off the switch, else false
    """
    def turnOffKettle(self):
        if self.checkOnline():
            channels = len(self.smart_sw.get_channels())
            for i in range(0, channels):
                print("Turning off channel %d of %s" % (i, self.smart_sw.name))
                self.smart_sw.turn_off_channel(i)
            return True
        else:
            return False