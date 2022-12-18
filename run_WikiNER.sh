#!/bin/bash

# install all the dependencies
pip3 install ipywidgets
pip3 install datasets
pip3 install evaluate
pip3 install spacy
pip3 install nltk
pip3 install seqeval

# take arguments
top_N=${1:-1000}
aliases=${2:-'true'}

# run script to retrieve top 1000 Wikipedia NEs and execute brute force model against CoNLL2003 dataset
python3 -m src.test.conll2003_test wikipedia_raw_NEs/qrank.csv $top_N $aliases

