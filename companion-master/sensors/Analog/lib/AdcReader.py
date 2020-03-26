class AdcReader(object):
    def __init__(self, channel):
        import Adafruit_BBIO.ADC as ADC
        ADC.setup()
        self.channel = channel

    def getValue(self):
        import Adafruit_BBIO.ADC as ADC
        return ADC.read(self.channel)

    def getChannel(self):
        return self.channel
