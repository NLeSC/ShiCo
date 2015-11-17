import unittest
import gensim
from shico import VocabularyMonitor as shVM


class VocabularyMonitorTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.vm = shVM()
        self.vm.loadAllModels('word2vecModels/195[0-3]_????.w2v')

    def testLoad(self):
        self.assertGreater(len(self.vm._models), 0,
                           'Should have at least 1 model')
        for label, model in self.vm._models.iteritems():
            self.assertIsInstance(model, gensim.models.word2vec.Word2Vec,
                                  'Object should be a Word2Vec model')

    def testModelsWork(self):
        nItems = 5
        for label, model in self.vm._models.iteritems():
            modelWords = model.vocab.keys()
            self.assertGreater(len(modelWords), 0,
                               'Model vocabulary should have at least 1 word')
            aWord = model.vocab.keys()[0]
            items = model.most_similar(aWord, topn=nItems)
            self.assertEqual(len(items), nItems,
                             'Model should produced at least %d items'
                             % nItems)

    def testTrackTermsGivesResults(self):
        seedTerms = 'x'
        maxTerms = 5
        results = self.vm.trackClouds(seedTerms, maxTerms=maxTerms)
        resultPeriods = results.keys()
        modelPeriods = self.vm._models.keys()
        self.assertEqual(len(resultPeriods), len(modelPeriods),
                         'There should be results for every time period')

        for period, result in results.iteritems():
            self.assertEqual(len(result), maxTerms,
                             'Every period should have %d terms' % maxTerms)
            for item in result:

                self.assertEqual(len(item), 2,
                                 'Results should be word,score tuples')

    def testTrackTermsOutlinks(self):
        seedTerms = 'x'
        maxTerms = 5

        rOut = self.vm.trackClouds(seedTerms, maxTerms=maxTerms,
                                   algorithm='outlinks')
        rIn = self.vm.trackClouds(seedTerms, maxTerms=maxTerms,
                                  algorithm='inlinks')
        rNA = self.vm.trackClouds(seedTerms, maxTerms=maxTerms,
                                  algorithm='non-adaptive')

        for key in rOut.keys():
            self.assertEqual(len(rOut[key]), len(rIn[key]),
                             'Outlinks and Inlinks should generate equal ' +
                             'number ofresults')
            self.assertEqual(len(rIn[key]), len(rNA[key]),
                             'Inlinks and non-adapt. should generate equal ' +
                             'number ofresults')

    def testTrackTermsKeys(self):
        seedTerms = 'x'
        keys = self.vm._models.keys()
        print keys
        sKey = keys[1]
        eKey = keys[-1]

        results = self.vm.trackClouds(seedTerms, startKey=sKey)
        self.assertGreater(len(keys), len(results),
                           'Should have less results than number of models')

        results = self.vm.trackClouds(seedTerms, endKey=eKey)
        self.assertGreater(len(keys), len(results),
                           'Should have less results than number of models')

        results = self.vm.trackClouds(seedTerms, startKey=sKey, endKey=eKey)
        self.assertGreater(len(keys), len(results),
                           'Should have less results than number of models')
