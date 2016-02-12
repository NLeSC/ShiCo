import unittest
import gensim
from shico import VocabularyMonitor as shVM


class VocabularyMonitorTest(unittest.TestCase):
    '''Tests for VocabularyMonitor'''

    @classmethod
    def setUpClass(self):
        # Fake models! Only made so we can do unittests
        self.vm = shVM('tests/w2vModels/*.w2v')

    def testLoad(self):
        '''Test loading of w2v models'''
        self.assertGreater(len(self.vm._models), 0,
                           'Should have at least 1 model')
        for label, model in self.vm._models.iteritems():
            self.assertIsInstance(model, gensim.models.word2vec.Word2Vec,
                                  'Object should be a Word2Vec model')

    def testModelsWork(self):
        '''Test that w2v models produce results.'''
        nItems = 5
        for label, model in self.vm._models.iteritems():
            modelWords = model.vocab.keys()
            self.assertGreater(len(modelWords), 0,
                               'Model vocabulary should have at least 1 word')
            aWord = model.vocab.keys()[0]
            items = model.most_similar(aWord, topn=nItems)
            self.assertEqual(len(items), nItems,
                             'Model should produced %d items' % nItems)

    def testTrackTermsGivesResults(self):
        '''Test that trackClouds produces results in the expected format.'''
        seedTerms = 'x'
        maxTerms = 5
        results, _ = self.vm.trackClouds(seedTerms, maxTerms=maxTerms)
        resultPeriods = results.keys()
        modelPeriods = self.vm._models.keys()
        self.assertEqual(len(resultPeriods), len(modelPeriods),
                         'There should be results for every time period')

        for period, result in results.iteritems():
            self.assertEqual(len(result), maxTerms,
                             'Every period should have %d terms. %s does not'
                             % (maxTerms, period))
            for item in result:
                self.assertEqual(len(item), 2,
                                 'Results should be word,score tuples')

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
        nTerms = [ 1, 2, 5, 10 ]

        for maxTerms in nTerms:
            results, _ = self.vm.trackClouds(seedTerms, maxTerms=maxTerms)
            for period, result in results.iteritems():
                self.assertEqual(len(result), maxTerms,
                                 'Every period should have %d terms. %s does not'
                                 % (maxTerms, period))

    def testTrackTermsKeys(self):
        '''Test that using range selection works.'''
        seedTerms = 'x'
        keys = self.vm._models.keys()
        print keys
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

    def testTrackTermMinDist(self):
        '''Test that min distance gives only terms with distance greater than
        given distance'''
        seedTerms = 'x'
        minDists = [ 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0 ]

        for minDist in minDists:
            _, yLinks = self.vm.trackClouds(seedTerms, minDist=minDist)
            for links in yLinks.itervalues():
                for seed, terms in links.iteritems():
                    dists = [dist for word,dist in terms if word!=seed]
                    if len(dists)>0:
                        self.assertGreater(min(dists), minDist,
                                   ('Minimum possible distance should' +
                                   ' be %.2f but seed %s is %.2f of ' +
                                   'some terms')%(minDist, seed, min(dists)))

    def testTrackTermNonAdaptive(self):
        '''Test that non-adaptive algorithms work as expected. '''
        # For non-adaptive, seeds should always be the same
        seedTerms = [ 'x' ]

        _, yLinks = self.vm.trackClouds(seedTerms, algorithm='non-adaptive')
        for period, links in yLinks.iteritems():
            self.assertEqual(seedTerms, links.keys(),
                             'Seeds used should remain constant for all periods'
                             ' but they differ for period %s'%period)

    def testTrackTermAdaptive(self):
        '''Test that adaptive algorithms work as expected.'''
        # For adaptive, seeds in T(n) should be the same as terms in T(n-1)
        seedTerms = 'x'

        yTerms, yLinks = self.vm.trackClouds(seedTerms, algorithm='adaptive')

        periods = list(yTerms.keys())   # T
        for n in range(1,len(periods)):
            seedsTn = yLinks[periods[n]].keys()
            termsTn_1 = [ w for w,_ in yTerms[periods[n-1]] ]
            # Compare seeds of T[n] vs terms of T[n-1],'
            self.assertEqual(sorted(termsTn_1), sorted(seedsTn),
                             'Seeds of period %s should match terms of period %s'
                             % (periods[n], periods[n-1]))

    def testTrackTermTermsFormat(self):
        '''Test that links are correct.'''
        self.fail('test not implemented')

    def testTrackTermLinksFormat(self):
        '''Test that links are correct.'''
        # _, links = self.vm.trackClouds(seedTerms, startKey=sKey)
        # TODO: validate links
        self.fail('test not implemented')
