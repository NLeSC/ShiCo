from collections import Counter


def getRangeMiddle(first, last=None):
    '''Find the year in the middle of a year range. The range can be given
    either by a single string in the format YEAR1_YEAR2, or by two strings
    in this format.'''
    if last is None:
        last = first
    y0 = int(first.split('_')[0])
    yn = int(last.split('_')[1])
    return round((yn + y0) / 2)


def yearlyNetwork(aggMeta, aggResults, results, links):
    '''Build a dictionary of network graph definitions. The key of this
    dictionary are the years and the values are the network definition
    (in the format used by D3).'''
    seeds = { y:seedResp.keys() for y,seedResp in links.iteritems() }

    networks = {}
    for year_mu, years in aggMeta.iteritems():
        y_results = {y: results[y] for y in years}
        y_links = {y: links[y] for y in years}
        y_seeds = {y: seeds[y] for y in years}

        finalVocab = aggResults[year_mu]
        networks[year_mu] = _metaToNetwork(
            y_results, y_seeds, finalVocab, y_links)
    return networks


def yearTuplesAsDict(results):
    '''Converts the values of a dictionary from tuples to dictionaries.
    E.g.
    From:
        {
            1950: ('a',1), ('b',2),('c',3)
        }
    To:
        {
            1950: {
                'a': 1,
                'b': 2,
                'c': 3
            }
        }
    '''
    return {year: _tuplesAsDict(vals) for year, vals in results.iteritems()}


def _buildNode(word, counts, seedSet, finalWords):
    ''' Build a node for a force directed graph in format used by front end'''
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


def _buildLink(seed, word, weight, nodeIdx):
    ''' Build a node for a force directed graph in format used by front end'''
    seedIdx = nodeIdx[seed]
    wordIdx = nodeIdx[word]
    return {
        'source': seedIdx,
        'target': wordIdx,
        'value':  1 / (weight + 1)
    }


def _buildLinks(y_links, nodeIdx):
    '''Build a list of links from the given yearly links. For each year group,
    link all seeds to all their results (with strength proportional to their
    weight)'''
    linkList = []
    # We are not doing anything with the years in y_links
    for links in y_links.values():
        for seed, results in links.iteritems():
            for word, weight in results:
                # TODO: check seeds present in dict more elegantly
                if seed in nodeIdx and word in nodeIdx:
                    linkList.append(_buildLink(seed, word, weight, nodeIdx))
                else:
                    print 'Seed or word not in index!'
    return linkList


def _buildNodes(wordCounts, seedSet, finalWords):
    '''Build a set of nodes for the network graph. Also builds an dictionary of
    words and the ID's used to represent them on the list of nodes.'''
    nodeIdx = {}
    nodes = []
    # Make nodes from unique words
    uniqueWords = set(wordCounts.keys() + list(seedSet))
    for idx, w in enumerate(uniqueWords):
        nodes.append(_buildNode(w, wordCounts, seedSet, finalWords))
        nodeIdx[w] = idx
    return nodes, nodeIdx


def _metaToNetwork(results, seeds, finalVocab, y_links):
    '''Build a network (nodes & links), using aggregated results. Network must
    be in a format usable by the front end. '''
    wordCounts = Counter([w for res in results.values() for w, v in res])
    seedSet = set(w for seed in seeds.values() for w in seed)
    finalWords = [w for w, v in finalVocab]

    # TODO: can we unittest that nodeIdx contains all words in y_links ?
    nodes, nodeIdx = _buildNodes(wordCounts, seedSet, finalWords)
    links = _buildLinks(y_links, nodeIdx)

    network = {
        'nodes': nodes,
        'links': links
    }
    return network


def _tuplesAsDict(pairList):
    '''Convert list of (words,weight) to dict of word: weight'''
    return {word: weight for word, weight in pairList}
