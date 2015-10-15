import numpy as np
import collections
from gensim import matutils
import os
import codecs
import sys
import glob
import gensim


# NOTE that you can give a dModels as input (this allows for
# adding to/replacing models already loaded).
def loadAllModels(sGlobPattern, dModels={}, bReplace=True, bBinary=True):
  for sModelFile in glob.glob(sGlobPattern):
    # Chop off the path and the extension
    sModelName = os.path.splitext(os.path.basename(sModelFile))[0]
    if sModelName.startswith('all_preprocessed_files'):
      sModelName = sModelName[23:]
      
    if (sModelName in dModels) and not bReplace:
      print "[%s]: already in" % sModelName
    else:
      print "[%s]: %s" % (sModelName, sModelFile)
      dModels[sModelName] = gensim.models.word2vec.Word2Vec.load_word2vec_format(sModelFile, binary=bBinary)

  return dModels

def cosineSimilarities(npaWrdEmbds1, npaWrdEmbds2):
  if (npaWrdEmbds1.size == 0) or (npaWrdEmbds2.size == 0):
    return np.array([[0.0]])
  npaNorms1 = np.array([np.sqrt(np.power(npaWrdEmbds1, 2).sum(axis=1))])
  npaNorms2 = np.array([np.sqrt(np.power(npaWrdEmbds2, 2).sum(axis=1))])
  npaNorms = npaNorms1.T * npaNorms2
  npaDots = npaWrdEmbds1.dot(npaWrdEmbds2.T)
  return npaDots / npaNorms

# Input: two matrices of word embeddings
def euclidean_distances(npaWrdEmbds1, npaWrdEmbds2):
  npaDistances = np.empty([npaWrdEmbds1.shape[0],npaWrdEmbds2.shape[0]],
                          dtype=float)
  for i in range(npaWrdEmbds1.shape[0]):
    for j in range(npaWrdEmbds2.shape[0]):
      npaDistances[i][j] = euclidean_distance_vec(npaWrdEmbds1[i],
                                                  npaWrdEmbds2[j])
  return npaDistances

# Input: two word embedding vectors
def euclidean_distance_vec(npaWrdEmbd1, npaWrdEmbd2):
  if (npaWrdEmbd1.size == 0) or (npaWrdEmbd2.size == 0):
    return 0.0
  npaDiff = npaWrdEmbd1 - npaWrdEmbd2
  return np.sqrt(np.power(npaDiff, 2).sum())

# Input: one word embedding vector, one matrix of word embeddings
def euclidean_distance_matrix(npaWrdEmbds, npaWrdEmbd):
  if (npaWrdEmbd1.size == 0) or (npaWrdEmbd2.size == 0):
    return 0.0

  return np.sqrt(np.power(npaWrdEmbds - npaWrdEmbd, 2).sum(axis=1))

# Find the most similar words in terms of Euclidean distance
# This turns out to give EXACTLY the same results as most_similar (which does
# things based on cosine similarities)...?!?!?!?
def most_similar_eucl(oModel, sWord, iTopN=10):
  npaDistances = np.sqrt(np.power(oModel.syn0 - oModel[sWord], 2).sum(axis=1))
  
  npaBestIndices = npaDistances.argsort()[:iTopN + 1]
  # Ignore (don't return) the input word
  aResult = [(oModel.index2word[i], npaDistances[i]) \
               for i in npaBestIndices if i != oModel.vocab[sWord].index]
  return aResult[:iTopN]

