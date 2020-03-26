import threading

import serial

from sensors.AbstractThread import AbstractThread
import sensors.Emus.message.incoming.messages as incoming
import sensors.Emus.message.outgoing.messages as outgoing


class EmusThread(AbstractThread):

    def __init__(self, device, port, buffer):
        super().__init__(device, port, buffer)
        self.switcher = {
            "BB1": incoming.BB1, "BB2": incoming.BB2,
            "BC1": incoming.BC1,
            "BT1": incoming.BT1, "BT2": incoming.BT2,
            "BT3": incoming.BT3, "BT4": incoming.BT4,
            "BV1": incoming.BV1, "BV2": incoming.BV2,
            "CF2": incoming.CF2, "CV1": incoming.CV1,
            "IN1": incoming.IN1, "OT1": incoming.OT1,
            "ST1": incoming.ST1,
        }
        self.incomingCF2 = None
        self.contactorClosed = False

    def openInterface(self, port):
        return serial.Serial(port, 57600)

    def read(self):
        byteString = self.interface.readline()

        while (byteString == b'\x00\n'):
            byteString = self.interface.readline()

        string = str(byteString, 'utf-8')
        id = string.split(',')[0]
        if not (id in self.switcher):
            return self.read()

        message = self.switcher[id](string)

        if (id == "CF2"):
            self.incomingCF2 = message

        return message

    """ Sends a message over the sensor interface.
    
    Args:
        message (EmusOutMessage): The message to be sent.
    """
 #       self.initializeAeroprobe()
    def send(self, message):
        self.interface.write(message.toByteArray())

    """ Allow the contactor to close by disabling "External contactor deactivation".
    
    When "External contactor deactivation" is disabled, the EMUS opens the pre-charge circuit when all protection
    types issue a pass.
    """
    def closeContactor(self):
        if (self.contactorClosed == False):
            print("Closing contactor!")
            self._setContactor(True)

    """ Force-close the contactor to enabling "External contactor deactivation".
    
    When "External contactor deactivation" is enabled, the EMUS will keep the contactor open independently of the
    status of the protection types.
    """
    def openContactor(self):
        if (self.contactorClosed == True):
            print("Opening contactor!")
            self._setContactor(False)

    """ Internal utility method that sets the contactor by enabling or disabling "External contactor deactivation".
    
    The method starts a thread that runs the _contactorCallBack method.
    
    Args:
        closed (bool): Boolean indicating whether the contactor should be allowed to close.
    """
    def _setContactor(self, closed):
        thread = threading.Thread(target=self._contactorCallback, args=[closed])
        thread.start()

    """ Internal utility method that sends a CF2 message with the "External contactor deactivation" pin set.
    
    The method sends a CF2 request message and waits for the CF2 message to arrive and to overwrite self.incomingCF2.
    After arrival of the CF2 message, the data is fed into a new outgoing CF2 message where the "External contactor
    deactivation" bit is modified based on the method parameter. Finally, the modified CF2 message is sent over the
    sensor interface.
    
    Args:
        closed (bool): Boolean indicating whether the contactor should be allowed to close.
    """
    def _contactorCallback(self, closed):
        self.incomingCF2 = None
        self.send(outgoing.CF2.requireMessage(1600))
        while (self.incomingCF2 == None):
            pass
        field = self.incomingCF2.getParameters()[1].getRaw()

        message = outgoing.CF2.contactorMessage(field, 1 - closed)
        self.send(message)
