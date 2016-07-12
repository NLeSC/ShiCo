import unittest
from shico.extras import cleanTermList


class ExtrasTest(unittest.TestCase):
    '''Tests extras package.'''

    def testCleanTermList(self):
        '''Test cleanTermList function.'''
        self.assertEqual(cleanTermList([]), [],
                         'Empty list should still be empty')

        uniqueList = [('alice', 0), ('bob', 0), ('charles', 0)]
        self.assertEqual(cleanTermList(uniqueList), uniqueList,
                         'List with unique entries should remain unchanged')

        withRepeat = [('alice', 0), ('bob', 0), ('bob', 0), ('charles', 0)]
        cleanedList = cleanTermList(withRepeat)
        self.assertNotEqual(cleanedList, withRepeat,
                            'List with repeats should be changed')
        self.assertLess(len(cleanedList), len(withRepeat),
                        'Cleaned version should have less items')

        withSimilars = [('SomeLongWord1', 0), ('SomeLongWord2', 0)]
        cleanedList = cleanTermList(withSimilars)
        self.assertNotEqual(cleanedList, withSimilars,
                            'List with similar items should be changed')
        self.assertLess(len(cleanedList), len(withSimilars),
                        'Cleaned version should have less items')