# - Get the related terms for all terms
# - See, for each term, how many times it is mentioned in a related term list
#   of another word
# - Keep the most related-to terms
#   So we sort by >>in-degree<<
def trackCloud3_inlink(oModel, aTerms, iMaxNrOfTerms=10,
                       iMaxNrOfRelatedTerms=10,
                       fMinDist=0.0, fSeedWordBoost=1.0,
                       bSumOfDistances=False, bDebug=False):
  if bDebug:
    import pdb
    pdb.set_trace()

  aRelatedTerms = []
  dRelatedTerms = {}
  for sTerm in aTerms:  
    if bSumOfDistances:
      try:
        aSimTerms = oModel.most_similar(sTerm, topn=iMaxNrOfRelatedTerms)

        # The terms are always related to themselves
        try:
          dRelatedTerms[sTerm] += fSeedWordBoost
        except KeyError:
          dRelatedTerms[sTerm] = fSeedWordBoost

        for tSimTerm in aSimTerms:
          if tSimTerm[1] < fMinDist:
            break
          fDistance = 1.0 - tSimTerm[1] # Similarity to distance
          try:
            dRelatedTerms[tSimTerm[0]] += fDistance
          except KeyError:
            dRelatedTerms[tSimTerm[0]] = fDistance
      except KeyError: # If the word is not present in this era
        pass
    else:
      try:
        aRelatedTerms += \
            [x[0] for x in \
               oModel.most_similar(sTerm, topn=iMaxNrOfRelatedTerms) \
               if x[1] >= fMinDist]
        
        # The terms are always related to themselves
        try:
          dRelatedTerms[sTerm] += fSeedWordBoost
        except KeyError:
          dRelatedTerms[sTerm] = fSeedWordBoost
      except KeyError: # If the word is not present in this era
        pass

  oCounter = None
  if bSumOfDistances:
    oCounter = collections.Counter(dRelatedTerms)
  else:
    # The terms are always related to themselves 
    aRelatedTerms += aTerms 
    oCounter = collections.Counter(aRelatedTerms)

  return oCounter.most_common(iMaxNrOfTerms)

# - Expend the seed term list with all similar terms (within distance)
# - See, for all terms in this expanded list, how many related terms they have
#   (within distance) in this expanded list
# - Keep the terms which have most of these
#   So we sort by >>out-degree<<
def trackCloud3_outlink_oud(oModel, aTerms, iMaxNrOfTerms=10,
                        iMaxNrOfRelatedTerms=10, fMinDist=0.0,
                        fSeedWordBoost=1.00,
                        bSumOfDistances=False):
  aSimilarTerms = []

  # Get the related terms for all terms
  for sTerm in aTerms:
    aSimilarTerms += \
        [x[0] for x in \
           oModel.most_similar(sTerm, topn=iMaxNrOfRelatedTerms) \
           if x[1] >= fMinDist]
  # The terms are always related to themselves 
  setSimilarTerms = set(aTerms + aSimilarTerms) 

  dOutlinks = {}
  for sSimTerm in setSimilarTerms:
    dOutlinks[sSimTerm] = \
        len( set([x[0] for x in \
                    oModel.most_similar(sSimTerm, topn=iMaxNrOfRelatedTerms)  \
                    if x[1] >= fMinDist]) &
             setSimilarTerms)

  oCounter = collections.Counter(dOutlinks)
  return oCounter.most_common(iMaxNrOfTerms)

# - Expend the seed term list with all similar terms (within distance)
# - See, for all terms in this expanded list, how many related terms they have
#   (within distance) in this expanded list
# - Keep the terms which have most of these
#   So we sort by >>out-degree<<
def trackCloud3_outlink(oModel, aTerms, iMaxNrOfTerms=10,
                        iMaxNrOfRelatedTerms=10, fMinDist=0.0,
                        fSeedWordBoost=1.00,
                        bSumOfDistances=False, bDebug=False):
  aFirstTierTerms = []
  dOutlinks = {}

  # Get the first tier related terms
  for sTerm in aTerms:
    try:
      aFirstTierTerms += \
          [x[0] for x in oModel.most_similar(sTerm, topn=iMaxNrOfRelatedTerms)\
             if x[1] >= fMinDist]
      aFirstTierTerms.append(sTerm)
      # Every word is related to itself
      dOutlinks[sTerm] = fSeedWordBoost
    except KeyError:
      pass
 
  setFirstTierTerms = set(aFirstTierTerms)
  dFirstTierTerms = {x: 1 for x in aFirstTierTerms}

  fAdd = 1.0
  for sFirstTierTerm in setFirstTierTerms:
    aSecondTierTerms = \
        [x for x in oModel.most_similar(sFirstTierTerm,
                                        topn=iMaxNrOfRelatedTerms) \
           if x[1] >= fMinDist]

    for tSecondTierTerm in aSecondTierTerms:
      if tSecondTierTerm[0] in dFirstTierTerms:
        if bSumOfDistances: # Else it is 1 (and stays 1)
          #fAdd = tSecondTierTerm[1] 
          fAdd = 1.0 - tSecondTierTerm[1] 

        try:
          dOutlinks[sFirstTierTerm] += fAdd
        except KeyError:
          dOutlinks[sFirstTierTerm] = fAdd

  if bDebug:
    import pdb
    pdb.set_trace()

  oCounter = collections.Counter(dOutlinks)
  return oCounter.most_common(iMaxNrOfTerms)

