#!/bin/bash

# install all the dependencies
pip3 install ipywidgets
pip3 install datasets
pip3 install transformers
pip3 install evaluate
pip3 install spacy
pip3 install nltk
pip3 install seqeval
pip3 install torch torchvision torchaudio

# run script execute BERT model over CoNLL2003 dataset
python3 -m src.bert.bert_conll2003_test 
