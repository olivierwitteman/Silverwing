from lib.pymavlink.dialects.v20.custom_messages import MAVLink_aeroprobe_message
from sensors.AbstractBuffer import Buffer


class AeroprobeBuffer(Buffer):
    def __init__(self, mavLink, sendFrequency):
        self.LENGTH = 16
        super(AeroprobeBuffer, self).__init__(mavLink, sendFrequency)

    def addMessage(self, message):
        for index, parameter in enumerate(message.getParameters()):
            self.addParameter(parameter, index)

    def toMavLinkMessage(self):
        return MAVLink_aeroprobe_message(hour=self._parameters[0].getValue(),
                                         min=self._parameters[1].getValue(),
                                         sec=self._parameters[2].getValue(),
                                         mil=self._parameters[3].getValue(),
                                         airspeed=self._parameters[7].getValue(),
                                         ind_airspeed=self._parameters[8].getValue(),
                                         angle_of_attack=self._parameters[9].getValue(),
                                         angle_of_sideslip=self._parameters[10].getValue(),
                                         press_alt=self._parameters[11].getValue(),
                                         press_static=self._parameters[12].getValue(),
                                         press_tot=self._parameters[13].getValue(),
                                         ext_temp=self._parameters[14].getValue())