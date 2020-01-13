from sensors.AbstractBuffer import Buffer
from lib.pymavlink.dialects.v20.custom_messages import MAVLink_isometer_message


class IsometerBuffer(Buffer):
    def __init__(self, mavLink, sendFrequency):
        self.LENGTH = 3
        super(IsometerBuffer, self).__init__(mavLink, sendFrequency)

    def addMessage(self, message):
        for index, parameter in enumerate(message.getParameters()):
            self.addParameter(parameter, index)

    def toMavLinkMessage(self):
        return MAVLink_isometer_message(frequency=self._parameters[0].getValue(),
                                        duty_cycle=self._parameters[1].getValue(),
                                        status=self._parameters[2].getValue())