def trackClouds3(dModels, aSeedTerms, sOutputFile=None,
                 iMaxNrOfTerms=10,
                 iMaxNrOfRelatedTerms=10, sStartKey=None, sEndKey=None,
                 fMinDist=0.0, fSeedWordBoost=1.00, sDirection='forwards',
                 sDescription='', bSumOfDistances=False, bOutlinks=False,
                 bDebug=False):
  fh = sys.stdout
  if sOutputFile is not None:
    fh = codecs.open(sOutputFile, mode='w', encoding='utf8')

  bBackwards = True if (sDirection == 'backwards') else False

  # First line always contains the seed terms
  print >>fh, ",".join(aSeedTerms)
  # Second line is always the direction
  print >>fh, sDirection
  # Third line is always the description
  print >>fh, sDescription

  aSeedSet = aSeedTerms
  dResult = {}

  aSortedKeys = sorted(dModels.keys())
  if bBackwards:
    aSortedKeys = aSortedKeys[::-1]

  for sKey in aSortedKeys:
    if (sEndKey is not None) and (sKey == sEndKey):
      break
    if (sStartKey is not None):
      if sKey != sStartKey:
        continue
      else:
        sStartKey = None

    if bOutlinks:
      dResult[sKey] = \
          trackCloud3_outlink(dModels[sKey], aSeedSet,
                              iMaxNrOfTerms=iMaxNrOfTerms,
                              iMaxNrOfRelatedTerms=iMaxNrOfRelatedTerms,
                              fMinDist=fMinDist,
                              fSeedWordBoost=fSeedWordBoost,
                              bSumOfDistances=bSumOfDistances,
                              bDebug=bDebug)
    else:
      dResult[sKey] = \
          trackCloud3_inlink(dModels[sKey], aSeedSet,
                             iMaxNrOfTerms=iMaxNrOfTerms,
                             iMaxNrOfRelatedTerms=iMaxNrOfRelatedTerms,
                             fMinDist=fMinDist,
                             fSeedWordBoost=fSeedWordBoost,
                             bSumOfDistances=bSumOfDistances,
                             bDebug=bDebug)

    if bSumOfDistances:
      print >>fh, "%s\t%s" % (sKey, ' '.join(["%s (%.2f)" % (x[0], x[1]) for x in dResult[sKey]]))
    else:
      print >>fh, "%s\t%s" % (sKey, ' '.join(["%s (%d)" % (x[0], x[1]) for x in dResult[sKey]]))

    # Make a new seed set
    aSeedSet = [x[0] for x in dResult[sKey]]

  if sOutputFile is not None:
    fh.close()
  # return dResult

def addRelatedWord(dRelatedWords, sWord, fWeight):
  try:
    dRelatedWords[sWord] += fWeight
  except KeyError:
    dRelatedWords[sWord] = fWeight

def expandRelatedWords(oModel, aSeedSet, iMaxNrOfTerms=None, fMinDist=None):
  dRelatedWords = {}

  for (sSeedWord, fSeedWordWeight) in aSeedSet:
    # Always add the seed words themselves
    addRelatedWord(dRelatedWords, sSeedWord, fSeedWordWeight)

    for (sRelatedWord, fRelatedWordWeight) in \
          oModel.most_similar(sSeedWord,topn=iMaxNrOfTerms):
      if fRelatedWordWeight < fMinDist:
        break
      else:
        fTmpWeight = fSeedWordWeight * fRelatedWordWeight
        addRelatedWord(dRelatedWords, sRelatedWord, fTmpWeight)
  
  return [(sWord, fWeight) for sWord, fWeight in dRelatedWords.iteritems()]

def trackVocab(dModels, aSeedTerms, iMaxNrOfTerms=10, iMaxNrOfRelatedTerms=10,
               sStartKey=None, sEndKey=None, fMinDist=0.0, bBackwards=False,
               bSumOfDistances=False, bOutlinks=False):
  import pdb
  pdb.set_trace()

  aSortedKeys = sorted(dModels.keys())
  if bBackwards:
    aSortedKeys = aSortedKeys[::-1]

  # Start with initial set, all the weights are identical
  aSeedSet = [(x, 1.0) for x in aSeedTerms]

  for sKey in aSortedKeys:
    if (sEndKey is not None) and (sKey == sEndKey):
      break
    if (sStartKey is not None):
      if sKey != sStartKey:
        continue
      else:
        sStartKey = None

    # NOTE that we change the seed set here with every iteration!
    aSeedSet = expandRelatedWords(dModels[sKey], aSeedSet,
                                  iMaxNrOfTerms=iMaxNrOfTerms,
                                  fMinDist=fMinDist)

    print "%s: %s" % (sKey, aSeedSet)

