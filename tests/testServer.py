import unittest
import json
import shico.server
import shico.server.app
from shico.server.utils import initApp

class ServerTest(unittest.TestCase):

    '''Tests for server'''
    @classmethod
    def setUpClass(self):
        # Fake models! Only made so we can do unittests
        initApp(shico.server.app.app, files='tests/w2vModels/*.w2v', binary=True,
            useMmap=False, w2vFormat=True, cleaningFunctionStr=None)
        self.app = shico.server.app.app.test_client()

    def testTrackService(self):
        '''Test calls to /track/<terms>. Response should be valid JSON with the
        correct structure.'''
        terms = 'x'
        resp = self.app.get('/track/' + terms)

        self.assertEqual(resp.status_code, 200,
                         'Response should be code 200')
        try:
            jsonStr = resp.data
            respJson = json.loads(jsonStr)
        except:
            self.fail('Response should be valid JSON')

        keyList = [ 'stream', 'networks', 'embedded', 'vocabs' ]
        respKeys = respJson.keys()
        for key in keyList:
            if key not in respKeys:
                self.fail('Missing key: ' + key)

        self._checkStream(respJson['stream'])
        self._checkNetwork(respJson['networks'])
        self._checkEmbedded(respJson['embedded'])
        self._checkVocab(respJson['vocabs'])

    def _checkStream(self, data):
        '''Check the structure of the stream data is correct.'''
        wordsPerResult = None

        for year,wordList in data.iteritems():
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

    def _checkNetwork(self, data):
        '''Check the structure of the network data is correct.'''
        for year, net in data.iteritems():
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

    def _checkEmbedded(self, data):
        '''Check the structure of the embedded data is correct.'''
        for year, embeddings in data.iteritems():
            self.assertGreater(len(embeddings), 0,
                               'List should contain some embeddings')
            for item in embeddings:
                self.assertEqual(sorted(item.keys()), sorted(['word', 'x', 'y']),
                                 'Embeddings should contain "word", "x" and "y"'
                                 'but %s does not' % year)

    def _checkVocab(self, data):
        '''Check the structure of the vocabularies data is correct.'''
        for year, seedVocabs in data.iteritems():
            self.assertGreater(len(seedVocabs), 0,
                               'List should contain some seed-vocabulary dictionaries')

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
