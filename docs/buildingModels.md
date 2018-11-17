
# How to build your ShiCo models?
This tutorial will show you how to build your own word2vec models for using ShiCo with your own data.

First, we will create some simulated data. This is only for illustration and you should replace this part of the tutorial for something which actually loads your own data.

ShiCo works with the assumption that we have a collection of documents for a number of year. Each document is labeled with one year. A document is represented as a list of sentences contained in the document. Each sentence is in turn a list of words. Any pre-processing required should be applied to the document at this stage -- for example making all words lowercase, removing stop-words, removing unusual symbols, etc. Note that the exact details of the pre-processing are for you to decide.

The following function creates a single random document:


```python
import numpy as np

def buildRandomDoc():
    '''Create a random document with two sentences of an arbitrary length.'''
    # This is my vocabulary of possible words
    vocab = [ 'hello', 'world', 'this', 'is', 'a', 'public', 'service', 'announcement',
             'this', 'is', 'only', 'a', 'test' ]

    doc = []
    for i in range(2):   # Two sentences per document
        # Each sentence in my document will be between 10 and 20 words
        wordsInSent = 10 + np.random.randint(10)

        # Pick words randomly from vocabulary
        sent = np.random.choice(vocab, wordsInSent).tolist()
        doc.append(sent)
    return doc

def printableDocument(doc):
    '''Get printable version of a my document'''
    text = '. '.join(' '.join(sent) for sent in doc)
    return (text[:57]+'...') if len(text)>60 else text

myDoc = buildRandomDoc()
print 'A single document looks like this:\n   ',printableDocument(myDoc)
```

    A single document looks like this:
        public world announcement only only is service is public ...


But of course, you don't want to analyze a single document but rather a collection of them. In practice, we will have a list of documents for each years.

The following snippet of code will create 3 documents for each year between 1950 and 1960. Notice that all years have the same number of documents, which will not always be the case.

Now, this is how our document collection looks like:


```python
for year in range(1950,1960):
    print '%d >'%year
    for n in range(3):
        doc = buildRandomDoc()
        print '  ',printableDocument(doc)
```

    1950 >
       this test announcement a hello public test is hello a tes...
       this service only only this hello hello only a this world...
       is world a a a announcement hello hello world a public is...
    1951 >
       this this world this service this announcement this servi...
       a public a a public only service announcement this announ...
       this public a announcement test a is hello only announcem...
    1952 >
       this a service a test only is is public announcement this...
       is is service this announcement this test a a hello is a ...
       a is this this a hello service a is this. this is this pu...
    1953 >
       world only a public public public this is hello a is serv...
       this service hello announcement is service announcement p...
       this world public a this this service announcement public...
    1954 >
       is only is public is a is a public a a test a test. a onl...
       announcement service public hello public is test a a is t...
       is only this this world hello hello test world announceme...
    1955 >
       only hello world test service service this this test this...
       a this hello test this world hello service a this this wo...
       this world a announcement test this hello a this a only a...
    1956 >
       is announcement public world a test is hello is hello a. ...
       is a hello a test this public service world public is. th...
       test public hello announcement service a a is world publi...
    1957 >
       this public this service hello is is only this this. hell...
       this is a hello a public announcement only this hello a i...
       is announcement world this this world public only announc...
    1958 >
       a only only only hello hello test is announcement test a ...
       test this is this only world this test a is this this a a...
       this service a is public service is a this test a public ...
    1959 >
       public is service this service this announcement a this t...
       service this a test announcement test only announcement s...
       is only only public this a hello world is world a hello p...


# Accessing your data
There are three things we need to be able to do with your data:
 - Know when is the starting year
 - Know when is the end year
 - Retrieve documents for particular years.

So you would need to implement 3 functions:

```python
def getMinYear():
    '''Retrieves the first year on the data set.'''
    pass
```

```python
def getMaxYear():
    '''Retrieves the last year on the data set.'''
    pass
```

```python
def getDocumentsForYear(year):
    '''Retrieves a list of documents for a year specified.'''
    pass
```

These could, for example, load the data from text files, a database, a webservice, etc.

This is our implementation of these functions, but this will be different for your own set of documents:


