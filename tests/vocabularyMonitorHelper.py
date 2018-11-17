import unittest
import six

class VocabularyMonitorBase(unittest.TestCase):

    # Do not run this unit test
    __test__ = False

    def __init__(self):
        self.vm = None

    '''Tests for VocabularyMonitor'''

    def testLoad(self):
        '''Test loading of w2v models'''
        self.assertGreater(len(self.vm._models), 0,
                           'Should have at least 1 model')

    def testModelsWork(self):
        '''Test that w2v models produce results.'''
        nItems = 5
        for label, model in self.vm._models.iteritems():
            wv = model.wv if hasattr(model, 'wv') else model
            modelWords = wv.vocab.keys()
            self.assertGreater(len(modelWords), 0,
                               'Model vocabulary should have at least 1 word')
            aWord = wv.vocab.keys()[0]
            items = wv.most_similar(aWord, topn=nItems)
            self.assertEqual(len(items), nItems,
                             'Model should produced %d items' % nItems)

    def testTrackTermsGivesResults(self):
        '''Test that trackClouds produces results in the expected format.'''
        seedTerms = 'x'
        yTerms, yLinks = self.vm.trackClouds(seedTerms)
        periods = yTerms.keys()
        modelPeriods = self.vm._models.keys()
        self.assertEqual(len(yTerms), len(modelPeriods),
                         'There should be terms for every time period')
        self.assertEqual(len(yLinks), len(modelPeriods),
                         'There should be links for every time period')

        for period in periods:
            self.assertGreater(len(yTerms[period]), 0,
                               'Every period should have some terms. %s does '
                               'not' % period)
            self.assertGreater(len(yLinks[period]), 0,
                               'Every period should have some links. %s does '
                               'not' % period)

    def testTrackTermsCountResults(self):
        '''Test that different algorithms still produce the same number of
        results'''
        seedTerms = 'x'
        maxTerms = 5

        rIn, _ = self.vm.trackClouds(seedTerms, maxTerms=maxTerms,
                                     algorithm='adaptive')
        rNA, _ = self.vm.trackClouds(seedTerms, maxTerms=maxTerms,
                                     algorithm='non-adaptive')

        for key in rIn.keys():
            self.assertEqual(len(rIn[key]), len(rNA[key]),
                             'adaptive and non-adaptive. should generate ' +
                             'equal number of results')

    def testTrackTermMaxTerms(self):
        '''Test that maxTerms limits the number of results'''
        seedTerms = 'x'
        nTerms = [1, 2, 5, 10]

        for maxTerms in nTerms:
            results, _ = self.vm.trackClouds(seedTerms, maxTerms=maxTerms)
            for period, result in results.iteritems():
                self.assertEqual(len(result), maxTerms,
                                 'Every period should have %d terms. %s does '
                                 'not' % (maxTerms, period))

    def testTrackTermsKeys(self):
        '''Test that using range selection works.'''
        seedTerms = 'x'
        keys = self.vm._models.keys()
        sKey = keys[1]
        eKey = keys[-1]

        results, _ = self.vm.trackClouds(seedTerms, startKey=sKey)
        self.assertGreater(len(keys), len(results),
                           'Should have less results than number of models')

        results, _ = self.vm.trackClouds(seedTerms, endKey=eKey)
        self.assertGreater(len(keys), len(results),
                           'Should have less results than number of models')

        results, _ = self.vm.trackClouds(seedTerms, startKey=sKey, endKey=eKey)
        self.assertGreater(len(keys), len(results),
                           'Should have less results than number of models')

    def testTrackTermMinSim(self):
        '''Test that min distance gives only terms with distance greater than
        given distance'''
        seedTerms = 'x'
        minSims = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

        for minSim in minSims:
            _, yLinks = self.vm.trackClouds(seedTerms, minSim=minSim)
            for links in yLinks.itervalues():
                for seed, terms in links.iteritems():
                    dists = [dist for word, dist in terms if word != seed]
                    if len(dists) > 0:
                        self.assertGreater(min(dists), minSim,
                                           'Minimum possible distance should '
                                           'be %.2f but seed %s is %.2f of '
                                           'some terms' % (minSim, seed,
                                                           min(dists)))

    def testTrackTermNonAdaptive(self):
        '''Test that non-adaptive algorithms work as expected. '''
        # For non-adaptive, seeds should always be the same
        seedTerms = ['x']

        _, yLinks = self.vm.trackClouds(seedTerms, algorithm='non-adaptive')
        for period, links in yLinks.iteritems():
            self.assertEqual(seedTerms, links.keys(),
                             'Seeds used should remain constant for all '
                             'periods but they differ for period %s' % period)

    def testTrackTermAdaptive(self):
        '''Test that adaptive algorithms work as expected.'''
        # For adaptive, seeds in T(n) should be the same as terms in T(n-1)
        seedTerms = 'x'

        yTerms, yLinks = self.vm.trackClouds(seedTerms, algorithm='adaptive')

        periods = list(yTerms.keys())   # T
        for n in range(1, len(periods)):
            seedsTn = yLinks[periods[n]].keys()
            termsTn_1 = [w for w, _ in yTerms[periods[n - 1]]]
            # Compare seeds of T[n] vs terms of T[n-1],'
            self.assertEqual(sorted(termsTn_1), sorted(seedsTn),
                             'Seeds of period %s should match terms of '
                             'period %s' % (periods[n], periods[n - 1]))

    def testTrackTermTermsFormat(self):
        '''Test that terms are in correct format.'''
        seedTerms = 'x'
        yTerms, _ = self.vm.trackClouds(seedTerms)

        for period, result in yTerms.iteritems():
            for pair in result:
                self.assertEqual(len(pair), 2,
                                 'Results should be word,score tuples')
                self.assertTrue(isinstance(pair[0], six.string_types),
                                'First element of result tuple should be '
                                'string')
                self.assertTrue(isinstance(pair[1], float),
                                'Second element of result tuple should be '
                                'float')

    def testTrackTermLinksFormat(self):
        '''Test that links are in correct format.'''
        seedTerms = 'x'
        _, yLinks = self.vm.trackClouds(seedTerms)

        for period, links in yLinks.iteritems():
            self.assertTrue(isinstance(links, dict),
                            'Should contain a dictionary')
            for seed, terms in links.iteritems():
                self.assertTrue(isinstance(seed, six.string_types),
                                'Seed should be a string')
                for pair in terms:
                    self.assertEqual(len(pair), 2,
                                     'Links should be word,score tuples')
                    self.assertTrue(isinstance(pair[0], six.string_types),
                                    'First element of link tuple should be '
                                    'string')
                    self.assertTrue(isinstance(pair[1], float),
                                    'Second element of link tuple should be '
                                    'float')
