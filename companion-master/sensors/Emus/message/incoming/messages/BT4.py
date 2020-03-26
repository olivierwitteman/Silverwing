import numpy as np

from sensors.Emus.message.encodings.HexDec import HexDec
from sensors.Emus.message.encodings.HexDecByteArray import HexDecByteArray
from sensors.Emus.message.incoming.EmusInMessage import EmusInMessage
from sensors.Emus.message.incoming.Field import Field
from sensors.Parameter import Parameter


class BT4(EmusInMessage):
    def __init__(self, string):
        self._fields = [
            Field(HexDec(0, 1),
                  Parameter('CELL STRING NUMBER', None)),
            Field(HexDec(0, 1),
                  Parameter('CELL NUMBER OF FIRST CELL IN GROUP', None)),
            Field(HexDec(0, 1),
                  Parameter('SIZE OF GROUP', None)),
            Field(HexDecByteArray(-100, 1, dtypeOut=np.int32),
                  Parameter('INDIVIDUAL CELL TEMPERATURES', 'C'))
        ]
        super().__init__(string)
