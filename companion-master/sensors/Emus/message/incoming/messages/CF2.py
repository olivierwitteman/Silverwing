from sensors.Emus.message.encodings.HexDec import HexDec
from sensors.Emus.message.encodings.HexBitBool import HexBitBool
from sensors.Emus.message.incoming.EmusInMessage import EmusInMessage
from sensors.Emus.message.incoming.Field import Field
from sensors.Parameter import Parameter


class CF2(EmusInMessage):
    def __init__(self, string):
        split = string.split(',')[1:-1]
        if split[0] == '1600':
            self._fields = [
                Field(HexDec(0, 1),
                      Parameter('PARAMETER ID', None)),
                Field(HexBitBool(list(range(0, 18)) + list(range(19, 21)) + list(range(22, 23)) + list(range(27, 28)) + list(range(30,31))),
                      Parameter('Function Flags 0'))
            ]
        else:
            self._fields = [
                Field(HexDec(0, 1),
                      Parameter('PARAMETER ID', None)),
                Field(HexDec(0, 1),
                      Parameter('PARAMETER DATA', None))
            ]
        super().__init__(string)
