import unittest
from bit_array import BitArray, BitArray2D, BitArrayIndexOutOfBoundsException

class TestBitArray(unittest.TestCase):
    def setUp(self):
        pass

    def test_bit_arraay_varying_bit_size(self):
        # Instantiate a few bit arrays with different size bits including 0
        for size in range(24):
            BitArray(size)

    def test_bit_array_check_bounds(self):
        ba = BitArray(10)
        good_values = range(10)
        bad_values = [-1, 11]
        for bad_value in bad_values:
            self.assertRaises(BitArrayIndexOutOfBoundsException,
                              lambda: ba._check_bounds(bad_value))
        try:
            for good_value in good_values:
                ba._check_bounds(good_value)
        except BitArrayIndexOutOfBoundsException:
            self.fail("BitArray._check_bounds should be in a valid range")

    def test_bit_array_get_set(self):
        ba = BitArray(10)
        for x in range(10):
            # Check initial value to be empty
            self.assertFalse(ba[x])
            # Change value
            ba[x] = 1
            # Check if value flipped correctly
            self.assertTrue(ba[x])

    def test_bit_array_length(self):
        for x in range(100):
            ba = BitArray(x)
            self.assertEqual(len(ba), x)

    def test_bit_array2d_get_set(self):
        ba_2d = BitArray2D(10, 10)
        test_range = [(x, y) for x in range(10) for y in range(10)]
        for x, y in test_range:
            self.assertFalse(ba_2d[x, y])
            ba_2d[x, y] = 1
            self.assertTrue(ba_2d[x, y])

    def test_bit_array2d_length(self):
        ba_2d = BitArray2D(10, 10)
        test_range = [(x, y) for x in range(10) for y in range(10)]
        for x, y in test_range:
            ba_2d = BitArray2D(x, y)
            self.assertEqual(len(ba_2d), x * y)
