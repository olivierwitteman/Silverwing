import time


class PWMReader(object):
    def __init__(self, channel):
        self.channel = channel

        self.prevHighTime = 0
        self.prevValue = 0

        self.dutyCycle = -1
        self.frequency = -1

        import Adafruit_BBIO.GPIO as GPIO
        GPIO.setup(channel, GPIO.IN)
        GPIO.add_event_detect(channel, GPIO.BOTH,
                              callback=self.GPIOCallbackHandler)  # Detect both low-high and high-low events

    def calculateDutyCycle(self, hightime):
        return round(hightime * self.frequency * 100)

    def GPIOCallbackHandler(self, channel):
        import Adafruit_BBIO.GPIO as GPIO
        value = GPIO.input(channel)
        if (value == 1 and self.prevValue != 1):
            # print("Input is HIGH")
            currentTime = time.time()
            if self.prevHighTime != 0:
                self.frequency = round(1.0 / (currentTime - self.prevHighTime))
            self.prevHighTime = currentTime
            # print("Frequency is " + str(self.frequency))
        if (value == 0 and self.prevHighTime != 0 and self.prevValue != 0):
            # print("Input is LOW")
            highTime = time.time() - self.prevHighTime
            self.dutyCycle = self.calculateDutyCycle(highTime)
            # print("Dutycycle is: " + self.dutyCycle)

        self.prevValue = value

    def getDutyCycle(self):
        return self.dutyCycle

    def getFrequency(self):
        return self.frequency
