import threading
from threading import Lock

"""
Cancel object used to let a user cancel a brewing process
"""
class Cancel:
    def __init__(self):
        self.lock = Lock()
        self.cancel = 0 # Cancel request has not occurred, set to 0

    """
    Check if state of cancel
    """
    def getCancel(self):
        self.lock.acquire()
        curr = self.cancel
        lock.release()
        return curr
s
    """
    Set cancel state
    """
    def setCancel(self, val):
        self.lock.acquire()
        self.cancel = val
        lock.release()
