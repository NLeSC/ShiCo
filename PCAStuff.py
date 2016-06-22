#!/usr/bin/env python

# coding: utf-8

# In[1]:

import gensim
import numpy as np
import sys
import matplotlib.pyplot as plt

print sys.stdout.encoding

model1_name = '/data/hdd/ShiCo/1950_1959.w2v'
model2_name = '/data/hdd/ShiCo/1951_1960.w2v'

model1 = gensim.models.word2vec.Word2Vec.load_word2vec_format(model1_name, binary=True)
model2 = gensim.models.word2vec.Word2Vec.load_word2vec_format(model2_name, binary=True)

M1pinv = np.linalg.pinv(model1.syn0norm).T

transform = np.zeros([300,300])

for i in range(300):

    v1 = np.zeros(300) # vector in space 1
    v1[i] = 1
    
    words = np.dot(M1pinv, v1)
    best = words.argsort()[::-1]
    print "Dimension", i
    for w in best[0:50]: 
      print "%30s %f" % (model1.index2word[w], words[w])
    print

    plt.figure()
    plt.plot(words[best])
    plt.savefig('em1_%03i_in_vocab1.png' % i)

    v2 = np.zeros(300) # vector in space 2
    missing_vocab = []
    for w1 in range(len(words)):
        word1 = model1.index2word[w1]
        if word1 in model2.vocab:
            v2 = v2 + words[w1] * model2.syn0norm[w]
        else:
            missing_vocab.append(word1)
    v2 = v2 / np.linalg.norm(v2)
     
    transform[i,:] = v2

    plt.figure()
    v2.sort()
    plt.plot(v2)
    plt.savefig('em1_%03i_in_em2.png' % i)

    np.save('transform.np', transform)

sys.exit(-1)



print "Most similar words"

print " = Model 1 = "
for w,_ in model1.most_similar('stoel', topn=10):
    print w

print " = Model 2 = "
for w,_ in model2.most_similar('stoel', topn=10):
    print w


print "Amsterdam + Antwerpen - Nederland = "

#print " = Model 1 = "
#vocab = model1.most_similar(positive=['amsterdam', 'antwerpen'], negative=['nederland'])
#for w, _ in vocab:
#    print w

#print " = Model 2 = "
#vocab = model2.most_similar(positive=['amsterdam', 'antwerpen'], negative=['nederland'])
#for w, _ in vocab:
#    print w

for i in range(300):
    x = np.zeros(300)
    x[i] = 1
    dist_from_x = model1.syn0norm.dot(x)
    # print dist_from_x.shape # (692536, )
    # print model1.syn0.shape # (692536, 300)
    idxmax, idxmin = dist_from_x.argmax(), dist_from_x.argmin()
    wordMax1 = model1.index2word[idxmax]
    wordMin1 = model1.index2word[idxmin]

    dist_from_x = model2.syn0norm.dot(x)
    idxmax, idxmin = dist_from_x.argmax(), dist_from_x.argmin()
    wordMax2 = model2.index2word[idxmax]
    wordMin2 = model2.index2word[idxmin]

    s = '%20s %20s   -   %20s %20s' % (wordMax1, wordMax2, wordMin1, wordMin2)
    print s.decode('ascii') 

sys.exit(-1)


mappings = []
for i in range(300):
    x = np.zeros(300)
    x[i] = 1
    concept = model1.syn0.dot(x)
    
    idx = concept.argsort()
    idx = idx[::-1]

    accum = np.zeros(300)
    for j in idx[:100]:
        try:
            word = model1.index2word[j]
            accum += concept[j] * model2[word]
        except:
            # print 'Not in vocab: ', word
            pass
    accum /= accum.sum()
    
    sortIdx = accum.argsort()
    sortIdx = sortIdx[::-1]
    
    # print i, sortIdx[0], accum[sortIdx[0]]
    mappings.append((i, sortIdx[0], accum[sortIdx[0]]))


# In[263]:

w = [ x for _,x,_ in mappings ]
w.sort()
plot(w)
print w
len(unique(w))


# In[281]:

z = np.array([ x for _,_,x in mappings ])
zidx = argsort(z)
zidx = zidx[::-1]
plot(z[zidx])


# In[284]:

mappings = np.array(mappings)
mappings[zidx][:20]


# In[302]:

x1 = np.zeros(300)
x1[80] = 1
concept1 = model1.syn0.dot(x1)

x2 = np.zeros(300)
x2[116] = 1
concept2 = model2.syn0.dot(x2)

idxConcept1 = concept1.argsort()
idxConcept1 = idxConcept1[::-1]
idxConcept2 = concept2.argsort()
idxConcept2 = idxConcept2[::-1]

words1 = [ model1.index2word[idxc] for idxc in idxConcept1[:20] ]
words2 = [ model2.index2word[idxc] for idxc in idxConcept2[:20] ]
for w1,w2 in zip(words1, words2):
    print "%15s  %15s" % (w1,w2)
