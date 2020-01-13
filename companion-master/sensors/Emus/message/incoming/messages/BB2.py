from sensors.Emus.message.encodings.HexDec import HexDec
from sensors.Emus.message.incoming.EmusInMessage import EmusInMessage
from sensors.Emus.message.incoming.Field import Field
from sensors.Parameter import Parameter


class BB2(EmusInMessage):
    def __init__(self, string):
        self._fields = [
            Field(HexDec(0, 1),
                  Parameter('CELL STRING NUMBER', None)),
            Field(HexDec(0, 1),
                  Parameter('CELL NUMBER OF FIRST CELL IN GROUP', None)),
            Field(HexDec(0, 1),
                  Parameter('SIZE OF GROUP', None)),
            Field(HexDec(0, 100 / 255),
                  Parameter('CELL STRING NUMBER', '%'))
        ]
        super().__init__(string)
