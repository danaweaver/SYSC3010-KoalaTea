"""
Logger class will display all database requests to the console on the PC monitor
to track database activity
"""
class Logger:
    """
    Logs when request to retrieve tea information has been received
    """
    def logGetTeaInformation(self):
        print("Retrieving tea information")

    """
    Logs when request to retrieve alarm information has been received
    """
    def logGetAlarmInformation(self):
        print("Retrieving alarm information")

    """
    Logs when request to add a custom tea profile has been received
    """
    def logAddCustom(self, name, time, temp):
        print("Adding custom tea profile:\nname: " + name + "\ntime: " + time + " secs\ntemperature: " + temperature + " degrees")

    """
    Logs when request to remove a custom tea information has been received
    """
    def logRemoveCustom(self, name, time, temp):
        print("Remove custom tea profile:\nname: " + name + "\ntime: " + time + " secs\ntemperature: " + temperature + " degrees")

    """
    Logs when request that has an unexpected message ID is received
    """
    def logUnexpectedMessage(self, id):
        print("Unexpected message request received - ID = " + id)
