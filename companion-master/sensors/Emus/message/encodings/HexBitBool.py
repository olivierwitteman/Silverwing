class HexBitBool(object):
    def __init__(self, indices):
        self._indices = indices

    def decode(self, hex):
        length = len(hex) * 4
        decoded = bin(int(hex, 16))[2:].zfill(length)
        booleans = list()
        for i in range(length):
            booleans.append(str(i) + ':' + decoded[length - 1 - i])
        return '; '.join([booleans[i] for i in self._indices])
