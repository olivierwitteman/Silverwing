from pymavlink import mavutil
import sys

from mavLink.MavLink import MavLink
from sensors.AbstractThread import AbstractThread


class MavLinkReceiverThread(AbstractThread):
    def __init__(self, device, port):
        super().__init__(device, port, None, log=False)

    def openInterface(self, port):
        return MavLink(port)

    def read(self):
        message = None
        while (message is None):
            message = self.interface.getConnection().recv_match(blocking=False)
        messageType = message.get_type()
        print("MessageType: " + str(messageType))
        if (messageType == "BAD_DATA"):
            print("Bad data received!")
            if (mavutil.all_printable(message.data)):
                sys.stdout.flush()
        elif (messageType == "BMS CONTACTOR"):
            emus = self.device.getEmus()
            if (message.main == 1):
                emus.closeContactor()
            elif (message.main == 0):
                emus.openContactor()
        elif (messageType == "COOLING_CONTACTOR"):
            if (message.main == 1):
                self.device.getCoolingContactor.setHigh()
            elif (message.main == 0):
                self.device.getCoolingContactor.setLow()
        else:
            pass
