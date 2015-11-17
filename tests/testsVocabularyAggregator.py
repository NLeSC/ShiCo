import unittest


class Test2(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass

    def testFailed(self):
        self.assertTrue(True)
