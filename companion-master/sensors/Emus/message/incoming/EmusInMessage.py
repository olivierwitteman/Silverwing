from sensors.AbstractInMessage import AbstractMessage


class EmusInMessage(AbstractMessage):
    def __init__(self, string):
        super().__init__(string)
        self._fields = []

    def _setParameters(self, string):
        parameters = list()

        split = string.split(',')[1:-1]
        for i, data in enumerate(split):
            if (self._fields[i] != None):
                if (split[i] != ''):
                    parameter = self._fields[i].decode(split[i])
                else:
                    parameter = self._fields[i].fill(None, None)
                parameters.append(parameter)
        return parameters

    def toMavLinkMessage(self):
        pass

    def getParameters(self):
        return self._parameters