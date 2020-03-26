class DigitalOut(object):
    def __init__(self, port):
        self._port = port
        self.openInterface()

    def openInterface(self):
        import Adafruit_BBIO.GPIO as GPIO
        GPIO.setup(self._port, GPIO.OUT)

    def setHigh(self):
        import Adafruit_BBIO.GPIO as GPIO
        GPIO.output(self._port, GPIO.HIGH)

    def setLow(self):
        import Adafruit_BBIO.GPIO as GPIO
        GPIO.output(self._port, GPIO.LOW)
