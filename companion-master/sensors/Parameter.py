class Parameter(object):
    def __init__(self, name="Unnamed", unit=None, value=None, raw=None):
        self._name = name
        self._unit = unit
        self._value = value
        self._raw = raw

    def setName(self, name):
        self._name = name

    def getName(self):
        return self._name

    def getUnit(self):
        return self._unit

    def setValue(self, value):
        self._value = value

    def getValue(self):
        return self._value

    def setRaw(self, raw):
        self._raw = raw

    def getRaw(self):
        return self._raw

    def toString(self):
        string = str(self._name) + ": "
        if (self._value != None):
            string += str(self._value)
        else:
            string += '-'
        if (self._unit != None):
            string += " " + str(self._unit)
        if (self._raw != None):
            string += " (" + str(self._raw) + ")"
        return string
