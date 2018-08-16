import numpy as np

from sortedcontainers import SortedDict
from sklearn import manifold
from format import wordLocationAsDict, getRangeMiddle


def _getPairwiseDistances(wordsT1, model):
    dists = np.zeros((len(wordsT1), len(wordsT1)))
    for i, w1 in enumerate(wordsT1):
        for j, w2 in enumerate(wordsT1[i:]):
            try:
                dists[i, i+j] = 1-model.n_similarity(w1, w2)
            except:
                # If we cannot calculate the similarity, they are
                # as dissimilar as possible
                dists[i, i+j] = 1
            dists[i+j, i] = dists[i, i+j]
    return dists


def _getMDSEmbedding(dists):
    seed = np.random.RandomState(seed=3)
    mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-9, random_state=seed,
                       dissimilarity="precomputed", n_jobs=1)
    xyEmbedding = mds.fit(dists).embedding_
    return xyEmbedding


def _normalizeCloud(X):
    X -= X.min(axis=0)
    X /= X.max(axis=0)
    X -= X.mean(axis=0)
    return X


def _findTransform(wordsT0, locsT0, wordsT1, locsT1):
    matchingTerms = list(set(wordsT0).intersection(set(wordsT1)))

    # If we don't have any matching terms -- do not transform
    # (or transform by identity matrix)
    if len(matchingTerms) == 0:
        return np.eye(2)

    F0 = []
    F1 = []

    for word in matchingTerms:
        F0.append(locsT0[wordsT0.index(word)])
        F1.append(locsT1[wordsT1.index(word)])

    F0 = np.array(F0)
    F1 = np.array(F1)

    T, residuals, rank, s = np.linalg.lstsq(F1, F0)
    return T


def doSpaceEmbedding(monitor, results, aggMetadata):
    '''Create 2D word embedding from given set of results'''
    embeddedResults = SortedDict()

    wordsT0 = None
    locsT0 = None
    for label, r in results.iteritems():
        model = monitor._models[label]
        wordsT1 = [w for w, _ in r]

        dists = _getPairwiseDistances(wordsT1, model)
        locsT1 = _getMDSEmbedding(dists)

        if wordsT0 is not None:
            T = _findTransform(wordsT0, locsT0, wordsT1, locsT1)
            locsT1 = locsT1.dot(T)
            locsT1 = _normalizeCloud(locsT1)

        wordsT0 = wordsT1
        locsT0 = locsT1

        str_label = str(int(getRangeMiddle(label)))
        embeddedResults[str_label] = [wordLocationAsDict(
            wordsT1[i], locsT1[i, :]) for i in range(len(wordsT1))]

    # Aggregation step (more like throwing away some years)
    embeddedResultsAgg = {year: embeddedResults[year] for year in aggMetadata if year in embeddedResults}
    embeddedResultsAgg = SortedDict(embeddedResultsAgg)

    return embeddedResultsAgg
