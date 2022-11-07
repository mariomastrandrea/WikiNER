import json
import sys

from src.model.preprocesser import get_NEs_from_file
from src.model.tagger import Tokenizer
from tag_test import test_on_tokenized_dataset
from urllib.request import urlopen


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


def get_huggingface_dataset(dataset_name, config, split):
    response = urlopen(
        f"https://datasets-server.huggingface.co/first-rows?dataset={dataset_name}&config={config}&split={split}")
    json_dataset = json.loads(response.read())
    return json_dataset


def from_nums_to_letters_tags(num_tags, scheme="BIO"):
    """
    Transform a huggingface num tags sequence in a *letters* tags sequence
    :param num_tags: list of num tags
    :param scheme: adopted tagging scheme
    :return: list of letter tags according to the provided scheme
    """
    if scheme == "BIO":
        """
        mapping = {
            0: "O",
            1: "B-PER",
            2: "I-PER",
            3: "B-ORG",
            4: "I-ORG",
            5: "B-LOC",
            6: "I-LOC",
            7: "B-MISC",
            8: "I-MISC"
        }
        """
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
    else:
        print(f"Error: not valid scheme \"{scheme}\"", file=sys.stderr)
        exit(1)

    # substitute each num with the corresponding letter
    tags_iterator = map(lambda num: simplified_mapping[num], num_tags)

    # return a list of letters tags
    return list(tags_iterator)


if __name__ == "__main__":
    _dataset_name = "conll2003"
    _config = "conll2003"
    _split = "train"

    # get the dataset dict from huggingface API - first 100 rows
    _dataset = get_huggingface_dataset(_dataset_name, _config, _split)

    # build a list of sentences tokens
    _sentences_tokens = list(map(lambda row: row["row"]["tokens"]  , _dataset["rows"]))

    # build a list of sentences tags, according to the (simplified) BIO scheme (just "B", "I" and "O")
    _sentences_tags = list(map(lambda row: from_nums_to_letters_tags(row["row"]["ner_tags"]),
                               _dataset["rows"]))

    # ---------------------------------------------------
    # print sentences tokens
    # print("\n".join(str(x) for x in _sentences_tokens))

    # print sentences letters tags
    # print("\n".join(str(x) for x in _sentences_tags))
    # ---------------------------------------------------

    # retrieve Named Entities list
    _NEs_filepath = "../../output/test1000_w_aliases.csv"
    _NEs_list = get_NEs_from_file(_NEs_filepath)

    output = test_on_CONLL(_sentences_tokens, _sentences_tags, _NEs_list)
    print(output)









