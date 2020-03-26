import time
import threading
from sensors.Parameter import Parameter

"""
The MavLink buffer that takes a MavLink object and runs a thread that periodically sends a MavLinkMessage
representation of itself to the MavLink object. Messages can be added to the buffer to be handled internally; 
that is, overwriting internal parameters to the most up to date instance. 
"""

class Buffer(object):
    def __init__(self, mavLink, sendFrequency):
        # MavLink-related stuff.
        self._mavLink = mavLink
        self._sendInterval = 1.0 / sendFrequency

        # buffer-related stuff.
        self._parameters = []
        for i in range(self.LENGTH):
            self._parameters.append(Parameter())

        # start MavLink-message-sender thread.
        thread = threading.Thread(target=self._sender)
        thread.start()

    def _sender(self):
        while (1):
            if not all (parameter.getValue() is None for parameter in self._parameters):
                self._mavLink.send(self.toMavLinkMessage())
            time.sleep(self._sendInterval)

    """ Getter method for the parameters.

    Returns:
        list<Parameter>: The list of _parameters.
    """
    def getParameters(self):
        return self._parameters

    def addMessage(self, message):
        raise NotImplementedError('Subclasses must override addMessage()!')

    def addParameter(self, parameter, index):
        self._parameters[index] = parameter

    """ Generates a MAVLink message from itself.

    Returns:
        mavlink_<name>_message: The generated MAVLink message.
    """
    def toMavLinkMessage(self):
        raise NotImplementedError('Subclasses must override toMavLinkMessage()!')

    """ Generates the string representation of itself.

    Returns:
        string: The string representation.
    """
    def toString(self):
        string = self.__class__.__name__ + ': '
        for parameter in self.getParameters():
            if parameter is not None:
                string += '\n  ' + parameter.toString()
        return string

    def getSendInterval(self):
        return self._sendInterval