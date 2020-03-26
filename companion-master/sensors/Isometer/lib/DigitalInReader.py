class DigitalInReader(object):
    def __init__(self, channel):
        self.channel = channel
        import Adafruit_BBIO.GPIO as GPIO
        GPIO.setup(channel, GPIO.IN)

    def getValue(self):
       import Adafruit_BBIO.GPIO as GPIO
       return GPIO.input(self.channel)