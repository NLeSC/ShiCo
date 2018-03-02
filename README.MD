[![Build Status](https://travis-ci.org/NLeSC/ShiCo.svg?branch=master)](https://travis-ci.org/NLeSC/ShiCo)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1187090.svg)](https://doi.org/10.5281/zenodo.1187090)


# ShiCo --  Exploring Shifting Concepts Through Time

## What is ShiCo?

ShiCo is a tool for visualizing time shifting concepts. We refer to a concept as the set of words which are related to a given seed word. ShiCo uses a set of semantic models (word2vec) spanning a number of years to explore how concepts change over time -- words related to a given concept at time *t=0* may differ from the words related to the same concept at time *t=n*. For example:

![Mock concept shift](./docs/mockConcept1.png)
![Mock concept shift](./docs/mockConcept2.png)

You can find more details of how the concept shift works [here](./docs/howItWorks.md) and you can read the user documentation [here](./docs/ui.md).

## How to use it?
You can read how to get your own instance of ShiCo up and running [here](./docs/deploy.md).

## How to extend it
If you would like to modify ShiCo, read the developer manual [here](./docs/develop.md).

## Licensing

Source code and data of ShiCo is licensed under the Apache License, version 2.0.
