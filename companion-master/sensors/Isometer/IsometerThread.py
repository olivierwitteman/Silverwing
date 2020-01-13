from sensors.AbstractThread import AbstractThread
from sensors.Isometer.IsometerInMessage import IsometerInMessage
from sensors.Isometer.lib.PWMReader import PWMReader
from sensors.Isometer.lib.DigitalInReader import DigitalInReader
import time

class IsometerThread(AbstractThread):

    def __init__(self, device, portPWM, portStatus, buffer):
        super().__init__(device, portPWM, buffer)
        self._interface2 = self.openInterface2(portStatus)

    def openInterface(self, port):
        return PWMReader(port)

    def openInterface2(self, port):
        return DigitalInReader(port)


    def read(self):
        time.sleep(self.buffer.getSendInterval())
        message = IsometerInMessage([self.interface.getFrequency(), self.interface.getDutyCycle(), self._interface2.getValue()])
        return message
