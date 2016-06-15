import unittest
import json
import shico.server


class ServerTest(unittest.TestCase):

    '''Tests for server'''
    @classmethod
    def setUpClass(self):
        # Fake models! Only made so we can do unittests
        shico.server.initApp('tests/w2vModels/*.w2v', True, None)
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
                           'Response should produce response for several ' +
                           'yearly models')

        wordsPerResult = None
        for year, wordList in respJson.iteritems():
            nWordsInList = len(wordList)
            self.assertGreater(nWordsInList, 0,
                               'Word lists should contain words')

            if wordsPerResult is None:
                wordsPerResult = nWordsInList
            else:
                self.assertEqual(wordsPerResult, nWordsInList,
                                 'All results should contain the same number' +
                                 ' of words')

            for word in wordList:
                self.assertIsNotNone(wordList[word],
                                     'Items in wordList should be word: ' +
                                     'weight dictionary entries')

    def testAppData(self):
        '''Test calls to /load-settings. Response should be valid JSON.'''
        resp = self.app.get('/load-settings')

        self.assertEqual(resp.status_code, 200,
                         'Response should be code 200')
        try:
            jsonStr = resp.data
            respJson = json.loads(jsonStr)
        except:
            self.fail('Response should be valid JSON')

        for key in ['cleaning', 'years']:
            self.assertTrue(key in respJson,
                            '"' + key + '" should be a key in the response')

        years = respJson['years']
        for key in ['first', 'last', 'values']:
            self.assertTrue(key in years,
                            '"' + key + '" should be a key in the response')

        for key in ['first', 'last']:
            self.assertTrue(str(years[key]) in years['values'],
                            '"' + key + '" should be a key in values')
