import serial

from sensors.AbstractThread import AbstractThread
from sensors.Aeroprobe.AeroprobeInMessage import AeroprobeInMessage


class AeroprobeThread(AbstractThread):

    def __init__(self, device, port, buffer):
        super().__init__(device, port, buffer)

    def openInterface(self, port):
        return serial.Serial(port,
                             baudrate=115200,
                             parity=serial.PARITY_NONE,
                             stopbits=serial.STOPBITS_ONE,
                             timeout=None)

    def read(self):
        # waits for the synchronisation bytes 0xFFFE.
        sync = [self.interface.read(1), self.interface.read(1)]
        while not (sync == [b'\xFF', b'\xFE']):
            byte = self.interface.read(1)
            sync = [sync[1], byte]

        # reads the data packet.
        packetId = int.from_bytes(self.interface.read(1), 'big')
        packetLength = int.from_bytes(self.interface.read(1), 'big')
        bytes = self.interface.read(packetLength)

        # parses the bytes to an AeroprobeInMessage for decoding.
        message = AeroprobeInMessage(bytes)

        return message
