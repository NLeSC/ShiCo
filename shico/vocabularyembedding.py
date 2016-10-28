import numpy as np

from sortedcontainers import SortedDict
from sklearn import manifold
from format import wordLocationAsDict, getRangeMiddle

def _getPairwiseDistances(wordsT1, model):
    dists = np.zeros((len(wordsT1),len(wordsT1)))
    for i,w1 in enumerate(wordsT1):
        for j,w2 in enumerate(wordsT1[i:]):
            try:
                dists[i,i+j] = 1-model.n_similarity(w1,w2)
            except:
                # If we cannot calculate the similarity, they are
                # as dissimilar as possible
                dists[i,i+j] = 1
            dists[i+j,i] = dists[i,i+j]
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
    '''Given two sets of words (wordsT0, wordsT1) and their locations
    (locsT0, locsT1), obtain the transformation paramters which will
    transform (rotate, scale and translate) words1 as required for it to match
    as closely as possible with words0.'''
    matchingTerms = list(set(wordsT0).intersection(set(wordsT1)))

    # If we don't have enough matching terms -- do not transform
    # (or transform by identity matrix)
    if len(matchingTerms)<3:
        return np.eye(2), np.array([0,0])

    # Find locations of matching terms
    L0 = np.array([ locsT0[wordsT0.index(w)] for w in matchingTerms ])
    L1 = np.array([ locsT1[wordsT1.index(w)] for w in matchingTerms ])

    # Shift so the first point of both sets is aligned
    sL0 = L0 - L0[0,:]
    sL1 = L1 - L1[0,:]

    # Find out rotation R and translation delta
    R, residuals, rank, s = np.linalg.lstsq(sL1[1:,:], sL0[1:,:])
    delta = L0[0,:] - L1[0,:].dot(R)
    return R, delta

def _applyTransform(data, params):
    '''Apply transformation parameters found by _findTransform to data'''
    R,delta = params
    data_tilde = data.dot(R)
    data_tilde = data_tilde + delta
    return data_tilde

def doSpaceEmbedding(monitor, results, aggMetadata):
    '''Create 2D word embedding from given set of results'''
    embeddedResults = SortedDict()

    wordsT0 = None
    locsT0  = None
    for label,r in results.iteritems():
        model = monitor._models[label]
        wordsT1 = [ w for w,_ in r ]

        dists = _getPairwiseDistances(wordsT1, model)
        locsT1 = _getMDSEmbedding(dists)

        if wordsT0 is not None:
            T = _findTransform(wordsT0, locsT0, wordsT1, locsT1)
            locsT1 = _applyTransform(locsT1, T)
            locsT1 = _normalizeCloud(locsT1)

        wordsT0 = wordsT1
        locsT0  = locsT1

        str_label = str(int(getRangeMiddle(label)))
        embeddedResults[str_label] = [ wordLocationAsDict(wordsT1[i],locsT1[i,:]) for i in range(len(wordsT1)) ]

    # Aggregation step (more like throwing away some years)
    embeddedResultsAgg = { year: embeddedResults[year] for year in aggMetadata }
    embeddedResultsAgg = SortedDict(embeddedResultsAgg)

    return embeddedResultsAgg
