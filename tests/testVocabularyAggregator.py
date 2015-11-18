import unittest
from sortedcontainers import SortedDict
from shico import VocabularyAggregator as shVA

class TestVocabularyAggregation(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self._data = SortedDict({
            '1950_1959': [(u'bevrijding', 1), (u'wereldoorlog', 1),
                          (u'oorlogen', 1), (u'burgeroorlog', 1),
                          (u'oorlof', 1), (u'bevr\xfcding', 1), (u'ooriog', 1),
                          (u'hongerwinter', 1), (u'oorlogse', 1), ('oorlog', 1)
                          ],
            '1951_1960': [(u'oorlog', 8), (u'bevrijding', 4),
                          (u'souvereiniteitsoverdracht', 3), (u'oorloe', 3),
                          (u'ooriogse', 3), (u'bevr\xfcding', 3),
                          (u'ooriog', 3), (u'oorlogsjaren', 3), (u'corlog', 2),
                          (u'boerenoorlog', 2)
                          ],
            '1952_1961': [(u'oorlog', 5), (u'bevrijding', 4),
                          (u'geboorteplek', 4), (u'bevryding', 4),
                          (u'herstelperiode', 3), (u'bezettingsjaren', 3),
                          (u'oorlogse', 3), (u'crisisperiode', 3),
                          (u'bevr\xfcding', 3), (u'oorlogsjaren', 3)
                          ],
            '1953_1962': [(u'oorlog', 6), (u'bevrijding', 5),
                          (u'geboorteplek', 4), (u'bevr\xfcding', 4),
                          (u'souvereiniteitsoverdracht', 3),
                          (u'bevrijdingsoorlog', 3), (u'bezettingsjaren', 3),
                          (u'wereldoorlog', 3), (u'oorlogse', 3),
                          (u'bevryding', 3)
                          ],
        })

    def testWeightingFunctions(self):
        for f in ['Gaussian', 'JSD',  'Linear']:
            try:
                agg = shVA(weighF=f)
                aggData = agg.aggregate(self._data)
            except:
                self.fail(f + ' should be a valid function')

        try:
            agg = shVA(weighF=lambda t1, t2: 0)
            aggData = agg.aggregate(self._data)
        except:
            self.fail('Lambda function should be a valid function')

        with self.assertRaises(Exception):
            agg5 = shVA(weighF='Unknown')
            aggData5 = agg5.aggregate(self._data)

    def testWordsPerYear(self):
        nWordsPerYear = 5
        agg = shVA(nWordsPerYear=nWordsPerYear)
        aggData = agg.aggregate(self._data)
        for words in aggData.itervalues():
            self.assertEqual(len(words), nWordsPerYear,
                             'Each year should have %d words ' % nWordsPerYear)

    def testYearsInInterval(self):
        agg = shVA(yearsInInterval=1)
        aggData = agg.aggregate(self._data)
        self.assertEqual(len(aggData.keys()), len(self._data.keys()),
                         'Should have same number of keys as original data')

        agg = shVA(yearsInInterval=2)
        aggData = agg.aggregate(self._data)
        self.assertEqual(len(aggData.keys()), len(self._data.keys())/2,
                         'Should have 1/2 the number of keys as original data')

        agg = shVA(yearsInInterval=len(self._data.keys()))
        aggData = agg.aggregate(self._data)
        self.assertEqual(len(aggData.keys()), 1,
                         'Should have only 1 key')
