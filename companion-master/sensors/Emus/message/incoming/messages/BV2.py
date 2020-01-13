from sensors.Emus.message.encodings.HexDec import HexDec
from sensors.Emus.message.encodings.HexDecByteArray import HexDecByteArray
from sensors.Emus.message.incoming.EmusInMessage import EmusInMessage
from sensors.Emus.message.incoming.Field import Field
from sensors.Parameter import Parameter


class BV2(EmusInMessage):
    def __init__(self, string):
        self._fields = [
            Field(HexDec(0, 1),
                  Parameter('CELL STRING NUMBER', None)),
            Field(HexDec(200, 1),
                  Parameter('CELL NUMBER OF FIRST CELL IN GROUP', None)),
            Field(HexDec(200, 1),
                  Parameter('SIE OF GROUP', None)),
            Field(HexDecByteArray(200, 0.01),
                  Parameter('INDIVIDUAL CELL VOLTAGES', 'V'))
        ]
        super().__init__(string)
