import unittest
from shico.vocabularyembedding import doSpaceEmbedding
from shico import VocabularyMonitor as shVM
from shico import VocabularyAggregator as shVA

class VocabularyEmbeddingTest(unittest.TestCase):

    '''Tests for VocabularyEmbedding'''

    @classmethod
    def setUpClass(self):
        # Fake models! Only made so we can do unittests
        vm = shVM('tests/w2vModels/*.w2v', useCache=False, useMmap=False,
                w2vFormat=True)
        results, links = vm.trackClouds('x')
        agg = shVA(yearsInInterval=1)
        aggResults, aggMetadata = agg.aggregate(results)
        self.embedded = doSpaceEmbedding(vm, results, aggMetadata)

    def testLoad(self):
        '''Test word embeddings'''
        self.assertGreater(len(self.embedded), 0,
                           'Dictionary should contain some years')
        for year, embeddings in self.embedded.iteritems():
            self.assertGreater(len(embeddings), 0,
                               'Embeddings should contain some words')
