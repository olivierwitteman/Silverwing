from sensors.Emus.message.encodings.HexDec import HexDec
from sensors.Emus.message.incoming.EmusInMessage import EmusInMessage
from sensors.Emus.message.incoming.Field import Field
from sensors.Parameter import Parameter


class BB1(EmusInMessage):
    def __init__(self, string):
        self._fields = [
            Field(HexDec(0, 1),
                  Parameter('NUMBER OF CELLS', None)),
            Field(HexDec(0, 100 / 255),
                  Parameter('MIN CELL BALANCING RATE', '%')),
            Field(HexDec(0, 100 / 255),
                  Parameter('MAX CELL BALANCING RATE', '%')),
            Field(HexDec(0, 100 / 255),
                  Parameter('AVERAGE CELL BALANCING RATE', '%')),
            None,
            Field(HexDec(0, 200, 0.01),
                  Parameter('BALANCING VOLTAGE TRESHOLD', 'V'))
        ]
        super().__init__(string)
