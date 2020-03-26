from sensors.AbstractBuffer import Buffer
import sensors.Emus.message.incoming.messages as incoming
from lib.pymavlink.dialects.v20.custom_messages import MAVLink_emus_bms_message


class EmusBuffer(Buffer):
    def __init__(self, mavLink, sendFrequency):
        self.LENGTH = 10
        super(EmusBuffer, self).__init__(mavLink, sendFrequency)

    def addMessage(self, message):

        if (type(message) == incoming.BT1):
            self.addParameter(message.getParameter(0), 0)
            self.addParameter(message.getParameter(1), 1)
            self.addParameter(message.getParameter(2), 2)
            self.addParameter(message.getParameter(3), 3)
        elif (type(message) == incoming.BV1):
            self.addParameter(message.getParameter(1), 4)
            self.addParameter(message.getParameter(2), 5)
            self.addParameter(message.getParameter(3), 6)
            self.addParameter(message.getParameter(4), 7)
        elif (type(message) == incoming.BC1):
            self.addParameter(message.getParameter(2), 8)
        elif (type(message) == incoming.CV1):
            self.addParameter(message.getParameter(1), 9)
        else:
            pass


    def toMavLinkMessage(self):
        args = []
        for parameter in self._parameters:
            if parameter.getValue() is None:
                '''If no data is received, put '-1' as placeholder value (otherwise mavlink message is not sent)'''
                args.append(-1)
            else:
                args.append(parameter.getValue())
        return MAVLink_emus_bms_message(*args)
