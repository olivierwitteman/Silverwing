from lib.pymavlink.dialects.v20.custom_messages import MAVLink_servo_feedback_message
from lib.pymavlink.dialects.v20.custom_messages import MAVLink_servo_currentsensor_message
from lib.pymavlink.dialects.v20.custom_messages import MAVLink_cooling_currentsensor_message

from mavLink.MavLink import MavLink
from mavLink.MavLinkReceiverThread import MavLinkReceiverThread

from sensors.Aeroprobe.AeroprobeThread import AeroprobeThread
from sensors.Emus.EmusThread import EmusThread
from sensors.Emus.EmusBuffer import EmusBuffer
from sensors.Aeroprobe.AeroprobeBuffer import AeroprobeBuffer
from sensors.Analog.AnalogBuffer import AnalogBuffer
from sensors.Analog.AnalogThread import AnalogThread
from sensors.Isometer.IsometerBuffer import IsometerBuffer
from sensors.Isometer.IsometerThread import IsometerThread
from lib.DigitalOut import DigitalOut


class Companion(object):

    """ Device object which initialises all sensor threads.

    Args:
        useBeagleBone (bool): Boolean indicating whether the host device is a BeagleBone.
        useMAVLink (bool): Boolean indicating whether a MAVLink connection is used.
        threads (list): List of threads to be run.
    """
    def __init__(self, useBeagleBone, useMAVLink):

        self._useBeagleBone = useBeagleBone
        self._threads = list()

        # if the host device is a Beaglebone.
        if (useBeagleBone):
            self.initializeUarts()

        # if a MavLink connection exists to px4.
        if (useMAVLink):
            self._mavLink = self.initializeMavLink()
        else:
            self._mavLink = MavLink()

        # reference to Emus, which is a special case, as this is the only thread that requires external control.
        self._emus = None
        # reference to cooling contactor digital output. Necessary as it requires external control.
        self._coolingContactor = None

        """" Initializations """
        self.initializeEmus()
        self.initializeAeroprobe()
        self.initializeServoPositionFeedback()
        self.initializeServoCurrentSensor()
        self.initializePumpCurrentSensor()
        self.initializeIsometer()
        if (useMAVLink):
            self.initializeCoolingContactor()


    def isBeagleBone(self):
        return self._useBeagleBone

    def addThread(self, thread):
        self._threads.append(thread)
        return self

    def addThreadType(self, Thread, port):
        thread = Thread(self, port)
        self._threads.append(thread)
        return self

    def start(self):
        for thread in self._threads:
            thread.start()

    def stop(self):
        for thread in self._threads:
            thread.stop()

    def getEmus(self):
        return self._emus

    def getCoolingContactor(self):
        return self._coolingContactor

    def initializeMavLink(self):
        thread = MavLinkReceiverThread(self, '/dev/ttyO4')
        self._threads.append(thread)
        return thread.getInterface()

    def initializeEmus(self):
        port = '/dev/ttyUSB0' if self.isBeagleBone() else '/dev/ttyUSB0'
        buffer = EmusBuffer(self._mavLink, sendFrequency=1)
        thread = EmusThread(self, port, buffer)
        self._threads.append(thread)
        self._emus = thread

    def initializeAeroprobe(self):
        port = '/dev/ttyO1' if self.isBeagleBone() else '/dev/ttyUSB0'
        buffer = AeroprobeBuffer(self._mavLink, sendFrequency=200)
        thread = AeroprobeThread(self, port, buffer)
        self._threads.append(thread)

    def initializeServoPositionFeedback(self):
        buffer = AnalogBuffer(self._mavLink, sendFrequency=1, size=3, messageCreator=MAVLink_servo_feedback_message)

        '''Note: if analog input channels are changed, also change this in AnalogBuffer.py'''
        self._threads.extend([
            AnalogThread(self, 'AIN0', buffer),     # servo1
            AnalogThread(self, 'AIN1', buffer),     # servo2
            AnalogThread(self, 'AIN2', buffer)      # servo3
        ])

    def initializeServoCurrentSensor(self):
        buffer = AnalogBuffer(self._mavLink, sendFrequency=1, size=3, messageCreator=MAVLink_servo_currentsensor_message)

        '''Note: if analog input channels are changed, also change this in AnalogBuffer.py'''
        self._threads.extend([
            AnalogThread(self, 'AIN3', buffer),     # servo1
            AnalogThread(self, 'AIN4', buffer),     # servo2
            AnalogThread(self, 'AIN5', buffer)      # servo3
        ])

    def initializePumpCurrentSensor(self):
        buffer = AnalogBuffer(self._mavLink, sendFrequency=1, size=1, messageCreator=MAVLink_cooling_currentsensor_message)

        '''Note: if analog input channel is changed, also change this in AnalogBuffer.py'''
        self._threads.append(AnalogThread(self, 'AIN6', buffer))

    def initializeIsometer(self):
        buffer = IsometerBuffer(self._mavLink, sendFrequency=1)
        self._threads.append(IsometerThread(self, portPWM="P8_7", portStatus="P8_9", buffer=buffer))

    def initializeCoolingContactor(self):
        self._coolingContactor = DigitalOut("P8_17")

    @staticmethod
    def initializeUarts():
        import Adafruit_BBIO.UART as UART
        UART.setup("UART1")
        UART.setup("UART2")
        UART.setup("UART4")