```python
def getMinYear():
    return 1950  # This is fixed, in our dummy case

def getMaxYear():
    return 1970  # This is fixed, in our dummy case

def getDocumentsForYear(year):
    docs = []
    for n in range(10):  # Generate 10 random documents for each year
        doc = buildRandomDoc()
        docs.append(doc)
    return docs
```

## Ready to go
Once you have implemented these three functions in whichever way is most convenient for you, we are ready to go.

We can do a few checks to make sure our data is fine (you can do these checks with your own data as well).
 - Make sure that for any given year, we get a list of documents
 - Make sure documents are lists of sentences
 - Make sure sentences are in turn lists of words


```python
assert getMinYear() < getMaxYear(), \
    'minYear should be before maxYear'

anyYear = getMinYear()

listOfDocs = getDocumentsForYear(anyYear)
assert isinstance(listOfDocs, list), \
    'We should get a list of documents of any given year'

listOfSentences = listOfDocs[0]
assert isinstance(listOfSentences, list), \
    'Each document should contain a list of sentences'

listOfWords = listOfSentences[0]
assert isinstance(listOfWords, list), \
    'Each sentence should contain a list of words'

word = listOfWords[0]
assert isinstance(word, str), \
    'Words should be strings'
```

Now we can glue together sentences for a given year, and join year ranges as required.

These two functions can remain the same for your own data.


```python
def getSentencesForYear(year):
    '''Return list of lists of strings.
    Return list of sentences in given year.
    Each sentence is a list of words.
    Each word is a string.'''
    docs = getDocumentsForYear(year)

    sentences = []
    for doc in docs:
        for sent in doc:
            sentences.append(sent)
    return sentences

def getSentencesInRange(startY, endY):
    '''Return list of lists of strings.
    Return list of sentences in given year.
    Each sentence is a list of words.
    Each word is a string.'''
    return [ s for year in range(startY, endY)
               for s in getSentencesForYear(year) ]
```

## Train models
Now we can train the models. There are a few settings you can play with:

 - yearsInModel -- each model will cover several years. This controls how many years will be included in each model
 - stepYears -- this controls the year gap between models.
 - modelFolder -- folder where the models will be stored.

**NOTE:** If your models have a lot of data, it could take a while to train. Grab a coffee (or tea!), and wait.


```python
import gensim

yearsInModel = 5
stepYears = 1
modelFolder = 'tempModels'

y0 = getMinYear()
yN = getMaxYear()

for year in range(y0,yN-yearsInModel+1, stepYears):
    startY = year
    endY   = year + yearsInModel
    modelName = modelFolder + '/%d_%d.w2v'%(year,year + yearsInModel)
    print 'Building model: ',modelName

    sentences = getSentencesInRange(startY, endY)
    model = gensim.models.Word2Vec(min_count=1)
    model.build_vocab(sentences)
    model.train(sentences)

    print '...saving'
    model.init_sims(replace=True)
    model.save_word2vec_format(modelName, binary=True)
```

    Building model:  tempModels/1950_1955.w2v
    ...saving
    Building model:  tempModels/1951_1956.w2v
    ...saving
    Building model:  tempModels/1952_1957.w2v
    ...saving
    Building model:  tempModels/1953_1958.w2v
    ...saving
    Building model:  tempModels/1954_1959.w2v
    ...saving
    Building model:  tempModels/1955_1960.w2v
    ...saving
    Building model:  tempModels/1956_1961.w2v
    ...saving
    Building model:  tempModels/1957_1962.w2v
    ...saving
    Building model:  tempModels/1958_1963.w2v
    ...saving
    Building model:  tempModels/1959_1964.w2v
    ...saving
    Building model:  tempModels/1960_1965.w2v
    ...saving
    Building model:  tempModels/1961_1966.w2v
    ...saving
    Building model:  tempModels/1962_1967.w2v
    ...saving
    Building model:  tempModels/1963_1968.w2v
    ...saving
    Building model:  tempModels/1964_1969.w2v
    ...saving
    Building model:  tempModels/1965_1970.w2v
    ...saving


Now that your models have been created, you should now be ready to run your own ShiCo server!
