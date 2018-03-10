from flask_restful import reqparse
from shico.server.validations import validatestr, validAlgorithm, validWeighting, validDirection, sumSimilarity, validCleaning

from shico.vocabularymonitor import VocabularyMonitor


def initParamParser():
    # VocabularyMonitor parameters:
    trackParser = reqparse.RequestParser()
    trackParser.add_argument('maxTerms', type=int, default=10)
    trackParser.add_argument('maxRelatedTerms', type=int, default=10)
    trackParser.add_argument('startKey', type=validatestr, default=None)
    trackParser.add_argument('endKey', type=validatestr, default=None)
    trackParser.add_argument('minSim', type=float, default=0.0)
    trackParser.add_argument('wordBoost', type=float, default=1.0)
    trackParser.add_argument('forwards', type=validDirection, default=True)
    trackParser.add_argument('boostMethod', type=sumSimilarity, default=True)
    trackParser.add_argument(
        'algorithm', type=validAlgorithm, default='adaptive')
    trackParser.add_argument('doCleaning', type=validCleaning, default=False)

    # VocabularyAggregator parameters:
    trackParser.add_argument('aggWeighFunction', type=validWeighting,
                             default='Gaussian')
    trackParser.add_argument('aggWFParam', type=float, default=1.0)
    trackParser.add_argument('aggYearsInInterval', type=int, default=5)
    trackParser.add_argument('aggWordsPerYear', type=int, default=10)

    return trackParser


def initApp(app, files, binary, useMmap, w2vFormat, cleaningFunctionStr):
    '''Initialize Flask app by loading VocabularyMonitor,
    tracker parameter parser and callable functions (if any).

    files    Files to be loaded by VocabularyMonitor
    binary   Whether files are binary
    useMmap  ???
    w2vFormat ???
    cleaningFunctionStr   ???
    '''
    # TODO: 'Add use cache on initApp'
    vm = VocabularyMonitor(files, binary=binary,
                           useMmap=useMmap, w2vFormat=w2vFormat)
    cleaningFunction = _getCallableFunction(cleaningFunctionStr)
    trackParser = initParamParser()

    app.config['vm'] = vm
    app.config['cleaningFunction'] = cleaningFunction
    app.config['trackParser'] = trackParser


def _getCallableFunction(functionFullName):
    ''' TODO: Add documentation '''
    if functionFullName is None:
        return None
    nameParts = functionFullName.split('.')
    moduleName = '.'.join(nameParts[:-1])
    functionName = nameParts[-1]
    customModule = __import__(moduleName, fromlist=[functionName])
    return getattr(customModule, functionName)
