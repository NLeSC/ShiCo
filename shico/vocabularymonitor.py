import glob
import os
import gensim
import sys
import codecs
import six

from sortedcontainers import SortedDict
from collections import defaultdict, Counter


class VocabularyMonitor():

    def __init__(self):
        self._models = SortedDict()

    def loadAllModels(self, sGlobPattern, bReplace=True, bBinary=True):
        """Load word2vec models from given sGlobPattern and return a dictionary of
        Word2Vec models.
        """
        for sModelFile in glob.glob(sGlobPattern):
            # Chop off the path and the extension
            sModelName = os.path.splitext(os.path.basename(sModelFile))[0]

            if (sModelName in self._models) and not bReplace:
                print "[%s]: already loaded" % sModelName
            else:
                print "[%s]: %s" % (sModelName, sModelFile)
                self._models[sModelName] = gensim.models.word2vec.Word2Vec.\
                    load_word2vec_format(sModelFile, binary=bBinary)

    def trackClouds(self, seedTerms, maxTerms=10, maxRelatedTerms=10,
                    startKey=None, endKey=None, minDist=0.0, wordBoost=1.00,
                    forwards=True, sumDistances=False, algorithm='inlinks'):
        '''
        algorithm    'inlinks', 'outlinks', or 'non-adaptive'
        '''
        if isinstance(seedTerms, six.string_types):
            seedTerms = [seedTerms]
        aSeedSet = seedTerms
        dResult = SortedDict()

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
                                      maxRelatedTerms=maxRelatedTerms)
            else:
                raise Exception('Algorithm not supported: ' + algorithm)

        return dResult

    def printTrackClouds(self, dResult, aSeedTerms, sOutputFile=None,
                         sumDistances=False, direction='forwards',
                         description='', aggregator=None):
        # Aggregation step
        if aggregator is not None:
            dResult = aggregator.aggregate(dResult)

        fh = sys.stdout
        if sOutputFile is not None:
            fh = codecs.open(sOutputFile, mode='w', encoding='utf8')
        if isinstance(aSeedTerms, six.string_types):
            aSeedTerms = [aSeedTerms]

        # First line always contains the seed terms
        print >>fh, ",".join(aSeedTerms)
        # Second line is always the direction
        print >>fh, direction
        # Third line is always the description
        print >>fh, description

        for sKey in dResult.keys():
            if sumDistances:
                print >>fh, "%s\t%s" % (sKey, ' '.join(["%s (%.2f)" %
                                        (x[0], x[1]) for x in dResult[sKey]]))
            else:
                print >>fh, "%s\t%s" % (sKey, ' '.join(["%s (%d)" %
                                        (x[0], x[1]) for x in dResult[sKey]]))

        if sOutputFile is not None:
            fh.close()

    def _trackInlink(self, model, seedTerms, maxTerms=10, maxRelatedTerms=10,
                     minDist=0.0, wordBoost=1.0, sumDistances=False):
        if sumDistances:
            result = self._inlinkSum(model, seedTerms,
                                     maxTerms=maxTerms, minDist=minDist,
                                     maxRelatedTerms=maxRelatedTerms,
                                     wordBoost=wordBoost)
        else:
            result = self._inlinkNosum(model, seedTerms,
                                       maxTerms=maxTerms, minDist=minDist,
                                       maxRelatedTerms=maxRelatedTerms,
                                       wordBoost=wordBoost)
        # Make a new seed set
        newSeedSet = [word for word, weight in result]
        return result, newSeedSet

    def _inlinkSum(self, model, seedTerms, maxTerms=10, maxRelatedTerms=10,
                   minDist=0.0, wordBoost=1.0):
        dRelatedTerms = defaultdict(float)
        for term in seedTerms:
            try:
                # The terms are always related to themselves
                dRelatedTerms[term] += wordBoost

                newTerms = model.most_similar(term, topn=maxRelatedTerms)
                for newTerm, tDist in newTerms:
                    if tDist < minDist:
                        break
                    fDistance = 1.0 - tDist  # Similarity to distance
                    dRelatedTerms[newTerm] += fDistance
            except KeyError:  # If the word is not present in this era
                pass

        oCounter = Counter(dRelatedTerms)
        return oCounter.most_common(maxTerms)

    def _inlinkNosum(self, model, seedTerms, maxTerms=10, maxRelatedTerms=10,
                     minDist=0.0, wordBoost=1.0):
        aRelatedTerms = []
        for term in seedTerms:
            try:
                newTerms = model.most_similar(term, topn=maxRelatedTerms)
                aRelatedTerms += \
                    [newTerm for newTerm, tDist in newTerms
                     if tDist >= minDist]
            except KeyError:  # If the word is not present in this era
                pass

        # The terms are always related to themselves
        aRelatedTerms += seedTerms
        oCounter = Counter(aRelatedTerms)

        return oCounter.most_common(maxTerms)

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

    def _trackSimple(self, model, seedTerms, maxTerms=10, maxRelatedTerms=10):
        relatedTerms = []

        # Get the first tier related terms
        for term in seedTerms:
            try:
                newTerms = model.most_similar(term, topn=maxRelatedTerms)
                relatedTerms += [newTerm for newTerm, tDist in newTerms]

                relatedTerms.append(term)
                # Every word is related to itself
            except KeyError:
                pass

        oCounter = Counter(relatedTerms)
        return oCounter.most_common(maxTerms), seedTerms
