import numpy as np

from sensors.Emus.message.encodings.HexDec import HexDec


class HexDecByteArray(object):
    def __init__(self, offset=0, multiplier=1, dtypeIn=np.uint32, dtypeOut=np.uint32):
        self._offset = offset
        self._multiplier = multiplier
        self._dtypeIn = dtypeIn
        self._dtypeOut = dtypeOut

    def decode(self, hex):
        hexDec = HexDec(self._offset, self._multiplier, self._dtypeIn, self._dtypeOut)
        data = list()
        for i in range(0, len(hex), 2):
            datapoint = hexDec.decode(hex[i: i + 2])
            data.append(datapoint)
        return data
