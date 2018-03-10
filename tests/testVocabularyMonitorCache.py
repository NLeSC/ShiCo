from shico import VocabularyMonitor as shVM
from shico.vocabularymonitor import CachedW2VModelEvaluator

from vocabularyMonitorHelper import VocabularyMonitorBase

class VocabularyMonitorTestCache(VocabularyMonitorBase):

    # Do run these unit test
    __test__ = True

    '''Tests for VocabularyMonitor using cache'''

    def __init__(self, *args, **kwargs):
        super(VocabularyMonitorBase, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(self):
        # Fake models! Only made so we can do unittests
        self.vm = shVM('tests/w2vModels/*.w2v', useCache=True, useMmap=False,
                w2vFormat=True)

    def testLoadClass(self):
        '''Test models are of expected class'''
        for label, model in self.vm._models.iteritems():
            self.assertIsInstance(model, CachedW2VModelEvaluator,
                                  'Object should be a CachedW2VModelEvaluator')
