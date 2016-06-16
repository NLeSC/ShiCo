'''ShiCo server.

Usage:
  server.py  [-f FILES] [-n] [-d] [-c FUNCTIONNAME]

  -f FILES         Path to word2vec model files (glob format is supported)
                   [default: word2vecModels/195[0-1]_????.w2v]
  -n,--non-binary  w2v files are NOT binary.
  -d               Run in development mode (debug mode).
  -c FUNCTIONNAME  Name of cleaning function to be applied to output.
                   (example: shico.extras.cleanTermList)
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
    embedded = _doSpaceEmbedding(results)
    networks = yearlyNetwork(aggMetadata, aggResults, results, links)
    return jsonify(stream=yearTuplesAsDict(aggResults),
                   networks=networks,
                   embedded=embedded)

from sortedcontainers import SortedDict
import numpy as np
from sklearn import manifold

def getPairwiseDistances(wordsT1, model):
    dists = np.zeros((len(wordsT1),len(wordsT1)))
    for i,w1 in enumerate(wordsT1):
        for j,w2 in enumerate(wordsT1[i:]):
            dists[i,i+j] = 1-model.n_similarity(w1,w2)
            dists[i+j,i] = dists[i,i+j]
    return dists

def getMDSEmbedding(dists):
    seed = np.random.RandomState(seed=3)
    mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                       dissimilarity="precomputed", n_jobs=1)
    xyEmbedding = mds.fit(dists).embedding_
    return xyEmbedding

def findTransform(wordsT0, locsT0, wordsT1, locsT1):
    matchingTerms = list(set(wordsT0).intersection(set(wordsT1)))

    F0 = []
    F1 = []

    for word in matchingTerms:
        F0.append(locsT0[wordsT0.index(word)])
        F1.append(locsT1[wordsT1.index(word)])

    F0 = np.array(F0)
    F1 = np.array(F1)

    T, residuals, rank, s = np.linalg.lstsq(F1, F0)
    return T

def _doSpaceEmbedding(results):
    embeddedResults = SortedDict()

    wordsT0 = None
    locsT0  = None
    for label,r in results.iteritems():
        model = _vm._models[label]
        wordsT1 = [ w for w,_ in r ]

        dists = getPairwiseDistances(wordsT1, model)
        locsT1 = getMDSEmbedding(dists)

        if wordsT0 is not None:
            T = findTransform(wordsT0, locsT0, wordsT1, locsT1)
            locsT1 = locsT1.dot(T)

        wordsT0 = wordsT1
        locsT0  = locsT1

        embeddedResults[label] = [ (wordsT1[i], locsT1[i,:].tolist()) for i in range(len(wordsT1)) ]

    return embeddedResults


if __name__ == '__main__':
    arguments = docopt(__doc__)
    files = arguments['-f']
    binary = not arguments['--non-binary']
    cleaningFunctionStr = arguments['-c']
    initApp(files, binary, cleaningFunctionStr)
    app.debug = arguments['-d']
    app.run(host='0.0.0.0', threaded=True)
