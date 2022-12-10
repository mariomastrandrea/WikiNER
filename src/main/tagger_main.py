import datasets

from src.model.NEs_loader import get_NEs_from_file
from src.model.objects.default_tokenizer import Tokenizer
from src.model.tagger import brutal_force_NER


def format_tags(tags, sentence):
    sentence_tokens = Tokenizer().tokenize(sentence)
    result = []

    for token, tag in zip(sentence_tokens, tags):
        formatted_tag = tag + (" " * (len(token) - 1))
        result.append(formatted_tag)

    return " ".join(result)


if __name__ == "__main__":
    # tagging a random sentence using a crafted list of NEs
    
    _NE_list = ["Microsoft", "Iowa State", "Fall 2022", "Deep Learning", "Iowa State University", "2022", "school"]
    _sentence = "I went to school at Iowa State University in Fall 2022"

    _tokenizer = Tokenizer()

    BIO_tags = brutal_force_NER(_tokenizer.tokenize(_sentence), _NE_list, _tokenizer, scheme="BIO")
    BILOU_tags = brutal_force_NER(_tokenizer.tokenize(_sentence), _NE_list, _tokenizer, scheme="BILOU")

    # print results
    BIO_formatted_tags = format_tags(BIO_tags, _sentence)
    BILOU_formatted_tags = format_tags(BILOU_tags, _sentence)
    print(f"{_NE_list}\n\n{_sentence}\n{BIO_formatted_tags}\n{BILOU_formatted_tags}")
    """

    # tagging the first sentence of the conll2003 dataset using a Wikipedia NEs list
    dataset = datasets.load_dataset("conll2003", split="train")
    _NE_list = get_NEs_from_file("../../wiki_NEs/test10000_w_aliases.csv")
    _sentence_tokens = dataset[3]["tokens"]
    _tokenizer = Tokenizer()

    BIO_tags = brutal_force_NER(_sentence_tokens, _NE_list, _tokenizer, scheme="BIO")

    BIO_formatted_tags = []

    for _token, _tag in zip(_sentence_tokens, BIO_tags):
        _formatted_tag = _tag + (" " * (len(_token) - 1))
        BIO_formatted_tags.append(_formatted_tag)

    _sentence_ = " ".join(_sentence_tokens)
    _tags_ = " ".join(BIO_formatted_tags)
    _NEs = "\n".join(_NE_list)

    print(f"\n{_sentence_}\n{_tags_}")
    """

