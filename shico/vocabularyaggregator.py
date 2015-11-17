from sortedcontainers import SortedDict
from collections import defaultdict
from utils import weightJSD, weightGauss, weightLinear


class VocabularyAggregator():
    def __init__(self, algorithm='adaptive', weighF='Gaussian', wfParam=10,
                 yearsInInterval=2, nWordsPerYear=5):
        self._aggAlgo = algorithm
        self._weighF = weighF
        self._wfParam = wfParam
        self._yearsInInterval = yearsInInterval
        self._nWordsPerYear = nWordsPerYear

    def aggregate(self, vocab):
        if self._aggAlgo == 'adaptive':
            return _adaptiveAggregation(vocab, n=self._nWordsPerYear,
                                        yIntervals=self._yearsInInterval,
                                        weightF=self._weighF,
                                        param=self._wfParam)
        raise Exception('Unknown aggregation algorithm: ' + self._aggAlgo)


def _adaptiveAggregation(V, n=5, yIntervals=2, weightF='Gaussian', param=10):
    if weightF == 'Gaussian':
        f = lambda y1, y2: weightGauss(y1, y2, param)
    elif weightF == 'JSD':
        f = lambda y1, y2: weightJSD(y1, y2, param)
    elif weightF == 'Linear':
        f = lambda y1, y2: weightLinear(y1, y2, param)
    else:
        f = weightF

    timeFrames = _arrangeIntervals(V, yIntervals)
    finalVocabs = SortedDict()
    for t in timeFrames:
        mu_t = _getMidRange(t[0], t[-1])
        V_prime = SortedDict({tx: V[tx] for tx in t})

        score = defaultdict(float)
        for years_v, words_v in V_prime.iteritems():
            mu_v = _getMidRange(years_v)
            fvt = f(mu_v, mu_t)
            for word, score_wv in words_v:
                score[word] += fvt * score_wv

        # Top n terms w sorted by score_w
        scoreList = [(k, v) for k, v in score.iteritems()]
        scoreList = sorted(scoreList, key=lambda pair: pair[1], reverse=True)
        topN = scoreList[:n]

        finalVocabs[str(int(mu_t))] = topN
    return finalVocabs


def _arrangeIntervals(vocabs, nYears=5):
    keys = vocabs.keys()
    return [keys[i:i + nYears] for i in range(0, len(keys), nYears)]


def _getMidRange(first, last=None):
    if last is None:
        last = first
    y0 = int(first.split('_')[0])
    yn = int(last.split('_')[1])
    return round((yn + y0) / 2)
