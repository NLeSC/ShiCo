'''ShiCo server.

Usage:
  server.py  [-f FILES] [-n] [-d]

  -f FILES         Path to word2vec model files (glob format is supported)
                   [default: word2vecModels/195[0-1]_????.w2v]
  -n,--non-binary  w2v files are NOT binary.
  -d               Run in development mode (debug mode).
'''
from docopt import docopt

from flask import Flask, jsonify
from flask_restful import reqparse
from flask.ext.cors import CORS

from vocabularymonitor import VocabularyMonitor
from vocabularyaggregator import VocabularyAggregator

from format import yearlyNetwork, getRangeMiddle, yearTuplesAsDict

app = Flask(__name__)
CORS(app)
_vm = None


def validatestr(value):
    try:
        s = str(value)
        if len(s) == 0:
            return None
        return s
    except:
        raise ValueError


def initApp(files, binary):
    '''Initialize Flask app by loading VocabularyMonitor.

    files    Files to be loaded by VocabularyMonitor
    binary   Whether files are binary
    '''
    global _vm
    _vm = VocabularyMonitor(files, binary)
    # _vm = "VocabularyMonitor(files, binary)"

# trackClouds parameters

# VocabularyMonitor parameters:
trackParser = reqparse.RequestParser()
trackParser.add_argument('maxTerms', type=int, default=10)
trackParser.add_argument('maxRelatedTerms', type=int, default=10)
trackParser.add_argument('startKey', type=validatestr, default=None)
trackParser.add_argument('endKey', type=validatestr, default=None)
trackParser.add_argument('minDist', type=float, default=0.0)
trackParser.add_argument('wordBoost', type=float, default=1.0)
trackParser.add_argument('forwards', type=bool, default=True)
trackParser.add_argument('sumDistances', type=bool, default=False)
trackParser.add_argument('algorithm', type=str, default='adaptive')

# VocabularyAggregator parameters:
trackParser.add_argument('aggWeighFunction', type=str, default='Gaussian')
trackParser.add_argument('aggWFParam', type=float, default=1.0)
trackParser.add_argument('aggYearsInInterval', type=int, default=5)
trackParser.add_argument('aggWordsPerYear', type=int, default=10)


@app.route('/available-years')
def avlYears():
    years = _vm.getAvailableYears()
    yearLabels = {int(getRangeMiddle(y)): y for y in years}
    return jsonify(values=yearLabels,
                   first=min(yearLabels.keys()),
                   last=max(yearLabels.keys())
                   )


@app.route('/track/<terms>')
def trackWord(terms):
    '''VocabularyMonitor.trackClouds service. Expects a list of terms to be
    sent to the Vocabulary monitor, and returns a JSON representation of the
    response.'''
    params = trackParser.parse_args()
    termList = terms.split(',')
    results, links = \
        _vm.trackClouds(termList, maxTerms=params['maxTerms'],
                        maxRelatedTerms=params['maxRelatedTerms'],
                        startKey=params['startKey'],
                        endKey=params['endKey'],
                        minDist=params['minDist'],
                        wordBoost=params['wordBoost'],
                        forwards=params['forwards'],
                        sumDistances=params['sumDistances'],
                        algorithm=params['algorithm'],
                        )
    agg = VocabularyAggregator(weighF=params['aggWeighFunction'],
                               wfParam=params['aggWFParam'],
                               yearsInInterval=params['aggYearsInInterval'],
                               nWordsPerYear=params['aggWordsPerYear']
                               )
    aggResults, aggMetadata = agg.aggregate(results)

    # TODO: use used seeds for next loop query
    networks = yearlyNetwork(aggMetadata, aggResults, results, links)
    return jsonify(
        stream=yearTuplesAsDict(aggResults),
        networks=networks
        )

if __name__ == '__main__':
    arguments = docopt(__doc__)
    initApp(arguments['-f'], not arguments['--non-binary'])
    app.debug = arguments['-d']
    app.run(host='0.0.0.0')
