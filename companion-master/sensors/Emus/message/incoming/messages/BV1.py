from sensors.Emus.message.encodings.HexDec import HexDec
from sensors.Emus.message.incoming.EmusInMessage import EmusInMessage
from sensors.Emus.message.incoming.Field import Field
from sensors.Parameter import Parameter


class BV1(EmusInMessage):
    def __init__(self, string):
        self._fields = [
            Field(HexDec(0, 1),
                  Parameter('NUMBER OF CELLS', None)),
            Field(HexDec(200, 0.01),
                  Parameter('MIN CELL VOLTAGE', 'V')),
            Field(HexDec(200, 0.01),
                  Parameter('MAX CELL VOLTAGE', 'V')),
            Field(HexDec(200, 0.01),
                  Parameter('AVERAGE CELL VOLTAGE', 'V')),
            Field(HexDec(200, 0.01),
                  Parameter('TOTAL VOLTAGE', 'V')),
            None
        ]
        super().__init__(string)
