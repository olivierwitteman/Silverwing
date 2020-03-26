import numpy as np

from sensors.Emus.message.encodings.HexDec import HexDec
from sensors.Emus.message.incoming.EmusInMessage import EmusInMessage
from sensors.Emus.message.incoming.Field import Field
from sensors.Parameter import Parameter


class BT3(EmusInMessage):
    def __init__(self, string):
        self._fields = [
            Field(HexDec(0, 1),
                  Parameter('NUMBER OF CELLS', None)),
            Field(HexDec(-100, 1, dtypeOut=np.int32),
                  Parameter('MIN CELL TEMPERATURE', 'C')),
            Field(HexDec(-100, 1, dtypeOut=np.int32),
                  Parameter('MAX CELL TEMPERATURE', 'C')),
            Field(HexDec(-100, 1, dtypeOut=np.int32),
                  Parameter('AVERAGE CELL TEMPERATURE', 'C')),
            None,
            None
        ]
        super().__init__(string)
