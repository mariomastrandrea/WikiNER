# WikiNER

## Project description
This project aims at evaluating the performances of a brute-force model for a Named Entity Recognition task, leveraging the Wikipedia most ranked Named Entities, and comparing them to the performances of a fine tuned BERT model.
We used the CoNLL2003 dataset to evaluate the performances of the two different models.

## Project structure
Main files/directories:
- `src/` -> contains all the python source code files
    - `bert/` -> contains the script to execute the BERT model on CoNLL2003
    - main/ -> contain the main scripts to retrieve Wikipedia top-N entities and save them in an output .csv file, and test the tagger algorithm
    - model/ -> contains the main functions to retrieve the Wikipedia Entities labels by means of the API, and to tag a sentences using a predefined tagging scheme (BIO or BILOU)  
    - `test/` -> contains the script to execute the brute force model over the CoNLL2003 dataset printing the performances on the screen

- wiki_NEs/ -> contains all the retrieved Wikipedia Named Entities' labels, based on top-N number and presence of aliases or not (the model has been run using this pre-computed files, instead of always computing the labels on the fly) 

- wikipedia_raw_NEs/ -> it contains the original file of the raw Wikidata NEs, without labels

- COM S579.ipynb -> python notebook with the first tasks, regarding Wikipedia NEs retrieval and brute-force model
- `COM S579_BERTModel.ipynb` -> python notebook containing the BERT model evaluation over CoNLL2003 

- run_WikiNER.sh -> script to run the brute-force model over CoNLL2003 (and installing all the required dependencies)
- run_BERT.sh -> script to run the BERT model over CoNLL2003 (after installing all the required dependencies)

- WikiNER_presentation_OLD.pdf -> project presentation showed in class (12/08/2022), *incomplete* (missing BERT model results)
- `WikiNER_presentation_final.pdf` -> *complete* Project presentation


## How to run the project
The project is composed of two distinct runs:
1. The brute-force model over CoNLL2003
2. The BERT model over CoNLL2003

The results of both are printed on the console after the complete execution

### Run WikiNER (brute-force model)
To run the brute-force model, retrieving the `top 1000` Wikipedia NEs labels (`with aliases`) on-the-fly, and using them to tag CoNLL2003 to evaluate the performances, open the main directory of the project containing the *run_WikiNER.sh* script and execute it: 
```code 
sh run_WikiNER.sh
```
The script will take about a 2 hours to finish and the result will appear on the console. 
The obtained result will be the same as the one in the slide n.16 in the final presentation, in the right table (with aliases) and 2nd row (top 1000 NEs).

To run the model using different parameters rather than the default ones (top_N=1000 and aliases=true), just run the run_WikiNER.sh with additional parameters:
```code 
sh run_WikiNER.sh [top N] [true/false]
```
where *top N* is the number of top NEs used and the second is a boolean stating if using NE aliases(true) or not(false)

### Run BERT model
To run the BERT model, open the main directory of the project containing the *run_BERT.sh* script and execute it: 
```code 
sh run_BERT.sh
```
The script will take about 5-6 hours to finish, and the result will appear on the console.
Unfortunately all the output is mixed with the progress updates of the training/validation, but scrolling up you can see 3 lines showing the results, one per each epoch. For example, this is the one after the 3rd epoch:
```code
{'eval_loss': 0.03649309277534485, 'eval_precision': 0.9443980631157122, 'eval_recall': 0.9518680578929654, 'eval_f1': 0.948118347162853, 'eval_accuracy': 0.9912191892839064, 'eval_runtime': 392.1533, 'eval_samples_per_second': 8.288, 'eval_steps_per_second': 0.52, 'epoch': 3.0}
```
The other 2 lines (for 1st and 2nd epoch) have the exact same format.

The obtained result will be the same as the one in the slide `n.25` of the final presentation, in the showed table.
(The screenshots showed in the slides, the cited steps, and the final results come from the COM_S579_BERTModel.ipynb notebook, so the performances numbers could have slightly differences in decimals)  

The checkpoints results of the script are also saved in the directory `bert-conll2003-test-output/`

## Authors
Mario Mastrandrea, Yuting Yang
