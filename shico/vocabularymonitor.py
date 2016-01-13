import glob
import os
import gensim
import six

from sortedcontainers import SortedDict
from collections import defaultdict, Counter


class VocabularyMonitor():
    '''Vocabulary Monitor tracks a concept through time. It uses a series of
    gensim Word2Vec models (one for each group of years) to produce a group of
    concept words.
    '''

    def __init__(self, globPattern, binary=True):
        '''Create a Vocabulary monitor using the gensim w2v models located in
        the given glob pattern.

        Arguments:
        globPattern     glob pattern where w2v files can be found
        binary          True if w2v files have been saved as binary
        '''
        self._models = SortedDict()
        self._loadAllModels(globPattern, binary=True)

    def _loadAllModels(self, globPattern, binary=True):
        '''Load word2vec models from given globPattern and return a dictionary of
        Word2Vec models.
        '''
        for sModelFile in glob.glob(globPattern):
            # Chop off the path and the extension
            sModelName = os.path.splitext(os.path.basename(sModelFile))[0]

            print '[%s]: %s' % (sModelName, sModelFile)
            self._models[sModelName] = gensim.models.word2vec.Word2Vec.\
                load_word2vec_format(sModelFile, binary=binary)

    def trackClouds(self, seedTerms, maxTerms=10, maxRelatedTerms=10,
                    startKey=None, endKey=None, minDist=0.0, wordBoost=1.00,
                    forwards=True, sumDistances=False, algorithm='inlinks'):
        '''
        TODO: Document properly
        algorithm    'inlinks', 'outlinks', or 'non-adaptive'
        '''
        if isinstance(seedTerms, six.string_types):
            seedTerms = [seedTerms]
        aSeedSet = seedTerms
        dResult = SortedDict()
        background = SortedDict()

        # Keys are already sorted because we use a SortedDict
        sortedKeys = self._models.keys()

        if (startKey is not None):
            if startKey not in sortedKeys:
                raise KeyError('Key ' + startKey + ' not a valid model index')
            keyIdx = sortedKeys.index(startKey)
            sortedKeys = sortedKeys[keyIdx:]

        if (endKey is not None):
            if endKey not in sortedKeys:
                raise KeyError('Key ' + endKey + ' not a valid model index')
            keyIdx = sortedKeys.index(endKey)
            sortedKeys = sortedKeys[:keyIdx]

        if not forwards:
            sortedKeys = sortedKeys[::-1]

        for sKey in sortedKeys:
            if algorithm == 'inlinks':
                dResult[sKey], aSeedSet = \
                    self._trackInlink(self._models[sKey], aSeedSet,
                                      maxTerms=maxTerms,
                                      maxRelatedTerms=maxRelatedTerms,
                                      minDist=minDist,
                                      wordBoost=wordBoost,
                                      sumDistances=sumDistances)
            elif algorithm == 'outlinks':
                dResult[sKey], aSeedSet = \
                    self._trackOutlink(self._models[sKey], aSeedSet,
                                       maxTerms=maxTerms,
                                       maxRelatedTerms=maxRelatedTerms,
                                       minDist=minDist,
                                       wordBoost=wordBoost,
                                       sumDistances=sumDistances)
            elif algorithm == 'non-adaptive':
                dResult[sKey], aSeedSet = \
                    self._trackSimple(self._models[sKey], aSeedSet,
                                      maxTerms=maxTerms,
                                      maxRelatedTerms=maxRelatedTerms,
                                      minDist=minDist)
            else:
                raise Exception('Algorithm not supported: ' + algorithm)

        return dResult

    def _trackInlink(self, model, seedTerms, maxTerms=10, maxRelatedTerms=10,
                     minDist=0.0, wordBoost=1.0, sumDistances=False):
        if sumDistances:
            result = self._trackCore(model, seedTerms, maxTerms=maxTerms,
                                     maxRelatedTerms=maxRelatedTerms,
                                     minDist=minDist, wordBoost=wordBoost,
                                     reward=lambda tDist: 1.0 - tDist)
        else:
            result = self._trackCore(model, seedTerms, maxTerms=maxTerms,
                                     maxRelatedTerms=maxRelatedTerms,
                                     minDist=minDist)
        # Make a new seed set
        newSeedSet = [word for word, weight in result]
        return result, newSeedSet

    def _trackOutlink(self, model, seedTerms, maxTerms=10, maxRelatedTerms=10,
                      minDist=0.0, wordBoost=1.0, sumDistances=False):
        aFirstTierTerms = []
        dOutlinks = defaultdict(float)

        # Get the first tier related terms
        for term in seedTerms:
            try:
                newTerms = model.most_similar(term, topn=maxRelatedTerms)
                aFirstTierTerms += \
                    [newTerm for newTerm, tDist in newTerms
                     if tDist >= minDist]

                aFirstTierTerms.append(term)
                # Every word is related to itself
                dOutlinks[term] = wordBoost
            except KeyError:
                pass

        dFirstTierTerms = set(aFirstTierTerms)

        for ftTerm in dFirstTierTerms:
            newTerms = model.most_similar(ftTerm, topn=maxRelatedTerms)
            aSecondTierTerms = \
                [(newTerm, tDist) for newTerm, tDist in newTerms
                 if tDist >= minDist]

            for stTerm, tDist in aSecondTierTerms:
                if stTerm in dFirstTierTerms:
                    fAdd = (1.0 - tDist) if sumDistances else 1.0
                    dOutlinks[ftTerm] += fAdd

        oCounter = Counter(dOutlinks)
        result = oCounter.most_common(maxTerms)
        # Make a new seed set
        newSeedSet = [word for word, weight in result]
        return result, newSeedSet

    def _trackSimple(self, model, seedTerms, maxTerms=10, maxRelatedTerms=10,
                     minDist=0.0):
        trackTerms = self._trackCore(model, seedTerms, maxTerms=maxTerms,
                        maxRelatedTerms=maxRelatedTerms, minDist=minDist)
        return trackTerms, seedTerms

    def _trackCore(self, model, seedTerms, maxTerms=10, maxRelatedTerms=10,
                     minDist=0.0, wordBoost=1.0, reward=lambda x: 1.0):
        dRelatedTerms = defaultdict(float)

        # Get the first tier related terms
        for term in seedTerms:
            try:
                # The terms are always related to themselves
                dRelatedTerms[term] = wordBoost

                newTerms = model.most_similar(term, topn=maxRelatedTerms)
                for newTerm, tDist in newTerms:
                    if tDist < minDist:
                        break
                    dRelatedTerms[newTerm] += reward(tDist)
            except KeyError:
                pass

        oCounter = Counter(dRelatedTerms)
        return oCounter.most_common(maxTerms)
