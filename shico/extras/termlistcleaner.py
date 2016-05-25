import editdistance

def cleanTermList(termList):
    '''
    TODO:
        Documentation
        'high level' documentation
        Add testing
    '''
    minEditDiff = 5
    cleanTerms = []
    for word, weight in termList:
        if not _isCloseToList(word, cleanTerms, minEditDiff):
            cleanTerms.append((word, weight))
    return cleanTerms

def _isCloseToList(word, cleanTerms, minEditDiff):
    if len(cleanTerms)==0:
        return False
    for known,_ in cleanTerms:
        diff = float(editdistance.eval(word, known)) / min(len(word),len(known))
        if diff < 0.20:
            print '%s is too close (%2.4f) to %s'%(word, diff, known)
            return True
    return False
