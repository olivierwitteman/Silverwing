from sensors.Emus.message.encodings.HexBitBool import HexBitBool
from sensors.Emus.message.incoming.EmusInMessage import EmusInMessage
from sensors.Emus.message.incoming.Field import Field
from sensors.Parameter import Parameter


class IN1(EmusInMessage):
    def __init__(self, string):
        self._fields = [
            Field(HexBitBool([4, 5, 6]),
                  Parameter('AC SENSE / IGN. IN. / FAST CHG.', None)),
            None,
            None,
            None
        ]
        super().__init__(string)
