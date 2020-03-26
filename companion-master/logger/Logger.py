import logging
import os
from datetime import datetime


class Logger(object):

    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logdir = os.path.dirname(os.path.realpath(__file__)) + '/logs/'
        self.logfile = self.logdir + datetime.now().strftime("%Y%m%d_%H%M%S") + '_' + name + '.log'

        # Create file logger handler
        fh = logging.FileHandler(self.logfile)
        ch = logging.StreamHandler()

        # Set logging levels
        self.logger.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)
        ch.setLevel(logging.ERROR)

        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def log(self, message):
        
        # If file is empty, add header with column names
        if os.stat(self.logfile).st_size == 0:
            self.logger.debug(self.makeHeader(message))

        line = datetime.now().strftime("%Y, %m, %d, %H, %M, %S, %f, ") + message.__class__.__name__
        for parameter in message.getParameters():
            if parameter != None:
                line += (', ' + str(parameter.getValue()))
        self.logger.debug(line)

    @staticmethod
    def makeHeader(message):
        columns = "year, month, day, hour, minute, second, microsecond, message name"
        for parameter in message.getParameters():
            if parameter != None:
                columns += ", " + parameter.getName() + "["
                if (parameter.getUnit() != None):
                    columns += parameter.getUnit()
                else:
                    columns += "-"
                columns += "]"
        return columns