#!/usr/bin/env python

import gensim
import numpy as np
import sys
import matplotlib.pyplot as plt

def compare(w):
    v1 = A[w]
    v1p = transform.T.dot(v1)
    W1p = V2W_B(v1p)
    v2 = B[w]
    W2 = V2W_B(v2)
    printVocabTopW(B, W2, 10)
    print "----", np.dot(v2, v1p)
    printVocabTopW(B, W1p, 10)

def printVocabTopW (A, W, top=20):
    best = W.argsort()[::-1]
    for idx in best[:top]:
        print "%30s %f" % (A.index2word[idx], W[idx])
    #best = best[::-1]
    #for idx in best[:top]:
    #    print "%30s %f" % (A.index2word[idx], W[idx])

def WfromAtoB(W1,A,B):
    N = len(B.vocab)

    # vector in space 2
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
    # we dropped elements, so the lenght will have changed, renormalize
    return W2 * np.linalg.norm(W1) / np.linalg.norm(W2)




try:
    transform = np.load('transform.npy')
    print 'loaded transform matrix'
except:
    transform = np.zeros([300,300])
    print 'Could not load transform matrix'

model1_name = '/data/hdd/ShiCo/1950_1959.w2v'
model2_name = '/data/hdd/ShiCo/1951_1960.w2v'

A = gensim.models.word2vec.Word2Vec.load_word2vec_format(model1_name, binary=True)
Ainv = np.linalg.pinv(A.syn0norm)

B = gensim.models.word2vec.Word2Vec.load_word2vec_format(model2_name, binary=True)
Binv = np.linalg.pinv(B.syn0norm)

# Word vector over the vocabulary A to a vector in the embedded space
def W2V_A(W):
    return (A.syn0norm.T).dot(W)

# Word vector over the vocabulary B to a vector in the embedded space
def W2V_B(W):
    return (B.syn0norm.T).dot(W)

# Vector in the semantic space, embedded in A, to a vector over the vocabulary A
def V2W_A(V):
    v = (Ainv.T).dot(V)
    return v

# Vector in the semantic space, embedded in B, to a vector over the vocabulary B
def V2W_B(V):
    v = (Binv.T).dot(V)
    return v


# for each dimension in the semantic, embedded, space
for i in range(0,300):
    # for redoing when crashed..
    if transform[i].max() > 0:
        print "Pass: ", i
        continue

    # build a unit vector
    v1 = np.zeros(300) # vector in space 1
    v1[i] = 1
  
    # build a vector over the vocabulary A from it 
    W1 = V2W_A(v1)

    # as vocabulary A and B do not have to be the same, reconstruct a vector over vocabulary B
    W2 = WfromAtoB(W1,A,B)

    # find the wordvector in the embbed space again
    v2 = W2V_B(W2)

    # add it to the transformation matrix
    transform[i,:] = v2
    np.save('transform.npy', transform)
