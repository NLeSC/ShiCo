import gensim

from shico import VocabularyMonitor as shVM

from vocabularyMonitorHelper import VocabularyMonitorBase

class VocabularyMonitorGensimTest(VocabularyMonitorBase):

    # Do run these unit test
    __test__ = True

    '''Tests for VocabularyMonitor'''

    def __init__(self, *args, **kwargs):
        super(VocabularyMonitorBase, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(self):
        # Fake models! Only made so we can do unittests
        self.vm = shVM('tests/gensimModels/*.w2v', w2vFormat=False, useCache=False)

    def testLoadClass(self):
        '''Test models are of expected class'''
        for label, model in self.vm._models.iteritems():
            self.assertIsInstance(model, gensim.models.word2vec.Word2Vec,
                                  'Object should be a Word2Vec model')
