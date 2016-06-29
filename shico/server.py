'''ShiCo server.

Usage:
  server.py  [-f FILES] [-n] [-d] [-p PORT] [-c FUNCTIONNAME]

  -f FILES         Path to word2vec model files (glob format is supported)
                   [default: word2vecModels/195[0-1]_????.w2v]
  -n,--non-binary  w2v files are NOT binary.
  -d               Run in development mode (debug mode).
  -c FUNCTIONNAME  Name of cleaning function to be applied to output.
                   (example: shico.extras.cleanTermList)
  -p PORT          Port in which ShiCo should run [default: 8000].
'''
from docopt import docopt

from flask import Flask, jsonify
from flask_restful import reqparse
from flask.ext.cors import CORS

from vocabularymonitor import VocabularyMonitor
from vocabularyaggregator import VocabularyAggregator
from vocabularyembedding import doSpaceEmbedding

from format import yearlyNetwork, getRangeMiddle, yearTuplesAsDict

app = Flask(__name__)
CORS(app)
_vm = None
_cleaningFunction = None


def validatestr(value):
    '''Validate that given value is a non-empty string. Used to validate
    tracker parameters.'''
    try:
        s = str(value)
        return None if (len(s) == 0) else s
    except:
        raise ValueError


def isValidOption(value, options):
    '''Validate that given value is a string from a predetermined set.
    Used to validate tracker parameters.'''
    if value in options:
        return value
    else:
        raise ValueError


def validAlgorithm(value):
    '''Validate algorithm -- in lower case'''
    return isValidOption(value, _algorithms).lower()


def validWeighting(value):
    '''Validate weighting function'''
    return isValidOption(value, _weighFuncs)


def validDirection(value):
    '''Validate direction is Forward (false means backward)'''
    return isValidOption(value, _directions) == 'Forward'


def sumSimilarity(value):
    '''Validate boost methods is Sum distances (false means Counts)'''
    return isValidOption(value, _boostMethods) == 'Sum similarity'


def validCleaning(value):
    return isValidOption(value, _yesNo) == 'Yes'


def initApp(files, binary, cleaningFunctionStr):
    '''Initialize Flask app by loading VocabularyMonitor.

    files    Files to be loaded by VocabularyMonitor
    binary   Whether files are binary
    '''
    global _vm, _cleaningFunction
    _vm = VocabularyMonitor(files, binary)
    # _vm = "VocabularyMonitor(files, binary)"

    _cleaningFunction = _getCallableFunction(cleaningFunctionStr)


def _getCallableFunction(functionFullName):
    ''' TODO: Add documentation '''
    if functionFullName is None:
        return None
    nameParts = functionFullName.split('.')
    moduleName = '.'.join(nameParts[:-1])
    functionName = nameParts[-1]
    customModule = __import__(moduleName, fromlist=[functionName])
    return getattr(customModule, functionName)

# trackClouds parameters

# VocabularyMonitor parameters:
trackParser = reqparse.RequestParser()
trackParser.add_argument('maxTerms', type=int, default=10)
trackParser.add_argument('maxRelatedTerms', type=int, default=10)
trackParser.add_argument('startKey', type=validatestr, default=None)
trackParser.add_argument('endKey', type=validatestr, default=None)
trackParser.add_argument('minDist', type=float, default=0.0)
trackParser.add_argument('wordBoost', type=float, default=1.0)
trackParser.add_argument('forwards', type=validDirection, default=True)
trackParser.add_argument('boostMethod', type=sumSimilarity, default=True)
trackParser.add_argument('algorithm', type=validAlgorithm, default='adaptive')
trackParser.add_argument('doCleaning', type=validCleaning, default=False)

# VocabularyAggregator parameters:
trackParser.add_argument(
    'aggWeighFunction', type=validWeighting, default='Gaussian')
trackParser.add_argument('aggWFParam', type=float, default=1.0)
trackParser.add_argument('aggYearsInInterval', type=int, default=5)
trackParser.add_argument('aggWordsPerYear', type=int, default=10)

# Fixed options
_algorithms = ('Adaptive', 'Non-adaptive')
_weighFuncs = ('Gaussian', 'Linear', 'JSD')
_directions = ('Forward', 'Backward')
_boostMethods = ('Sum similarity', 'Counts')
_yesNo = ('Yes', 'No')


@app.route('/load-settings')
def appData():
    '''VocabularyMonitor.getAvailableYears service. Takes no parameters.
    Returns JSON structure with years available.'''
    avlYears = _vm.getAvailableYears()
    yearLabels = {int(getRangeMiddle(y)): y for y in avlYears}
    years = {
        'values': yearLabels,
        'first': min(yearLabels.keys()),
        'last': max(yearLabels.keys())
    }
    canClean = _cleaningFunction is not None
    return jsonify(years=years, cleaning=canClean)


@app.route('/track/<terms>')
def trackWord(terms):
    '''VocabularyMonitor.trackClouds service. Expects a list of terms to be
    sent to the Vocabulary monitor, and returns a JSON representation of the
    response.'''
    params = trackParser.parse_args()
    termList = terms.split(',')
    termList = [ term.lower() for term in termList ]
    results, links = \
        _vm.trackClouds(termList, maxTerms=params['maxTerms'],
                        maxRelatedTerms=params['maxRelatedTerms'],
                        startKey=params['startKey'],
                        endKey=params['endKey'],
                        minDist=params['minDist'],
                        wordBoost=params['wordBoost'],
                        forwards=params['forwards'],
                        sumSimilarity=params['boostMethod'],
                        algorithm=params['algorithm'],
                        cleaningFunction=_cleaningFunction if params[
                            'doCleaning'] else None
                        )
    agg = VocabularyAggregator(weighF=params['aggWeighFunction'],
                               wfParam=params['aggWFParam'],
                               yearsInInterval=params['aggYearsInInterval'],
                               nWordsPerYear=params['aggWordsPerYear']
                               )

    aggResults, aggMetadata = agg.aggregate(results)
    embedded = doSpaceEmbedding(_vm, results, aggMetadata)
    networks = yearlyNetwork(aggMetadata, aggResults, results, links)
    return jsonify(stream=yearTuplesAsDict(aggResults),
                   networks=networks,
                   embedded=embedded)


if __name__ == '__main__':
    arguments = docopt(__doc__)
    files = arguments['-f']
    binary = not arguments['--non-binary']
    cleaningFunctionStr = arguments['-c']
    port = int(arguments['-p'])
    initApp(files, binary, cleaningFunctionStr)
    app.debug = arguments['-d']
    app.run(host='0.0.0.0', port=port, threaded=True)
