from collections import Counter

# TODO: Document
# TODO: Beautify (rename functions and so on)
def _makeNode(word, counts, seedSet, finalWords):
    if word in seedSet:
        nodeType = 'seed'
    elif word in finalWords:
        nodeType = 'word'
    else:
        nodeType = 'drop'
    return {
            'name': word,
            'count': counts[word],
            'type': nodeType
           }

def _buildNode(seed, word, weight, nodeIdx):
    # TODO: check seeds present in dict more elegantly
    if seed in nodeIdx:
        seedIdx = nodeIdx[seed]
    else:
        seedIdx = -1
        print 'Seed not found:',seed
    if word in nodeIdx:
        wordIdx = nodeIdx[word]
    else:
        wordIdx = -1
        print 'Word not found:',word
    return {
            'source': seedIdx,
            'target': wordIdx,
            'value':  1/(weight+1)
            }

def _buildLinks(y_links, nodeIdx):
    linkList = []
    for year,links in y_links.iteritems():
        for seed,results in links.iteritems():
            for word,weight in results:
                linkList.append(_buildNode(seed, word, weight, nodeIdx))
    return linkList

def _metaToNetwork(year, results, seeds, finalVocab, y_links):
    words = [ w for res in results.values() for w,v in res ]
    counts = Counter(words)
    seedSet = set( w for seed in seeds.values() for w in seed )
    finalWords = [ w for w,v in finalVocab ]

    # Make nodes from unique words
    uniqueWords = set(counts.keys() + list(seedSet))
    nodeIdx = {}
    nodes = []
    for idx,w in enumerate(uniqueWords):
        nodes.append(_makeNode(w, counts, seedSet, finalWords))
        nodeIdx[w] = idx
    links = _buildLinks(y_links, nodeIdx)

    network = {
        "nodes": nodes,
        "links": links
    }
    return network


def _yearlyNetwork(aggMeta, aggResults, results, seeds, links):
    r = {}
    for year_mu, years in aggMeta.iteritems():
        y_results = { y: results[y] for y in years }
        y_seeds = { y: seeds[y] for y in years }
        y_links = { y: links[y] for y in years }
        finalVocab = aggResults[year_mu]
        r[year_mu] = _metaToNetwork(year_mu, y_results, y_seeds, finalVocab, y_links)
    return r
