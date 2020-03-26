from sensors.AbstractInMessage import AbstractMessage
from sensors.Parameter import Parameter

class AnalogMessage(AbstractMessage):
    def __init__(self, port, value):
        super().__init__(value)
        self._port = port

    @classmethod
    def _setParameters(cls, value):
        return [Parameter(value=value)]

    def getPort(self):
        return self._port
