import unittest
import json
import shico.server


class ServerTest(unittest.TestCase):
    '''Tests for server'''
    @classmethod
    def setUpClass(self):
        # Fake models! Only made so we can do unittests
        shico.server.initApp('tests/w2vModels/*.w2v', True)
        self.app = shico.server.app.test_client()

    def testTrackService(self):
        '''Test calls to /track/<terms>. Response should be valid JSON.'''
        terms = 'x'
        resp = self.app.get('/track/' + terms)

        self.assertEqual(resp.status_code, 200,
                         'Response should be code 200')
        try:
            jsonStr = resp.data
            respJson = json.loads(jsonStr)
        except:
            self.fail('Response should be valid JSON')

        years = respJson.keys()
        self.assertGreater(len(years), 0,
                           'Response should produce response for several yearly models')

        wordsPerResult = None
        for year,wordList in respJson.iteritems():
            nWordsInList = len(wordList)
            self.assertGreater(nWordsInList, 0,
                               'Word lists should contain words')

            if wordsPerResult is None:
                wordsPerResult = nWordsInList
            else:
                self.assertEqual(wordsPerResult, nWordsInList,
                                 'All results should contain the same number of words')

            for item in wordList:
                self.assertEqual(len(item), 2,
                                 'Items in wordList should be word/weight pairs')
