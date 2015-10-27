import unittest
import gensim
import shiftingVocabularyMonitor as shVM


class VocabularyMonitorTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.allModels = shVM.loadAllModels("word2vecModels/1950_????.w2v")

    def testLoad(self):
        self.assertGreater(len(self.allModels), 0,
                           "Should have at least 1 model")
        for label, model in self.allModels.iteritems():
            self.assertIsInstance(model, gensim.models.word2vec.Word2Vec,
                                  "Object should be a Word2Vec model")

    def testModelsWork(self):
        nItems = 5
        for label, model in self.allModels.iteritems():
            modelWords = model.vocab.keys()
            self.assertGreater(len(modelWords), 0,
                               "Model vocabulary should have at least 1 word")
            aWord = model.vocab.keys()[0]
            items = model.most_similar(aWord, topn=nItems)
            self.assertEqual(len(items), nItems,
                             "Model should produced at least %d items"
                             % nItems)
