
# coding: utf-8

# In[1]:

import gensim


# In[11]:

model1 = gensim.models.word2vec.Word2Vec.load_word2vec_format('./word2vecModels/1950_1959.w2v', binary=True)


# In[15]:

model2 = gensim.models.word2vec.Word2Vec.load_word2vec_format('./word2vecModels/1951_1960.w2v', binary=True)


# In[17]:

for w,_ in model1.most_similar('stoel', topn=10):
    print w
print '======='
for w,_ in model2.most_similar('stoel', topn=10):
    print w


# In[21]:

print model1.most_similar('stoel', topn=False)[:100]


# In[26]:

# model1.vocab.keys()[:100]
v = model1.vocab[u'soestdijk']


# In[44]:

import numpy as np


# In[49]:

import sklearn.decomposition


# In[153]:

#pca = sklearn.decomposition.PCA(n_components=10, whiten=True)
#pca.fit(model1.syn0)
svd = sklearn.decomposition.TruncatedSVD(n_components=10, )


# In[154]:

pca.components_.shape


# In[150]:

pca0 = pca.components_[0,:]
pca0.shape


# In[159]:




# In[180]:

for i in range(300):
    x = np.zeros(300)
    x[i] = 1
    dist_from_x = model1.syn0.dot(x)
    idxmax, idxmin = dist_from_x.argmax(), dist_from_x.argmin()
    wordMax = model1.index2word[idxmax]
    wordMin = model1.index2word[idxmin]
    print i,': ',wordMax,' '*(20-len(wordMax)),wordMin 


# In[195]:

vocab = model1.most_similar(positive=['amsterdam', 'londen'], negative=['nederland'])
for w, _ in vocab:
    print w


# In[178]:

plot(model1.syn0[idxmax,:])
plot(model1.syn0[idxmin,:])
#plot(x)
axis([-10,310,-1,2])


# In[107]:

model1.most_similar('otnen')


# # Test2

# In[198]:

v0 = model1.syn0[0,:]
v0.dot(v0)


# In[244]:

# for i in range(300):
if True:
    i = 0
    x = zeros(300)
    x[i] = 1
    concept = model1.syn0.dot(x)
    concept


# In[245]:

idx = concept.argsort()
idx = idx[::-1]
plot(concept[idx])


# In[246]:

for i in idx[:10]:
    print '%2.4f'%concept[i], model1.index2word[i]


# In[247]:

accum = np.zeros(300)
for i in idx[:100]:
    try:
        word = model1.index2word[i]
        accum += concept[i] * model2[word]
    except:
        print 'Not in vocab: ', word
accum /= accum.sum()


# In[248]:

sortIdx = accum.argsort()
sortIdx = sortIdx[::-1]
plot(accum[sortIdx])
print sortIdx[0], accum[sortIdx[0]]


# In[261]:

mappings = []
for i in range(300):
    x = zeros(300)
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


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



