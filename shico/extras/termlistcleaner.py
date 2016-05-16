import editdistance

def cleanTermList(termList):
    minEditDiff = 5
    cleanTerms = []
    for word, weight in termList:
        if not isCloseToList(word, cleanTerms, minEditDiff):
            cleanTerms.append((word, weight))
    return cleanTerms

def isCloseToList(word, cleanTerms, minEditDiff):
    if len(cleanTerms)==0:
        return False
    for known,_ in cleanTerms:
        d = editdistance.eval(word, known)
        if d < minEditDiff:
            print '%s is too close (%d) to %s'%(word, d, known)
            return True
    return False
