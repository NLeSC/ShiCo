import unittest
from shico import utils as shU
import numpy as np


class TestUtils(unittest.TestCase):
    '''Tests for utils'''
    @classmethod
    def setUpClass(self):
        windowSize = 15
        self.y1 = 1960
        self.y2 = 1970
        self.y0 = self.y1-windowSize
        self.yN = self.y1+windowSize
        self.yRange = np.linspace(self.y0, self.yN)

    def testJSD(self):
        '''Test JSD weighting function'''
        self._doTests(shU.weightJSD, 'JSD')

    def testGaussian(self):
        '''Test Gaussian weighting function'''
        self._doTests(shU.weightGauss, 'Gaussian')
        # Test with non-default C
        self._doTests(lambda y1, y2: shU.weightGauss(y1, y2, c=5), 'Gaussian')

    def testLinear(self):
        '''Test linear weighting function'''
        self._doTests(shU.weightLinear, 'Linear')
        # Test with non-default A
        self._doTests(lambda y1, y2: shU.weightLinear(y1, y2, a=5), 'Linear')

    def _doTests(self, f, name):
        ''' Apply sanity checks to the given weighting function. '''
        self.assertEqual(f(self.y1, self.y1), 1,
                         name + ' should be 1 for the same number')
        self.assertEqual(f(self.y1, self.y1), 1,
                         name + ' should be symmetric')
        self.assertGreater(f(self.y1, self.y1), 0,
                           name + ' should be positive')

        # Test function in a range
        wRange = np.array([f(self.y1, yi) for yi in self.yRange])
        self.assertLessEqual(wRange.max(), 1,
                             name + ' should have upper bound 1')
        self.assertGreaterEqual(wRange.min(), 0,
                                name + ' should have lower bound 0')
