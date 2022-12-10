# usage: conll2003_test.py <input NEs file>

import sys

from src.model.NEs_loader import get_NEs_from_file
from src.model.objects.default_tokenizer import Tokenizer
from datasets import load_dataset
from src.test.generic_dataset_test import test_on_tokenized_dataset


def test_on_CONLL(
        sentences_tokens,  # list[list[str]]
        ground_truth_tag_sequences,  # list[list[str]]
        NE_list,  # list[str]
        scheme="BIO"
):
    performance_metrics = test_on_tokenized_dataset(
        sentences_tokens,
        ground_truth_tag_sequences,
        NE_list,
        Tokenizer(),
        scheme
    )

    return performance_metrics


def get_huggingface_dataset(dataset_name, split):
    # return the entire dataset
    return load_dataset(dataset_name, split=split)


def map_row_to_tokens_and_letters_tags(row):
    """
    Transform a huggingface num tags sequence in a *letters* tags sequence
    :param row: dataset row containing sentence "tokens" and a list of num "ner_tags"
    :param scheme: adopted tagging scheme
    :return: list of letter tags according to the provided scheme
    """
    # retrieve sentence tokens
    sentence_tokens = row["tokens"]

    # now compute the sentence tags
    simplified_mapping = {
        0: "O",
        1: "B",  # -PER
        2: "I",  # -PER
        3: "B",  # -ORG
        4: "I",  # -ORG
        5: "B",  # -LOC
        6: "I",  # -LOC
        7: "B",  # -MISC
        8: "I"   # -MISC
    }

    # take the NEs tags and map each num tag with the corresponding letter
    sentence_letter_tags = list(map(lambda num: simplified_mapping[num], row["ner_tags"]))

    # return a list of *sentence tokens* and a list of *letters tags*
    return sentence_tokens, sentence_letter_tags


if __name__ == "__main__":
    # input checks
    if len(sys.argv) != 2:
        print("Usage: conll2003_test.py <input NEs filepath>")
        exit()

    _NEs_filepath = sys.argv[1]

    # retrieve Named Entities list from input file
    wiki_NEs_list = get_NEs_from_file(_NEs_filepath)
    if wiki_NEs_list is None:
        exit()

    _dataset_name = "conll2003"
    _split = "train"

    # get the entire dataset dict from huggingface API
    conll2003_dataset = get_huggingface_dataset(_dataset_name, _split)

    # from the dataset, for each sentence, build:
    # - a list of sentences tokens
    # - a list of sentences tags, according to the (simplified) BIO scheme (just "B", "I" and "O")
    _sentences_tokens_and_sentences_tags_iterator = \
        map(lambda row: map_row_to_tokens_and_letters_tags(row), conll2003_dataset)

    # now save separately sentences tokens and sentences tags
    conll2003_sentences_tokens = []
    conll2003_sentences_tags   = []

    for _tuple in _sentences_tokens_and_sentences_tags_iterator:
        conll2003_sentences_tokens.append(_tuple[0])
        conll2003_sentences_tags.append(_tuple[1])

    # * execute brute-force tagging over CoNLL2003 using NEs and measure performances *
    tagging_report = test_on_CONLL(conll2003_sentences_tokens, conll2003_sentences_tags, wiki_NEs_list)
    print(tagging_report)
