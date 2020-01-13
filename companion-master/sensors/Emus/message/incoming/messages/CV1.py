from sensors.Emus.message.encodings.HexDec import HexDec
from sensors.Emus.message.incoming.EmusInMessage import EmusInMessage
from sensors.Emus.message.incoming.Field import Field
from sensors.Parameter import Parameter


class CV1(EmusInMessage):
    def __init__(self, string):
        self._fields = [
            Field(HexDec(0, 0.01),
                  Parameter('TOTAL VOLTAGE', 'V')),
            Field(HexDec(0, 0.1),
                  Parameter('CURRENT', 'A')),
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None
        ]
        super().__init__(string)
