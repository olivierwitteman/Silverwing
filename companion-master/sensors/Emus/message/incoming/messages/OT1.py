from sensors.Emus.message.encodings.HexBitBool import HexBitBool
from sensors.Emus.message.incoming.EmusInMessage import EmusInMessage
from sensors.Emus.message.incoming.Field import Field
from sensors.Parameter import Parameter


class OT1(EmusInMessage):
    def __init__(self, string):
        self._fields = [
            Field(HexBitBool([7]),
                  Parameter('CHARGER', None)),
            None,
            Field(HexBitBool([4, 5, 6, 7]),
                  Parameter('HEATER / BAT. LOW / BUZZER / CHG. IND.', None)),
            None
        ]
        super().__init__(string)
