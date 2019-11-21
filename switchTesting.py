from meross_iot.manager import MerossManager
from meross_iot.meross_event import MerossEventType
from meross_iot.cloud.devices.light_bulbs import GenericBulb
from meross_iot.cloud.devices.power_plugs import GenericPlug
from meross_iot.cloud.devices.door_openers import GenericGarageDoorOpener
from random import randint
import time
import os

EMAIL = "tuanhao256@gmail.com"
PASSWORD = "967456852159"

def event_handler(eventobj):
    if eventobj.event_type == MerossEventType.DEVICE_ONLINE_STATUS:
        print("Device online status changed: %s went %s" % (eventobj.device.name, eventobj.status))
        pass

    elif eventobj.event_type == MerossEventType.DEVICE_SWITCH_STATUS:
        print("Switch state changed: Device %s (channel %d) went %s" % (eventobj.device.name, eventobj.channel_id,
                                                                        eventobj.switch_state))
    elif eventobj.event_type == MerossEventType.CLIENT_CONNECTION:
        print("MQTT connection state changed: client went %s" % eventobj.status)

        # TODO: Give example of reconnection?
    else:
        print("Unknown event!")


if __name__ == '__main__':
    # Initiates the Meross Cloud Manager. This is in charge of handling the communication with the remote endpoint
    manager = MerossManager(meross_email=EMAIL, meross_password=PASSWORD)

    # Register event handlers for the manager...
    manager.register_event_handler(event_handler)

    # Starts the manager
    manager.start()

    smart_sw = manager.get_device_by_name("Living room lamp")
    print("a device is ")
    print(smart_sw)

    if not smart_sw.online:
        print("The plug %s seems to be offline. Cannot play with that..." % smart_sw.name)

    print("Let's play with smart plug %s" % smart_sw.name)

    channels = len(smart_sw.get_channels())
    print("The plug %s supports %d channels." % (smart_sw.name, channels))
    for i in range(0, channels):
        print("Turning on channel %d of %s" % (i, smart_sw.name))
        smart_sw.turn_on_channel(i)

        time.sleep(1)

        print("Turning off channel %d of %s" % (i, smart_sw.name))
        smart_sw.turn_off_channel(i)

    # At this point, we are all done playing with the library, so we gracefully disconnect and clean resources.
    print("We are done playing. Cleaning resources...")
    manager.stop()

    print("Bye bye!")
