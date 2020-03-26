from sensors.Emus.message.encodings.HexBitBool import HexBitBool
from sensors.Emus.message.encodings.HexDec import HexDec
from sensors.Emus.message.incoming.EmusInMessage import EmusInMessage
from sensors.Emus.message.incoming.Field import Field
from sensors.Parameter import Parameter


class ST1(EmusInMessage):
    def __init__(self, string):
        self._fields = [
            Field(HexDec(),
                  Parameter('CHARGING STATE')),
            Field(HexDec(),
                  Parameter('LAST CHARGING ERROR')),
            Field(HexDec(),
                  Parameter("LAST CHARGING ERROR PARAMETER")),
            Field(HexDec(),
                  Parameter('STAGE DURATION', 's')),
            Field(HexBitBool(list(range(0, 6))),
                  Parameter('BATTERY STATUS FLAGS')),
            Field(HexBitBool(list(range(0, 7)) + list(range(10, 14))),
                  Parameter('PROTECTION FLAGS')),
            Field(HexBitBool([0, 1, 2, 5]),
                  Parameter('POWER REDUCTION FLAGS')),
            Field(HexBitBool(list(range(0, 27))),
                  Parameter('PIN STATUS FLAGS')),
        ]
        super().__init__(string)
