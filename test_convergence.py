#!/usr/bin/env python

import codecs
import locale
import sys

# Wrap sys.stdout into a StreamWriter to allow writing unicode.
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout) 



import numpy as np
from PCAStuff import *

models = [
"/data/hdd/ShiCo/timesModels/1940(0).w2v",
"/data/hdd/ShiCo/timesModels/1940(50000).w2v",
"/data/hdd/ShiCo/timesModels/1940(100000).w2v",
"/data/hdd/ShiCo/timesModels/1940(150000).w2v",
"/data/hdd/ShiCo/timesModels/1940(200000).w2v",
"/data/hdd/ShiCo/timesModels/1940(250000).w2v",
"/data/hdd/ShiCo/timesModels/1940(300000).w2v",
"/data/hdd/ShiCo/timesModels/1940(350000).w2v",
"/data/hdd/ShiCo/timesModels/1940(400000).w2v",
"/data/hdd/ShiCo/timesModels/1940(450000).w2v",
"/data/hdd/ShiCo/timesModels/1940(500000).w2v",
"/data/hdd/ShiCo/timesModels/1940(550000).w2v",
"/data/hdd/ShiCo/timesModels/1940(600000).w2v",
"/data/hdd/ShiCo/timesModels/1940(650000).w2v",
"/data/hdd/ShiCo/timesModels/1940(700000).w2v",
"/data/hdd/ShiCo/timesModels/1940(750000).w2v",
"/data/hdd/ShiCo/timesModels/1940(800000).w2v",
"/data/hdd/ShiCo/timesModels/1940(850000).w2v",
"/data/hdd/ShiCo/timesModels/1940(900000).w2v",
"/data/hdd/ShiCo/timesModels/1940(950000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1000000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1050000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1100000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1150000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1200000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1250000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1300000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1350000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1400000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1450000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1500000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1550000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1600000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1650000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1700000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1750000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1800000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1850000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1900000).w2v",
"/data/hdd/ShiCo/timesModels/1940(1950000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2000000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2050000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2100000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2150000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2200000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2250000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2300000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2350000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2400000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2450000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2500000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2550000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2600000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2650000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2700000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2750000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2800000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2850000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2900000).w2v",
"/data/hdd/ShiCo/timesModels/1940(2950000).w2v",
"/data/hdd/ShiCo/timesModels/1940(3000000).w2v",
"/data/hdd/ShiCo/timesModels/1940(3050000).w2v",
"/data/hdd/ShiCo/timesModels/1940(3100000).w2v",
"/data/hdd/ShiCo/timesModels/1940(3150000).w2v",
"/data/hdd/ShiCo/timesModels/1940(3200000).w2v",
"/data/hdd/ShiCo/timesModels/1940(3250000).w2v",
"/data/hdd/ShiCo/timesModels/1940(3300000).w2v",
"/data/hdd/ShiCo/timesModels/1940(3350000).w2v",
"/data/hdd/ShiCo/timesModels/1940(3400000).w2v",
"/data/hdd/ShiCo/timesModels/1940(3450000).w2v",
"/data/hdd/ShiCo/timesModels/1940(3500000).w2v",
"/data/hdd/ShiCo/timesModels/1940(3550000).w2v",
"/data/hdd/ShiCo/timesModels/1940(3600000).w2v",
"/data/hdd/ShiCo/timesModels/1940(3650000).w2v",
"/data/hdd/ShiCo/timesModels/1940(3700000).w2v"
]

final_model = "/data/hdd/ShiCo/timesModels/1940(3700000).w2v"
F, Finv = model_load(final_model)

for i in range(0, len(models)-1):
  A, Ainv = model_load(models[i])
  B, Binv = model_load(models[i + 1])

  # similarity with next, i+1, model
  Tab = calculateTransform(A, Ainv, B, Binv, sameVocab=True)
  Tba = calculateTransform(B, Binv, A, Ainv, sameVocab=True)
  TTinv = Tab * Tba
  Si_ip = np.trace(TTinv)  / 300

  # similarity with 'best' model
  Taf = calculateTransform(A, Ainv, F, Finv, sameVocab=True)
  Tfa = calculateTransform(F, Finv, A, Ainv, sameVocab=True)
  Si_if = np.trace(Taf * Tfa)  / 300

  print 'Step:', i, models[i], Si_ip, Si_if

  # how did dimension change? what dimension changed most?
  print "Diag ", i, " :",
  diag = np.zeros(300)
  for i in range(300):
    diag[i] = np.abs(1 - TTinv[i,i])
    print diag[i],
  print
  most_changed = diag.argmax()
  least_changed = diag.argmin()


  # what does the dimension look like?

  least = np.zeros(300)
  least[most_changed] = 1

  print 'Most changed:', most_changed, diag[most_changed]
  most = np.zeros(300)
  most[most_changed] = 1
  Wa = V2W(Ainv, most)
  Wb = V2W(Binv, most)
  printVocabChange(A, Wa, A, Wb, 20, False)

  print 'Least changed;', least_changed, diag[least_changed]
  least = np.zeros(300)
  least[least_changed] = 1
  Wa = V2W(Ainv, least)
  Wb = V2W(Binv, least)
  printVocabChange(A, Wa, A, Wb, 20, False)
