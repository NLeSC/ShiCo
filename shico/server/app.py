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

from flask import Flask, current_app, jsonify
from flask.ext.cors import CORS

from shico.vocabularyaggregator import VocabularyAggregator
from shico.vocabularyembedding import doSpaceEmbedding

from shico.format import yearlyNetwork, getRangeMiddle, yearTuplesAsDict
from shico.server.utils import initApp


app = Flask(__name__)
CORS(app)

@app.route('/load-settings')
def appData():
    '''VocabularyMonitor.getAvailableYears service. Takes no parameters.
    Returns JSON structure with years available.'''
    avlYears = app.config['vm'].getAvailableYears()
    yearLabels = {int(getRangeMiddle(y)): y for y in avlYears}
    years = {
        'values': yearLabels,
        'first': min(yearLabels.keys()),
        'last': max(yearLabels.keys())
    }
    canClean = app.config['cleaningFunction'] is not None
    return jsonify(years=years, cleaning=canClean)


@app.route('/track/<terms>')
def trackWord(terms):
    '''VocabularyMonitor.trackClouds service. Expects a list of terms to be
    sent to the Vocabulary monitor, and returns a JSON representation of the
    response.'''
    params = app.config['trackParser'].parse_args()
    termList = terms.split(',')
    termList = [ term.strip() for term in termList ]
    termList = [ term.lower() for term in termList ]
    results, links = \
        app.config['vm'].trackClouds(termList, maxTerms=params['maxTerms'],
                        maxRelatedTerms=params['maxRelatedTerms'],
                        startKey=params['startKey'],
                        endKey=params['endKey'],
                        minSim=params['minSim'],
                        wordBoost=params['wordBoost'],
                        forwards=params['forwards'],
                        sumSimilarity=params['boostMethod'],
                        algorithm=params['algorithm'],
                        cleaningFunction=app.config['cleaningFunction'] if params[
                            'doCleaning'] else None
                        )
    agg = VocabularyAggregator(weighF=params['aggWeighFunction'],
                               wfParam=params['aggWFParam'],
                               yearsInInterval=params['aggYearsInInterval'],
                               nWordsPerYear=params['aggWordsPerYear']
                               )

    aggResults, aggMetadata = agg.aggregate(results)
    embedded = doSpaceEmbedding(app.config['vm'], results, aggMetadata)
    networks = yearlyNetwork(aggMetadata, aggResults, results, links)
    return jsonify(stream=yearTuplesAsDict(aggResults),
                   networks=networks,
                   embedded=embedded,
                   vocabs=links)

if __name__ == "__main__":
    arguments = docopt(__doc__)
    files = arguments['-f']
    binary = not arguments['--non-binary']
    cleaningFunctionStr = arguments['-c']
    port = int(arguments['-p'])

    with app.app_context():
        initApp(current_app, files, binary, cleaningFunctionStr)

    app.debug = True
    app.run(host='0.0.0.0')
