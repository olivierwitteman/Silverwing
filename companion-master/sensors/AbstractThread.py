import threading

from logger.Logger import Logger

"""
A class extending Threading.thread that takes a buffer and a port name. Classes extending AbstractThread require an
implementation for opening the interface corresponding to the port name and an implementation for reading the interface. 
AbstractThread then handles the loop that periodically reads the interface, logs everything and updates its buffer.
"""

class AbstractThread(threading.Thread):

    def __init__(self, device, port, buffer=None, log=True):
        super(AbstractThread, self).__init__()
        self.isRunning = False

        # initialises host device.
        self.device = device

        # initialises sensor interface.
        self.interface = self.openInterface(port)

        # initialises MAVLink message buffer.
        self.buffer = buffer

        # initialises data logger.
        self.logger = Logger(self.toString()) if log else None

    """ Opens sensor interface that the read method.
    
    Args:
        port (string): Port designator.
    Returns:
        object: Interface object.
    """
    def openInterface(self, port):
        raise NotImplementedError('Subclasses must override openSerial()!')

    def getInterface(self):
        return self.interface

    """ Reads sensor data from sensor interface and returns the corresponding message.
    
    Returns:
        AbstractMessage: Message containing sensor data.
    """
    def read(self):
        raise NotImplementedError('Subclasses must override read()!')

    """ Starts the thread through threading.Thread by calling the run method.
    """
    def start(self):
        print("Starting " + self.toString() + "!")
        self.isRunning = True
        super().start()

    """ Thread logic that handles all reading, logging and relaying over MAVLink.
    
    The logic consists of three steps:
    1) Reading the sensor interface for a new AbstractMessage.
    2) Logging the message to the thread-specific log file.
    3) Overwriting the buffer with the new message.
    """
    def run(self):
        while (self.isRunning):

            # read interface for message.
            message = self.read()
            if self.toString() is not "AeroprobeThread" and self.toString() is not "MavLinkReceiverThread":
                print(message.toString())

            # adds to MAVLink buffer
            if (self.buffer != None):
                self.buffer.addMessage(message)

            # log message.
            if (self.logger != None):
                self.logger.log(message)

    """ Stops the thread.
    """
    def stop(self):
        print("Stopping " + self.toString() + "!")
        self.isRunning = False

    """ Returns the thread name as a string
    
    Returns:
        string: The thread name.
    """
    def toString(self):
        return self.__class__.__name__
