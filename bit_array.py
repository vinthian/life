import math

class BitArrayIndexOutOfBoundsException(Exception):
    pass

class BitArray(object):
    def __init__(self, size):
        self._bits = size
        self._bytes = math.ceil(size / 8)
        self._data = bytearray(self._bytes)

    def _check_bounds(self, i):
        try:
            assert (i >= 0 and i < self._bits) == True
        except AssertionError:
            raise BitArrayIndexOutOfBoundsException

    def __getitem__(self, i):
        self._check_bounds(i)
        return not (self._data[i // 8] & (1 << (i % 8)) == 0)

    def __setitem__(self, i, value):
        self._check_bounds(i)
        assert isinstance(value, int)
        if value:
            self._data[i // 8] |= (1 << (i % 8))
        else:
            self._data[i // 8] &= ~(1 << (i % 8))


class BitArray2D(BitArray):
    def __init__(self, width, height):
        super().__init__(width * height)
        self._width, self._height = width, height

    def __getitem__(self, coords):
        return super().__getitem__(self._index(*coords))

    def __setitem__(self, coords, value):
        super().__setitem__(self._index(*coords), value)

    def _index(self, x, y):
        return self._width * y + x
