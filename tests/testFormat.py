import unittest
from sortedcontainers import SortedDict
from shico import format as fmt


class TestFormat(unittest.TestCase):

    '''Tests for formatting functions'''
    @classmethod
    def setUpClass(self):
        self._vocab = SortedDict({
            '1950_1959': [('w1', 1.0), ('w2', 1.0)],
            '1951_1960': [('w3', 1.0), ('w4', 1.0)],
            '1952_1961': [('w5', 1.0), ('w6', 1.0)],
            '1953_1962': [('w7', 1.0), ('w8', 1.0)]
        })
        self._links = SortedDict({
            '1950_1959': {'w1': [('w1', 0.0), ('w2', 1.0)]},
            '1951_1960': {'w3': [('w3', 0.0), ('w4', 1.0)]},
            '1952_1961': {'w5': [('w5', 0.0), ('w6', 1.0)]},
            '1953_1962': {'w7': [('w7', 0.0), ('w8', 1.0)]}
        })
        self._aggVocab = SortedDict({
            '1954': [('w1', 1.0), ('w2', 1.0)],
            '1955': [('w3', 1.0), ('w4', 1.0)],
            '1956': [('w5', 1.0), ('w6', 1.0)],
            '1957': [('w7', 1.0), ('w8', 1.0)]
        })
        self._aggPeriods = SortedDict({
            '1954': ['1950_1959'],
            '1955': ['1951_1960'],
            '1956': ['1952_1961'],
            '1957': ['1953_1962']
        })

    def testGetRangeMiddle(self):
        '''Test finding middle of range works'''
        self.assertEqual(fmt.getRangeMiddle('1951_1960'), 1955,
                         'Middle of 50s decade should be 1955')
        self.assertEqual(fmt.getRangeMiddle('1959_1968', '1962_1971'), 1965,
                         'Middle of 60s decade should be 1965')

    def testYearlyNetwork(self):
        '''Test building of yearly networks'''
        networks = fmt.yearlyNetwork(self._aggPeriods, self._aggVocab,
                                     self._vocab, self._links)

        self.assertEqual(sorted(networks.keys()), list(self._aggVocab.keys()),
                         'A network should be created for each aggregated '
                         'vocabulary')

        self.assertEqual(
            sorted(networks.keys()), list(self._aggPeriods.keys()),
            'A network should be created for each aggregation period')
        for year, net in networks.iteritems():
            self.assertEqual(sorted(net.keys()), sorted(['nodes', 'links']),
                             'Each network should contain "nodes" and "links"'
                             'but %s does not' % year)
            for node in net['nodes']:
                self.assertEqual(sorted(node.keys()),
                                 sorted(['name', 'type', 'count']),
                                 'Each node should contain "name", "type" and '
                                 '"count", but a node on %s does not' % year)
            for link in net['links']:
                self.assertEqual(sorted(link.keys()),
                                 sorted(['source', 'target', 'value']),
                                 'Each link should contain "source", "target" '
                                 'and "value", but a link on %s does not'
                                 % year)

    def testYearTuplesAsDict(self):
        '''Test converting tuple dictionary to nested dictionary'''
        dicts = fmt.yearTuplesAsDict(self._aggVocab)
        self.assertEqual(sorted(dicts.keys()), list(self._aggVocab.keys()),
                         'A dictionary should be created for each aggregated '
                         'vocabulary')
        for year, d in dicts.iteritems():
            self.assertEqual(len(d), len(self._aggVocab[year]),
                             'Dict should have same number of items as '
                             'aggregated vocabulary but %s does not' % year)

    def testWordLocationAsDict(self):
        '''Test creating word-location dictionary'''
        word = 'w1'
        loc = (0,1)
        d = fmt.wordLocationAsDict(word,loc)
        self.assertIsInstance(d, dict,' Should be a dictionary')
        self.assertEqual(sorted(d.keys()),
                         sorted(['word', 'x', 'y']),
                         'Should contain "word", "x" and "y"')
