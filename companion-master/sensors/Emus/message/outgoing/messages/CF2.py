from sensors.Emus.message.outgoing.EmusOutMessage import EmusOutMessage


class CF2(EmusOutMessage):
    def __init__(self, fields):
        super().__init__("CF2", fields)

    """Creates a Function Flags 0 (1600) CF2 message that sets the contactor to @value.
    :param data:    Data surrounding the contactor bit.
    :param value:   Bit value (Note: when bit 27's flag is DISABLED the contactor is ON).
    :returns:       New CF2 instance containing @data and the contactor set to @value.
    """
    @classmethod
    def contactorMessage(cls, field, value):
        message = cls(['1600', field])
        message.setBit(1, 27, value)
        return message

    @classmethod
    def requireMessage(cls, id=None):
        if (id == None):
            raise ValueError('CF2 requires a parameter ID for its request sentence (i.e., id can not be None)!')
        return cls([str(id), '?'])
