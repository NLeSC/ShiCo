# -*- coding: utf-8 -*-

import sys
import re
from nltk.tokenize.punkt import PunktSentenceTokenizer
import codecs


class kbTokenizer:

    '''Tokenizer used to pre-process KB dataset for generating Word2Vec models
    from word2vecModels/*.w2v. '''

    def __init__(self, bLowerCase=True):
        self.bLowerCase = bLowerCase

        self.oPunktSentTokenizer = PunktSentenceTokenizer()

        self.sNonTokenChars = (u"[‘’“”…”’“–«»\,‘\]\[;:\-\"'\?!¡¢∞§¶•ª≠∑´®†¨^π"
                               "ƒ©˙∆˚¬≈√∫~⁄™‹›ﬁﬂ‡°·±—‚„‰∏”`◊ˆ~¯˘¿÷\*\(\)<>="
                               "\+#^\\\/_]+")
        self.reNonTokenChars_start = \
            re.compile(u"(\A|\s)%s" % self.sNonTokenChars, re.U)
        self.reNonTokenChars_end = \
            re.compile(u"%s(\.?(\s|\Z))" % self.sNonTokenChars, re.U)
        self.reWhitespace = re.compile("\W+", re.U)

    def removeNonTokenChars(self, sString):
        sString = re.sub(self.reNonTokenChars_start, '\g<1>', sString)
        return re.sub(self.reNonTokenChars_end, '\g<1>', sString)

    def tokenizeSentence(self, sString):
        aTokens = None
        if self.bLowerCase:
            aTokens = self.reWhitespace.split(
                self.removeNonTokenChars(sString.lower()))
        else:
            aTokens = self.reWhitespace.split(
                self.removeNonTokenChars(sString))

        # split() gives empty first/last elements if there were separators at
        # the start/end of the string (so whitespace, in this case).
        # We correct for that.
        iStart = 1 if aTokens[0] == '' else 0
        if aTokens[-1] == '':
            return aTokens[iStart:-1]
        else:
            return aTokens[iStart:]

    def tokenizeText(self, sText):
        '''
        Input is a utf8 text.
        Output is a list of lists of tokens. One list of tokens per sentence.
        '''
        aTextTokens = []
        for sSentence in self.oPunktSentTokenizer.sentences_from_text(sText):
            aTokens = self.tokenizeSentence(sSentence)

            if len(aTokens) > 0:
                aTextTokens.append(aTokens)

        return aTextTokens

    def tokenizeFile(self, sFile):
        try:
            fhInput = codecs.open(sFile, mode='r', encoding='utf8')
        except IOError, oError:
            print >>sys.stderr, "[ERROR] Error while opening '%s'" % sFile
            print >>sys.stderr, "[ERROR] '%s'" % oError
            exit(1)

        sText = fhInput.read()
        fhInput.close()

        return self.tokenizeText(sText)

if __name__ == "__main__":
    ''' Run:
    $ python kbTokenizer.py example_files/ddd\:011184560\:mpeg21\:a0001.txt
    This will print a list of tokens for each sentence in the file.
    '''
    import argparse
    oArgsParser = argparse.ArgumentParser(
        description='Tokenize a KB text file.')
    oArgsParser.add_argument('INPUT_FILE')
    oArgs = oArgsParser.parse_args()

    # To make the printing go right, we make sure that the output is utf8
    # encoded. In general, it might be a good idea to set the Pythion IO
    # encoding envirnoment variable: PYTHONIOENCODING=utf8
    if sys.stdout.encoding != 'utf8':
        sys.stdout = codecs.getwriter('utf8')(sys.stdout)

    oKbTokenizer = kbTokenizer()

    aTextTokens = oKbTokenizer.tokenizeFile(oArgs.INPUT_FILE)

    for aSentenceTokens in aTextTokens:
        print "%s" % aSentenceTokens
