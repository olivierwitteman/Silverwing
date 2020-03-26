class EmusOutMessage(object):

    def __init__(self, id, fields):
        self._id = id

        """The data fields present in the message in string format."""
        self._fields = fields

    """Calculates CRC.
    :returns:   CRC value for the message (self).
    """
    def _crc(self):
        byteData = bytearray(self._id + ',' + ','.join(self._fields) + ',', 'ascii')

        crc = 0
        for byte in byteData:
            for i in range(8):
                feedback_bit = (crc ^ byte) & 0x01
                if feedback_bit == 0x01:
                    crc = crc ^ 0x18
                crc = (crc >> 1) & 0x7F
                if feedback_bit == 0x01:
                    crc = crc | 0x80
                byte = byte >> 1
        return '{0:0{1}X}'.format(crc, 2)

    """Sets data bit at specific index.
    :param index:   Bit index.
    :param value:   To-be-set bit value.
    """
    def setBit(self, fieldIndex, bitIndex, value):
        byte = int(self._fields[fieldIndex], 16)

        if (value == 1):
            byte |= 1 << bitIndex
        else:
            byte &= ~(1 << bitIndex)

        self._fields[fieldIndex] = '{0:0{1}X}'.format(byte, 8)

    """Generates string of the message (self).
    :returns:   Message string.
    """
    def toString(self):
        return self._id + ',' + ','.join(self._fields) + ',' + self._crc() + '\r\n'

    """Generates request-message.
    :returns:   New EmusOutMessage instance.
    """
    @classmethod
    def requireMessage(cls, id=None):
        return cls(['?'])

    """Generates byte array ready to be sent over the serial bus
    :returns:   Byte-array view of this message.
    """
    def toByteArray(self):
        return bytearray(self.toString(), 'ascii')
