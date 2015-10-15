import codecs
import glob
import os

def loadTermFrequencies(sGlobPattern, dTfModels={}):
  for sVocabFile in glob.glob(sGlobPattern):
    # Chop off the path and the extension
    sModelName = os.path.splitext(os.path.basename(sVocabFile))[0]
    if sModelName.endswith('.vocab'):
      sModelName = sModelName[:-6]

    print "Loading %s" % sModelName
    dTfModels[sModelName] = termFrequencies(sVocabFile)

  return dTfModels

def tfs(dTfModels, aWords, bPrintTotalPerYear=False):
  for sModel in sorted(dTfModels.keys()):
    if bPrintTotalPerYear:
      print "%s (%d):" % (sModel, dTfModels[sModel].iTotalNrOfTokens),
    else:
      print "%s:" % sModel,
    for sWord in aWords:
      print "%s (%d)" % (sWord, dTfModels[sModel][sWord]),
    print

class termFrequencies:
  def __init__(self, sFile):
    self.dTermFrequencies = {}
    
    self.sFile = sFile # Just to remember
    self.iTotalNrOfTokens = 0
    
    fhFile = codecs.open(sFile, mode='r', encoding='utf8')
    for sLine in fhFile:
      sWord, sFreq = sLine.strip().split(' ')

      iFreq = int(sFreq)
      self.dTermFrequencies[sWord] = iFreq

      self.iTotalNrOfTokens += iFreq

    fhFile.close()

  def __getitem__(self, sTerm):
    try:
      return self.dTermFrequencies[sTerm]
    except KeyError:
      return 0

if __name__ == "__main__":
  import argparse
  oArgsParser = argparse.ArgumentParser(description='Bla')
  oArgsParser.add_argument('TERM_FREQUENCY_FILE')
  oArgsParser.add_argument('WORD', nargs='+',
                           help='Words you want the frequency for')
  oArgsParser.add_argument('-v', dest="bVerbose", help="Be verbose",
                           action="store_true")
  oArgs = oArgsParser.parse_args()

  if oArgs.bVerbose:
    print "Loading..."
  oTF = termFrequencies(oArgs.TERM_FREQUENCY_FILE)

  for sWord in oArgs.WORD:
    print "Freq of %s: %d" % (sWord, oTF[sWord])
