from src.model.tagger import brutal_force_NER
from seqeval.metrics import classification_report

from src.utilities import print_percentage

"""
This file contains generic functions to test our tagging model against some datasets,
both in the case the dataset is already tokenized or not
"""


def test_on_tokenized_dataset(
        sentences_tokens,  # list[list[str]]
        ground_truth_tag_sequences,  # list[list[str]]
        NE_list,  # list[str]
        tokenizer,
        scheme="BIO"
):
    """
    Test the brute-force tagging over a *tokenized* dataset: tag all the (tokenized) sentences and compare
    the results with the provided dataset tags
    :param sentences_tokens: list of sentences' tokens (each sentence is a list of string tokens)
    :param ground_truth_tag_sequences: list of provided tags for each sentence. It contains a list of
                                        tags for each sentence
    :param NE_list: list of (string) Named Entities used to tag the sentences
    :param tokenizer: the same tokenizer object used to tokenize the sentences. It has a .tokenize(str) method
    :param scheme: tagging scheme used to tag the sentences
    :return: a global performances report reflecting the quality of the brute-force tagging over the dataset
    """
    predicted_tag_sequences = []

    # compute the predicted tag sequences for all the sentences and store them in 'predicted_tag_sequences'
    for i, sentence_tokens in enumerate(sentences_tokens):
        # compute tags
        predicted_tag_sequence = brutal_force_NER(sentence_tokens, NE_list, tokenizer, scheme)
        # save them
        predicted_tag_sequences.append(predicted_tag_sequence)
        # print loading percentage
        print_percentage(i+1, len(sentences_tokens))

    print()     # print new line

    # compute the performances: summary of the precision, recall, F1 score for each class
    performance_metrics = classification_report(
        ground_truth_tag_sequences,
        predicted_tag_sequences
    )

    return performance_metrics



def test_on_dataset(
        sentences,  # list[str]
        ground_truth_tag_sequences,  # list[list[str]]
        NE_list,  # list[str]
        tokenizer,
        scheme="BIO"
):
    """
    Test the brute-force tagging over a (not tokenized) dataset: tag all the (string) sentences and compare
    the results with the provided dataset tags
    :param sentences: list of (string) sentences
    :param ground_truth_tag_sequences: list of provided tags for each sentence. It contains a sequence of
                                        tags for each sentence
    :param NE_list: list of (string) Named Entities used to tag the sentences
    :param tokenizer: the tokenizer object to be used to tokenize the sentences and the Named Entities.
    It has to have a .tokenize(str) method, and it must reflect the tokenization of the dataset
    :param scheme: tagging scheme used to tag the sentences
    :return: a global performances report reflecting the quality of the brute-force tagging over the dataset
    """
    predicted_tag_sequences = []

    # compute the predicted tag sequences for all the sentences and store them in 'predicted_tag_sequences'
    for sentence in sentences:
        sentence_tokens = tokenizer.tokenize(sentence)
        predicted_tag_sequence = brutal_force_NER(sentence_tokens, NE_list, tokenizer, scheme)
        predicted_tag_sequences.append(predicted_tag_sequence)

    # compute the performances: summary of the precision, recall, F1 score for each class
    performance_metrics = classification_report(
        ground_truth_tag_sequences,
        predicted_tag_sequences
    )

    return performance_metrics
