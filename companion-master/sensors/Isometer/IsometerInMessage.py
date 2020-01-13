from sensors.AbstractInMessage import AbstractMessage
from sensors.Parameter import Parameter


class IsometerInMessage(AbstractMessage):
    def __init__(self, value):
        super().__init__(value)

    @classmethod
    def _setParameters(cls, value):
        parameters = list()
        parameters.append(Parameter("FREQUENCY", "Hz", value[0]))
        parameters.append(Parameter("DUTY CYCLE", "%", value[1]))
        parameters.append(Parameter("STATUS", None, value[2]))
        return parameters
