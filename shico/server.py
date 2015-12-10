'''ShiCo server.

Usage:
  server.py  [-f FILES] [-n]

  -f FILES         Path to word2vec model files (glob format is supported)
                   [default: word2vecModels/195[0-1]_????.w2v]
  -n,--non-binary  w2v files are NOT binary.
'''
from docopt import docopt

from flask import Flask, jsonify
from flask_restful import reqparse

from vocabularymonitor import VocabularyMonitor

app = Flask(__name__)
_vm = None


def initApp(files, binary):
    '''Initialize Flask app by loading VocabularyMonitor.

    files    Files to be loaded by VocabularyMonitor
    binary   Whether files are binary
    '''
    global _vm
    _vm = VocabularyMonitor(files, binary)

# trackClouds parameters
trackParser = reqparse.RequestParser()
trackParser.add_argument('maxTerms', type=int, default=10)
trackParser.add_argument('maxRelatedTerms', type=int, default=10)
trackParser.add_argument('startKey', type=str, default=None)
trackParser.add_argument('endKey', type=str, default=None)
trackParser.add_argument('minDist', type=float, default=0.0)
trackParser.add_argument('wordBoost', type=float, default=1.0)
trackParser.add_argument('forwards', type=bool, default=True)
trackParser.add_argument('sumDistances', type=bool, default=False)
trackParser.add_argument('algorithm', type=str, default='inlinks')


@app.route('/track/<terms>')
def trackWord(terms):
    '''VocabularyMonitor.trackClouds service. Expects a list of terms to be
    sent to the Vocabulary monitor, and returns a JSON representation of the
    response.'''
    defaults = trackParser.parse_args()
    termList = terms.split(',')
    results = \
        _vm.trackClouds(termList, maxTerms=defaults['maxTerms'],
                        maxRelatedTerms=defaults['maxRelatedTerms'],
                        startKey=defaults['startKey'],
                        endKey=defaults['endKey'],
                        minDist=defaults['minDist'],
                        wordBoost=defaults['wordBoost'],
                        forwards=defaults['forwards'],
                        sumDistances=defaults['sumDistances'],
                        algorithm=defaults['algorithm'],
                        )
    return jsonify(results)

if __name__ == '__main__':
    arguments = docopt(__doc__)
    initApp(arguments['-f'], not arguments['--non-binary'])
    # app.debug = True
    app.run(host='0.0.0.0')
