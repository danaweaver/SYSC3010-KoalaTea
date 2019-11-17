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

    name - Name of tea profile being added
    steepTime - Steeping time (in sec) of tea profile being added
    temp - Temperature (in degrees) of tea profile being added
    """
    def logAddCustom(self, name, steepTime, temp):
        print("Adding custom tea profile:\nname: " + name + "\nsteep time: " + str(steepTime) + " secs\ntemperature: " + str(temp) + " degrees")

    """
    Logs when request to remove a custom tea information has been received

    teaID - ID of entry requested to be removed
    """
    def logRemoveCustom(self, teaId):
        print("Remove custom tea profile:\nteaId: " + str(teaId))
    
    """
    Logs when response message is sent back to Controller

    Response - Response message
    """
    def logSendResponse(self, response):
        print("Sending reponse - message: " + response)

    """
    Logs when request that has an incorrect message format is received
    """
    def logErrorMessage(self):
        print("Incorrect message format received")
