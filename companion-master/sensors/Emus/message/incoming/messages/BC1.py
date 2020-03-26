import numpy as np

from sensors.Emus.message.encodings.HexDec import HexDec
from sensors.Emus.message.incoming.EmusInMessage import EmusInMessage
from sensors.Emus.message.incoming.Field import Field
from sensors.Parameter import Parameter


class BC1(EmusInMessage):
    def __init__(self, string):
        self._fields = [
            Field(HexDec(0, 1),
                  Parameter('BATTERY CHARGE', 'C')),
            Field(HexDec(0, 1),
                  Parameter('BATTERY CAPACITY', 'C')),
            Field(HexDec(0, 0.01, np.int32, np.int32),
                  Parameter('STATE OF CHARGE', '%'))
        ]
        super().__init__(string)
