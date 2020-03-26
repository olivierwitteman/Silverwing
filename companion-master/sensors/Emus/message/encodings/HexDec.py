import numpy as np


class HexDec(object):
    def __init__(self, offset=0, multiplier=1, dtypeIn=np.uint32, dtypeOut=np.uint32):
        self._offset = offset
        self._multiplier = multiplier
        self._dtypeIn = dtypeIn
        self._dtypeOut = dtypeOut

    def decode(self, hex):
        return self._dtypeOut(self._dtypeIn(int(hex, 16) + self._offset) * self._multiplier)