def trackWord(dModels, sTerm, iMaxNrOfRelatedTerms=10, fMinDist=0.0):
  aSortedKeys = sorted(dModels.keys())
  for sKey in aSortedKeys:
    try:
      print "%s: %s" % \
          (sKey,
           ", ".join(["%s (%.2f)" % (x[0], x[1]) for x in \
                        dModels[sKey].most_similar(sTerm,
                                                   topn=iMaxNrOfRelatedTerms)\
                        if x[1] > fMinDist]))
    except KeyError:
      print "%s: []" % sKey

def trackWords(dModels, aTerms, sDirection, sDescription, sOutputFile=None,
               iMaxNrOfRelatedTerms=10, fMinDist=0.0):
  fh = sys.stdout
  if sOutputFile is not None:
    fh = codecs.open(sOutputFile, mode='w', encoding='utf8')

  # First line always contains the seed terms
  print >>fh, ",".join(aTerms)
  # Actually the directi0n doesn't mean anything here. We just always have it
  # on the second line, so the rest of the code can rely on this...
  print >>fh, sDirection
  # And third line is always the description
  print >>fh, sDescription

  aSortedKeys = sorted(dModels.keys())
  for sKey in aSortedKeys:
    try:
      aWordEmbeddings = initialVectors(dModels[sKey], sKey, aTerms)
      if len(aWordEmbeddings) == 0:
        print >>fh, "%s\t" % sKey
      else:
        npaMeanVector = np.mean(aWordEmbeddings, axis=0)

        print >>fh, "%s\t%s" % \
            (sKey,
             " ".join(surroundingWords(dModels[sKey], npaMeanVector,
                                       fMinDist, iMaxNrOfRelatedTerms)))
    except KeyError:
      print >>fh, "%s\t" % sKey

  if sOutputFile is not None:
    fh.close()

# Input: the model of the new time period to consider (so that is current now)
#        the terms the previous time period produced
#
# What we do is:
# - We get the word embeddings for all the terms in the current model
#
# - We take the mean of them all, and cut away a term at the outside
#   then we take the mean again, and cut away one peripheral term again
#   We repeat this procedure until we have iMaxNrOfTerms terms left.
#
# - We get the iMaxNrOfRelatedTerms terms for these and return them
# 
def trackCloud1(oModel, aTerms, iMaxNrOfTerms=10, iMaxNrOfRelatedTerms=10,
               sDist='cosine', fMinDist=0.0):
  aEmbeddings = []
  for sTerm in aTerms:
    try:
      aEmbeddings.append(oModel[sTerm])
    except KeyError:
      pass

  npaEmbeddings = np.array(aEmbeddings, dtype=float)

  # Get the mean
  npaMean = npaEmbeddings.mean(axis=0)

  # Prune
  while npaEmbeddings.shape[0] > iMaxNrOfTerms:
    # Find out which term is farthest away 
    iDelIndex = None
    iDelIndex2 = None
    if sDist == 'cosine':
      npaCosineSims = cosineSimilarities(npaEmbeddings, np.array([npaMean]))

      ###
      npaAllCosines = cosineSimilarities(npaEmbeddings, npaEmbeddings)
      aCoordinates = np.where(npaAllCosines == npaAllCosines[npaCosineSims > 0].min())
      print "%s" % list(aCoordinates)
      #print "Most distant terms are: %s, %s" % (aTerms[aCoordinates[0][0]],
      #                                          aTerms[aCoordinates[0][1]])
      #print "Del: %d" % npaCosineSims.argmin()
      ###
      iDelIndex = aCoordinates[0][0]
      iDelIndex2 = aCoordinates[0][1]
      #iDelIndex = \
      #    cosineSimilarities(npaEmbeddings, np.array([npaMean])).argmin()

    elif sDist == 'eucl':
      npaEuclideanDistances = \
          euclidean_distances(npaEmbeddings, np.array([npaMean]))

      print "%s" % zip(aTerms, [x[0] for x in npaEuclideanDistances])

      iDelIndex = \
          euclidean_distances(npaEmbeddings, np.array([npaMean])).argmax()

    print "Throwing out [1] %s" % aTerms[iDelIndex]
    # Cut it from the embeddings
    npaEmbeddings = npaEmbeddings[range(iDelIndex) + \
                                    range(iDelIndex+1, npaEmbeddings.shape[0])]
    # Also cut it from the term list
    aTerms = aTerms[:iDelIndex] + aTerms[iDelIndex+1:]

    if iDelIndex2 is not None:
      if iDelIndex2 > iDelIndex:
        iDelIndex2 -= 1
      print "Throwing out [2] %s" % aTerms[iDelIndex2]
      # Cut it from the embeddings
      npaEmbeddings = \
          npaEmbeddings[range(iDelIndex2) + \
                          range(iDelIndex2+1, npaEmbeddings.shape[0])]
      # Also cut it from the term list
      aTerms = aTerms[:iDelIndex2] + aTerms[iDelIndex2+1:]

    # Take a new mean
    npaMean = npaEmbeddings.mean(axis=0)

  # Enrich with related terms in this period
  aNewTerms = []
  for sTerm in aTerms:
    #print "Finding most similar for %s" % sTerm
    # Get the most similar terms (they come as tuples: (term, distance))
    aNewTerms += [x[0] for x in oModel.most_similar(sTerm,
                                                    topn=iMaxNrOfRelatedTerms)
                  if x[1] >= fMinDist]
  
  # Add the seed terms and make them unique 
  return list(set(aNewTerms + aTerms))

