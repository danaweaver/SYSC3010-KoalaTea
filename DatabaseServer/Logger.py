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
        print("Adding custom tea profile:\nname: " + name + "\ntime: " + str(time) + " secs\ntemperature: " + str(temp) + " degrees")

    """
    Logs when request to remove a custom tea information has been received
    """
    def logRemoveCustom(self, teaId):
        print("Remove custom tea profile:\nteaId: " + str(teaId))
    
    """
    Logs when response message is sent back to Controller
    """
    def logSendResponse(self, response):
        print("Sending reponse - message: " + response)

    """
    Logs when request that has an unexpected message ID is received
    """
    def logUnexpectedMessage(self, id):
        print("Unexpected message request received - ID = " + id)
