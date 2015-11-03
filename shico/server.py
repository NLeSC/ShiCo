"""ShiCo server.

Usage:
  server.py  [-f FILES]

  -f FILES    Path to word2vec model files (glob format is supported)
              [default: word2vecModels/195[0-1]_????.w2v]
"""
from docopt import docopt

from flask import Flask, jsonify
from flask_restful import reqparse

from vocabularymonitor import VocabularyMonitor

arguments = docopt(__doc__)

_vm = VocabularyMonitor()
_vm.loadAllModels(arguments['-f'])

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
trackParser.add_argument('outlinks', type=bool, default=False)

if __name__ == '__main__':
    app = Flask(__name__)
    # app.debug = True

    @app.route('/track/<word>')
    def trackWord(word):
        defaults = trackParser.parse_args()
        results = _vm. \
            trackClouds(word, maxTerms=defaults['maxTerms'],
                        maxRelatedTerms=defaults['maxRelatedTerms'],
                        startKey=defaults['startKey'],
                        endKey=defaults['endKey'],
                        minDist=defaults['minDist'],
                        wordBoost=defaults['wordBoost'],
                        forwards=defaults['forwards'],
                        sumDistances=defaults['sumDistances'],
                        outlinks=defaults['outlinks'],
                        )
        return jsonify(results)

    app.run(host='0.0.0.0')