def trackCloud2(oModel, aTerms, iMaxNrOfTerms=50, iMaxNrOfRelatedTerms=5,
               sDist='cosine', fMinDist=0.0):
  # Enrich with related terms in this period
  aNewTerms = []
  for sTerm in aTerms:
    #print "Finding most similar for %s" % sTerm
    # Get the most similar terms (they come as tuples: (term, distance))
    aNewTerms += [x[0] for x in oModel.most_similar(sTerm,
                                                    topn=iMaxNrOfRelatedTerms)
                  if x[1] >= fMinDist]
  
  # Add the seed terms and make them unique 
  aNewTerms = list(set(aNewTerms + aTerms))

  aEmbeddings = [oModel[sTerm] for sTerm in aNewTerms if sTerm in oModel]
  npaEmbeddings = np.array(aEmbeddings, dtype=float)

  # Get the mean
  npaMean = npaEmbeddings.mean(axis=0)

  # Prune
  while npaEmbeddings.shape[0] > iMaxNrOfTerms:
    # Find out which term is farthest away 
    iDelIndex = None
    if sDist == 'cosine':
      npaCosineSims = cosineSimilarities(npaEmbeddings, np.array([npaMean]))
      iDelIndex = \
          cosineSimilarities(npaEmbeddings, np.array([npaMean])).argmin()
    elif sDist == 'eucl':
      iDelIndex = \
          euclidean_distances(npaEmbeddings, np.array([npaMean])).argmax()
    print "Throwing out %s" % aNewTerms[iDelIndex]
    # Cut it from the embeddings
    npaEmbeddings = npaEmbeddings[range(iDelIndex) + \
                                    range(iDelIndex+1, npaEmbeddings.shape[0])]
    # Also cut it from the term list
    aNewTerms = aNewTerms[:iDelIndex] + aNewTerms[iDelIndex+1:]
    # Take a new mean
    npaMean = npaEmbeddings.mean(axis=0)

  return aNewTerms                              

def surroundingWords(oModel, npaWordVector, fMinDist, iTopN, bDebug=False):
  # The following code is along the lines of gensim's most_similar() function
  npaDistances = np.dot(oModel.syn0norm,
                        matutils.unitvec(npaWordVector))

  if bDebug:
    import pdb
    pdb.set_trace()

  npaBestIndices = np.argsort(npaDistances)[::-1][:iTopN]
  dResults = {oModel.index2word[x]: npaDistances[x] for x in npaBestIndices \
                if x >= fMinDist}
  aResult = []

  aSortedKeys = sorted(dResults.keys(), key=dResults.__getitem__, reverse=True)

  for sWord in aSortedKeys:
    aResult.append("%s (%.2f)" % (sWord, dResults[sWord]))
    if len(aResult) == iTopN:
      break

  return aResult

