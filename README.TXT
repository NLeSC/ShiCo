VERSION 0.0000001

This is version 0.000001 (as in, I just dumped the code, no comments, no code cleaning whatsoever...).
Actually, the only functions of interest are:
- trackClouds3() - the "adaptive" method
- trackWord() - gives you the related words of a particular word over time 

All the other functions are earlier attempts that I ended up not using.
I didn't throw them out yet for fear of breaking things.

If you are interested in seeing term frequencies of words, you can use the
termFrequencies module. It works in a fashion very similar to
trackClouds()/trackWords(), see the snippet below.

### Example snippet ###########################################################

As the word2vec models take a long time to load it is actually mos convenient
to play around with this in a python shell.

What I typically do is:

$ python
Python 2.7.3 |CUSTOM| (default, Apr 11 2012, 17:52:16) 
[GCC 4.1.2 20080704 (Red Hat 4.1.2-44)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import shiftingVocabularyMonitor as shVM

>>> # NOTE that we only want to load the w2v models, NOT the .vocab.w2v files
>>> allModels = shVM.loadAllModels("path/to/word2vecModels/????_????.w2v")

>>> shVM.trackClouds3(allModels, ['rationalisatie'], fMinDist=.65, bSumOfDistances=True)
1950_1959: rationalisatie (1.00), rationalisering (0.33), automatisering (0.33), mechanisering (0.32), intensivering (0.32), specialisatie (0.31), mechanisatie (0.25)
1951_1960: rationalisatie (2.50), mechanisering (2.44), mechanisatie (2.41), intensivering (2.25), rationalisering (2.21), automatisering (1.87), specialisatie (1.34), perfectionering (0.96), industrialisatie (0.96), motorisering (0.67)
1952_1961: mechanisatie (2.98), automatisering (2.88), rationalisatie (2.78), mechanisering (2.72), rationalisering (2.42), intensivering (2.25), industrialisatie (1.99), motorisering (1.99), perfectionering (1.96), specialisatie (1.65)
...
...

>>>