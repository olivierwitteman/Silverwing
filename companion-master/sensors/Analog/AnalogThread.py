from sensors.AbstractThread import AbstractThread
from sensors.Analog.lib.AdcReader import AdcReader
from sensors.Analog.AnalogMessage import AnalogMessage
import time


class AnalogThread(AbstractThread):

    def __init__(self, device, port, buffer):
        self.port = port
        super().__init__(device, port, buffer)

    def openInterface(self, port):
        return AdcReader(port)

    def read(self):
        time.sleep(self.buffer.getSendInterval())
        value = round(self.interface.getValue(), 4)
        message = AnalogMessage(self.port, value)
        for parameter in message.getParameters():
            parameter.setName(message.getPort())
        self.buffer.addMessage(message)
        return message

    """ Returns the thread name as a string

    Returns:
        string: The thread name with the port name appended (to distinguish multiple AnalogThreads running)
    """

    def toString(self):
        return self.__class__.__name__ + str(self.port)
