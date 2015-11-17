import unittest
from shico import utils as shU
import numpy as np


class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        windowSize = 15
        self.y1 = 1960
        self.y2 = 1970
        self.y0 = self.y1-windowSize
        self.yN = self.y1+windowSize
        self.yRange = np.linspace(self.y0, self.yN)

    def testJSD(self):
        self._doTests(shU.weightJSD)

    def testGaussian(self):
        self._doTests(shU.weightGauss)
        self._doTests(lambda y1, y2: shU.weightGauss(y1, y2, c=5))

    def testLinear(self):
        self._doTests(shU.weightLinear)
        self._doTests(lambda y1, y2: shU.weightLinear(y1, y2, a=5))

    def _doTests(self, f):
        self.assertEqual(f(self.y1, self.y1), 1,
                         'Should be 1 for the same number')
        self.assertEqual(f(self.y1, self.y1), 1,
                         'Should be symmetric')
        self.assertGreater(f(self.y1, self.y1), 0,
                           'Should be positive')

        # Test function in a range
        wRange = np.array([f(self.y1, yi) for yi in self.yRange])
        self.assertLessEqual(wRange.max(), 1,
                             'Should have upper bound 1')
        self.assertGreaterEqual(wRange.min(), 0,
                                'Should have lower bound 0')
