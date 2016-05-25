import editdistance


def cleanTermList(termList):
    '''Remove items from a list, which are 'too close' to other items on the
    list. In this way, only one version is retained. Closeness is measured as
    the edit distance between any two words, normalized by the length of
    the shortest word.

    termList    A list of (word,weight) tuples to be filtered.
    '''
    minEditDiff = 0.20
    cleanTerms = []
    for word, weight in termList:
        if not _isCloseToList(word, cleanTerms, minEditDiff):
            cleanTerms.append((word, weight))
    return cleanTerms


def _isCloseToList(word, cleanTerms, minEditDiff):
    if len(cleanTerms) == 0:
        return False
    for known, _ in cleanTerms:
        diff = float(editdistance.eval(word, known)) / \
            min(len(word), len(known))
        if diff < minEditDiff:
            # print '%s is too close (%2.4f) to %s'%(word, diff, known)
            return True
    return False
