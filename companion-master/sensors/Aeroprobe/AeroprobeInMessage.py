import struct

from sensors.AbstractInMessage import AbstractMessage
from sensors.Parameter import Parameter


class AeroprobeInMessage(AbstractMessage):
    def __init__(self, bytes):
        super().__init__(bytes)

    @classmethod
    def _setParameters(cls, bytes):
        format = '>BBBHBBBffffifffB'
        parameters = list()
        parameters.append(Parameter("Hour", "hr"))
        parameters.append(Parameter("Minute", "min"))
        parameters.append(Parameter("Second", "s"))
        parameters.append(Parameter("Millisecond", "ms"))
        parameters.append(Parameter("Month", "month"))
        parameters.append(Parameter("Day", "day"))
        parameters.append(Parameter("Year", "year"))
        parameters.append(Parameter("Airspeed", "m/s"))
        parameters.append(Parameter("Indicated Airspeed", "m/s"))
        parameters.append(Parameter("Angle of Attack", "deg"))
        parameters.append(Parameter("Angle of Sideslip", "deg"))
        parameters.append(Parameter("Pressure altitude", "m "))
        parameters.append(Parameter("Static Pressure", "Pa"))
        parameters.append(Parameter("Total Pressure", "Pa"))
        parameters.append(Parameter("Ext. Temp. Sensor Temperature", "C"))
        parameters.append(Parameter("Checksum", ""))

        values = struct.unpack(format, bytes)
        for i in range(len(parameters)):
            parameters[i].setValue(values[i])
        return parameters