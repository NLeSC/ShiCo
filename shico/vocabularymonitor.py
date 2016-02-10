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

    def getAvailableYears(self):
        '''
        TODO: Document properly
        '''
        return list(self._models.keys())

    def trackClouds(self, seedTerms, maxTerms=10, maxRelatedTerms=10,
                    startKey=None, endKey=None, minDist=0.0, wordBoost=1.00,
                    forwards=True, sumDistances=False, algorithm='adaptive'):
        '''
        TODO: Document properly
        algorithm    'adaptive', or 'non-adaptive'
        adaptive previously known as inlinks
        '''
        if isinstance(seedTerms, six.string_types):
            seedTerms = [seedTerms]
        aSeedSet = seedTerms

        # Initialize dicts to be returned
        # Dictionary of terms found for each year
        ## yTerms = { year: [(word1, weight1), word2, weight2]}
        yTerms = SortedDict()
        yLinks = SortedDict()

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
            if algorithm == 'adaptive':
                terms, links, newSeedSet = \
                    self._trackInlink(self._models[sKey], aSeedSet,
                                      maxTerms=maxTerms,
                                      maxRelatedTerms=maxRelatedTerms,
                                      minDist=minDist,
                                      wordBoost=wordBoost,
                                      sumDistances=sumDistances)
            elif algorithm == 'non-adaptive':
                # Non-adaptive algorithm uses always same set of seeds
                newSeedSet = aSeedSet
                terms, links = \
                    self._trackCore(self._models[sKey], aSeedSet,
                                    maxTerms=maxTerms,
                                    maxRelatedTerms=maxRelatedTerms,
                                    minDist=minDist)
            else:
                raise Exception('Algorithm not supported: ' + algorithm)

            # Store results and prepare for next iteration
            yTerms[sKey] = terms
            aSeedSet = newSeedSet
            yLinks[sKey] = links

        return yTerms, yLinks

    def _trackInlink(self, model, seedTerms, maxTerms=10, maxRelatedTerms=10,
                     minDist=0.0, wordBoost=1.0, sumDistances=False):
        if sumDistances:
            terms, links = self._trackCore(
                model, seedTerms, maxTerms=maxTerms,
                maxRelatedTerms=maxRelatedTerms, minDist=minDist,
                wordBoost=wordBoost,  reward=lambda tDist: 1.0 - tDist)
        else:
            terms, links = self._trackCore(
                model, seedTerms, maxTerms=maxTerms,
                maxRelatedTerms=maxRelatedTerms, minDist=minDist)
        # Make a new seed set
        newSeedSet = [word for word, weight in terms]
        return terms, links, newSeedSet

    def _trackCore(self, model, seedTerms, maxTerms=10, maxRelatedTerms=10,
                   minDist=0.0, wordBoost=1.0, reward=lambda x: 1.0):
        dRelatedTerms = defaultdict(float)
        links = defaultdict(list)

        # Get the first tier related terms
        for term in seedTerms:
            try:
                # The terms are always related to themselves
                dRelatedTerms[term] = wordBoost
                links[term].append((term, 0))

                newTerms = model.most_similar(term, topn=maxRelatedTerms)
                for newTerm, tDist in newTerms:
                    if tDist < minDist:
                        break
                    dRelatedTerms[newTerm] += reward(tDist)
                    links[term].append((newTerm, tDist))
            except KeyError:
                pass

        # Select the top N terms with biggest weights (where N=maxTerms)
        topTerms = _getCommonTerms(dRelatedTerms, maxTerms)

        selectedTerms = set(word for word, weight in topTerms)
        links = {seed: _pruned(pairs, selectedTerms)
                 for seed, pairs in links.iteritems()}
        return topTerms, links


def _pruned(pairs, words):
    return [(word, weight) for word, weight in pairs if word in words]


def _getCommonTerms(relatedTerms, maxTerms):
    termCounter = Counter(relatedTerms)
    topTerms = termCounter.most_common(maxTerms)
    return topTerms