def initialVectors(oModel, sModelName, aTerms):
  # Allocate space
  #npaVectors = np.empty([len(aTerms), oModel.layer1_size])
  aWordEmbeddings = []

  for sTerm in aTerms:
    try:
      aWordEmbeddings.append(oModel[sTerm])
    except KeyError:
      print "[WARNING]: Word %s is unknown in %s" % (sTerm, sModelName)

  return aWordEmbeddings

def trackAreaInSpace(dModels, aTerms, fMinDist=0.1, iTopN=10,
                     bForward=True, bDebug=False):
  aModelKeys = sorted(dModels.keys()) if bForward \
      else sorted(dModelskeys(), reverse=True)

  npaInitialVectors = \
      initialVectors(dModels[aModelKeys[0]], aModelKeys[0], aTerms)

  if npaInitialVectors is None:
    return None
    
  for sModelKey in aModelKeys:
    print sModelKey[0:4]
    for iIndex in range(len(aTerms)):
      print "%s: %s" % (aTerms[iIndex],
                        surroundingWords(dModels[sModelKey],
                                         npaInitialVectors[iIndex],
                                         fMinDist, iTopN, bDebug=bDebug))

## Storing function ###########################################################

def storeAllResults_fromFile(sInputFile, sOutputDir, dModels, bVerbose=False,
                             bTrackWords=True):
  fhInput = codecs.open(sInputFile, mode='r', encoding='utf8')

  iLineNr = 0
  for sLine in fhInput:
    iLineNr += 1
    if sLine[0] == '#':
      continue
    sSeedWords, sDirection, sDescription = sLine.strip().split("\t")
    aSeedTerms = sSeedWords.split(" ")

    if sDirection not in ['forwards', 'backwards']:
      print "[ERROR] no valid direction on line %d: %s" % (iLineNr, sLine)
      exit(1)

    storeAllResults(sOutputDir, dModels, aSeedTerms, sDirection=sDirection,
                    sDescription=sDescription, bVerbose=bVerbose,
                    bTrackWords=bTrackWords)

  fhInput.close()

def storeAllResults(sOutputDir, dModels, aSeedTerms, iMaxNrOfTerms=10,
                    iMaxNrOfRelatedTerms=10, sStartKey=None, sEndKey=None,
                    sDirection='forwards', sDescription='',
                    # fSeedWordBoost=1.00,
                    bDebug=False, bVerbose=False, bTrackWords=True):

  if sDirection not in ['forwards', 'backwards']:
    print "[ERROR] %s is not a valid direction" % sDirection
    exit(1)

  for fMinDist in [.6, .65, .7]:
    sFileAppendix = "minDist_%s_%s" % ( ("%f" % fMinDist).replace('.', '_'),

                                      "_".join(aSeedTerms))

    if bTrackWords:
      # Just track the words
      sFileName = "trackWords_%s.txt" % sFileAppendix
      if bVerbose:
        print "Doing %s" % sFileName 
      sOutputFile = os.path.join(sOutputDir, sFileName)
      trackWords(dModels, aSeedTerms, sDirection, sDescription,
                 sOutputFile=sOutputFile,
                 iMaxNrOfRelatedTerms=iMaxNrOfRelatedTerms, fMinDist=fMinDist)

    # Track clouds
    for bOutlinks in [True, False]:
      sLinkType = 'outlinks' if bOutlinks else 'inlinks';
      for bSumOfDistances in [True, False]:
        sSumOfDist = 'weightedSum' if bSumOfDistances else 'noWeightedSum';
  
        sFileName = "trackClouds_%s_%s_%s_%s.txt" % \
            (sDirection, sLinkType, sSumOfDist, sFileAppendix)
        if bVerbose:
          print "Doing %s" % sFileName 
        sOutputFile = os.path.join(sOutputDir, sFileName)
  
        trackClouds3(dModels, aSeedTerms, sOutputFile=sOutputFile,
                     iMaxNrOfTerms=iMaxNrOfTerms, 
                     iMaxNrOfRelatedTerms=iMaxNrOfRelatedTerms,
                     sStartKey=sStartKey, sEndKey=sEndKey,
                     fMinDist=fMinDist, 
                     #fSeedWordBoost=fSeedWordBoost,
                     sDirection=sDirection, sDescription=sDescription,
                     bSumOfDistances=bSumOfDistances,
                     bOutlinks=bOutlinks)
