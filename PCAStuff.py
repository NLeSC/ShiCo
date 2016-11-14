#!/usr/bin/env python

import gensim
import numpy as np

# model1_name = '/data/hdd/ShiCo/1950_1959.w2v'
# model2_name = '/data/hdd/ShiCo/1951_1960.w2v'
# A = gensim.models.word2vec.Word2Vec.load_word2vec_format(model1_name, binary=True)
# Ainv = np.linalg.pinv(A.syn0norm)
# B = gensim.models.word2vec.Word2Vec.load_word2vec_format(model2_name, binary=True)
# Binv = np.linalg.pinv(B.syn0norm)

def model_load(name):
  A = gensim.models.word2vec.Word2Vec.load_word2vec_format(name, binary=True)
  Ainv = np.linalg.pinv(A.syn0norm)
  return A, Ainv

# for each dimension in the semantic, embedded, space
def calculateTransform(A,Ainv,B,Binv, sameVocab=False):

    Nembedded, Nfull = np.shape(Ainv)
    transform = np.zeros([Nembedded, Nembedded])

    for i in range(0,Nembedded):
        # build a unit vector
        v1 = np.zeros(Nembedded) # vector in space 1
        v1[i] = 1
      
        # build a vector over the vocabulary A from it, by using the inverse of the W2V mapping
        W1 = V2W(Ainv, v1)
    
        if sameVocab:
            # user insists the vocabularies are the same, so W2 :== W1
            W2 = W1
        else:
            # as vocabulary A and B do not have to be the same, reconstruct a vector over vocabulary B
            W2 = WordFromVocab2Vocab(W1, A, B)

        W2 /= np.linalg.norm(W2)
    
        # find the wordvector in the embbed space again
        v2 = W2V(B, W2)
        v2 /= np.linalg.norm(v2)
    
        # add it to the transformation matrix
        transform[i,:] = v2
    return transform

def compare(w):
    v1 = A[w]
    v1p = transform.T.dot(v1)
    v1p /= np.linalg.norm(v1p)

    W1p = V2W(Binv, v1p)
    W1p /= np.linalg.norm(W1p)

    v2 = B[w]

    W2 = V2W(Binv, v2)
    W2 /= np.linalg.norm(W2)

    printVocabTopW(B, W2, 10)
    print "----", np.dot(v2, v1p)
    printVocabTopW(B, W1p, 10)

def printVocabTopW (A, W, top=20, neg=False):
    best = W.argsort()[::-1]
    for idx in best[:top]:
        print "%30s %f" % (A.index2word[idx], W[idx])
    if neg:
        best = best[::-1]
        for idx in best[:top]:
            print "%30s %f" % (A.index2word[idx], W[idx])

def printVocabChange (A, Wa, B, Wb, top=20, neg=False):
    bestA = Wa.argsort()[::-1]
    bestB = Wb.argsort()[::-1]
    for idx, idy in zip(bestA[:top], bestB[:top]):
        print "%30s %f  %f  %30s %f" % (A.index2word[idx], Wa[idx], Wb[idx], B.index2word[idy], Wb[idy])
    if neg:
        bestA = bestA[::-1]
        bestB = bestB[::-1]
        for idx, idy in zip(bestA[:top], bestB[:top]):
            print "%30s %f  %f  %30s %f" % (A.index2word[idx], Wa[idx], Wb[idx], B.index2word[idy], Wb[idy])

def WordFromVocab2Vocab(W1,A,B):
    # vector in space 2
    N = len(B.vocab)
    W2 = np.zeros(N)
   
    # for each dimension in the vocabulary B
    for j in range(N):
        # find the corresponding word in B
        word = B.index2word[j]
       
        # if this word is vocabulary A,
        if word in A.vocab:
            # get its index in vocabulary A
            ii = A.vocab[word].index
            # and add its word vector to our result with the proper weight
            W2[j] = W1[ii]
        else:
            pass
    return W2

# Returns a unit vector over the vocabulary with the component for the given text set to 1
def TextToWord(A, text):
    result = np.zeros( len(A.vocab) )
    result [ A.vocab[text].index ] = 1
    return result

# Word vector over the vocabulary a vector in the embedded space
def W2V(M, W):
    return (M.syn0norm.T).dot(W)

# Vector in the semantic space to a vector over the vocabulary
def V2W(Minv, v):
    return (Minv.T).dot(v)
