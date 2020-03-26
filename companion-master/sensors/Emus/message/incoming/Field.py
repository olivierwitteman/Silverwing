class Field(object):
    def __init__(self, encoding, parameter):
        self._encoding = encoding
        self._parameter = parameter

    def decode(self, data):
        self._parameter.setValue(self._encoding.decode(data))
        self._parameter.setRaw(data)
        return self._parameter

    def fill(self, value, raw):
        self._parameter.setValue(value)
        self._parameter.setRaw(raw)
        return self._parameter
