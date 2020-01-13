from sensors.AbstractBuffer import Buffer


class AnalogBuffer(Buffer):
    def __init__(self, mavLink, sendFrequency, size, messageCreator):
        self.LENGTH = size
        super(AnalogBuffer, self).__init__(mavLink, sendFrequency)
        self._creator = messageCreator

    def addMessage(self, message):
        if (message.getPort() == 'AIN0'):
            self.addParameter(message.getParameter(0), 0)
        if (message.getPort() == 'AIN1'):
            self.addParameter(message.getParameter(0), 1)
        if (message.getPort() == 'AIN2'):
            self.addParameter(message.getParameter(0), 2)
        if (message.getPort() == 'AIN3'):
            self.addParameter(message.getParameter(0), 0)
        if (message.getPort() == 'AIN4'):
            self.addParameter(message.getParameter(0), 1)
        if (message.getPort() == 'AIN5'):
            self.addParameter(message.getParameter(0), 2)
        if (message.getPort() == 'AIN6'):
            self.addParameter(message.getParameter(0), 0)

    def toMavLinkMessage(self):
        args = []
        for parameter in self._parameters:
            args.append(parameter.getValue())
        return self._creator(*args)
