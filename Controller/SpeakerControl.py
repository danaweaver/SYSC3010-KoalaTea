from pygame import mixer

class SpeakerControl:

    def __init__(self):
        mixer.init()

    """
    Play alarm song from the specified file
    
    fileLocation - the file location of the alarm song (string)
    """
    def playAlarm(self, fileLocation):
        mixer.music.load(fileLocation)
        mixer.music.play()


    """
    Stop the alarm from playing
    
    fileLocation - the file location of the alarm song (string)
    """
    def stopAlarm(self):
        mixer.music.stop()