import datasets
from nltk.tokenize import word_tokenize

from src.model.preprocesser import get_NEs_from_file


def brutal_force_NER(sentence_tokens, NE_list, tokenizer, scheme="BIO"):
    """
    Tag a specified sentence using the provided list of NEs, following a certain tag scheme and
    using a brute-force approach
    :param sentence_tokens: the sentence tokens that have be tagged
    :param NE_list: list of NEs strings used to tag the sentence tokens
    :param tokenizer: the same tokenizer* object used to tokenize the sentence;
    it has to have a .tokenize(str) method capable of tokenize a string
    :param scheme: tag scheme to be used for tagging (default: "BIO")
    :return: the list of tags related to the provided sentence, one tag per each token
    *the tokenizer is necessary to tokenize the Named Entities accordingly with the sentence tokens
    """
    # find all the requested matches
    matches = find_not_overlapping_matches(sentence_tokens, NE_list, tokenizer)

    # representing them according to the specified scheme

    if scheme == "BIO":
        return represent_BIO_tags(sentence_tokens, matches)

    if scheme == "BILOU":
        return represent_BILOU_tags(sentence_tokens, matches)

    # * insert other tag schemes here *


def find_not_overlapping_matches(sentence_tokens, NE_list, tokenizer):
    """
    Find all the not overlapping matches of the provided Named Entities against the provided sentence
    :param sentence_tokens: list of strings representing the sentence's tokens
    :param NE_list: list of strings representing the Named Entities
    :param tokenizer: the same object used to tokenize the sentence,
    and the one which will be used to tokenize also the NEs. It has to have a .tokenize(str) method
    :return: set of not overlapping matches (a match is a dict like: {"start":x, "end":y})
    """

    matches = set()  # set where to store all the matches between a NE and the sentence's tokens
    # (a match is a dict like: { "start": x, "end": y }
    #   - x is the starting index in the sentence's tokens
    #   - y is the (exclusive) ending index in the sentence's tokens (y token is not included in the match)

    # build a helper data structure to improve detection of overlapping NEs
    # for each token, it contains the belonging match (if exist)
    tokens_matches = [None for _ in range(len(sentence_tokens))]

    for entity in NE_list:
        entity_tokens = tokenizer.tokenize(entity)  # (an entity can be composed of multiple tokens as well)
        # find NE's matches in the sentence - an entity could potentially have multiple matches
        entity_matches = find_matches_of(entity_tokens, sentence_tokens)

        # for each of the found matches check if it is overlapping with a previous existing one
        for entity_match in entity_matches:
            overlapping_matches = set()  # previous existing matches overlapping with the new one

            for token_match in tokens_matches[entity_match["start"]:entity_match["end"]]:
                # loop over the relative sentence tokens and check if they already belong to a match
                if token_match is not None:
                    overlapping_matches.add(token_match)

            if len(overlapping_matches) > 0:
                # there are overlapping matches with the new one
                # -> discard the previous overlapping matches only if this match is the *longest*

                if not is_the_longest_match(entity_match, overlapping_matches):
                    # * ignore this match *
                    break

                # this is the longest match -> discard the previous overlapping matches

                for match_to_discard in overlapping_matches:
                    # - remove from the matches list
                    matches.remove(match_to_discard)
                    # - remove references in token_matches list
                    for i in range(match_to_discard["start"], match_to_discard["end"]):
                        tokens_matches[i] = None

            # now *save the new match*

            # - add it to the matches list
            matches.add(entity_match)
            # - put references in the tokens_matches list
            for i in range(entity_match["start"], entity_match["end"]):
                tokens_matches[i] = entity_match

    return matches


def is_the_longest_match(entity_match, other_matches):
    """
    Tell if the provided match is the *only* longest among the others provided
    :return: True if it is the longest one (and no one else), False otherwise
    """
    match_len = entity_match["end"] - entity_match["start"]

    for match in other_matches:
        this_len = match["end"] - match["start"]
        if match_len <= this_len:
            return False

    return True


def find_matches_of(entity_tokens, sentence_tokens):
    """
    Return a list of matches of the specified NE in the provided sentence
    (an entity can potentially appear multiple times in the same sentence)
    """
    matches = []
    entity_len = len(entity_tokens)

    # loop over the sentence tokens, and search for the entity tokens
    for i in range(len(sentence_tokens) - entity_len + 1):
        if entity_tokens == sentence_tokens[i:i + entity_len]:
            # there is a match !
            new_match = Match(
                start=i,
                end=i + entity_len
            )
            # save the match
            matches.append(new_match)

    return matches


class Tokenizer:
    def tokenize(self, sentence):
        """
        It split a string sentence in a sequence of tokens
        :param sentence: string with the sentence
        :return: list of strings, one for each token
        """
        # todo: improve the tokenization with a tokenizer from a lib
        return word_tokenize(sentence)


class Match:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __key(self):
        return self.start, self.end

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())

    def __getitem__(self, item):
        return self.__dict__[item]


# * tag schemes functions *


def represent_BIO_tags(sentence_tokens, matches):
    """
    Return NER tags of the sentence according to the BIO* (Begin, Inside, Outside) scheme
    :param sentence_tokens: list of the tokens representing the sentence
    :param matches: all the matches we want to represent in the sentence
    :return: a list of the (ordered) BIO tags, one per each token of the sentence

    * BIO stands for "Beginning, Inside, Outside". It is a tag scheme labelling each token with one of
    these three tag (B, I, O) depending on the membership of the token in a Named Entity:
    • B (Begin)   -> if the token is the beginning of a NE;
    • I (Inside)  -> if the token belongs to a NE, but it is not the initial token
    • O (Outside) -> if the token does *not* belong to any NE
    """
    # initialize all the tags to "O" (Outside)
    tags = ["O" for _ in range(len(sentence_tokens))]

    # insert the tag related of each match
    for match in matches:
        for x in range(match["start"], match["end"]):
            # tag the start token with "B", the rest with "I"
            tags[x] = "B" if x == match["start"] else "I"

    return tags


def represent_BILOU_tags(sentence_tokens, matches):
    """
    Return NER tags of the sentence according to the BILOU* scheme
    :param sentence_tokens: list of the tokens representing the sentence
    :param matches: all the matches we want to represent in the sentence
    :return: a list of the (ordered) BILOU tags, one per each token of the sentence

    * BILOU stands for "Beginning, Inside, Last, Outside, Unit-length".
    It is a tag scheme labelling each token with one of these five tags (B, I, L, O, U)
    depending on the membership of the token in a Named Entity. It distinguishes a 'simple' NE,
    made of one single token, and a 'composed' token, made of multiple subsequent tokens.
    • B (Begin)   -> if the token is the beginning of a composed NE
    • I (Inside)  -> if the token belongs to a composed NE, but it is not the initial token neither the last one
    • L (Last)    -> if the token is the last of a composed NE
    • O (Outside) -> if the token does *not* belong to any NE
    • U (Unit-Length) -> if the token represent a simple NE (NE made of one single token)
    """

    # initialize all the tags to "O" (Outside)
    tags = ["O" for _ in range(len(sentence_tokens))]

    # insert the tag related of each match
    for match in matches:
        if match["end"] - match["start"] == 1:
            # Unit-length Named Entity
            tags[match["start"]] = "U"
            continue

        for x in range(match["start"], match["end"]):
            # tag the start token with "B", the last with "L", and the rest with "I"
            tags[x] = "B" if x == match["start"] else "L" if x == match["end"] - 1 else "I"

    return tags


# * rapid test *


def format_tags(tags, sentence):
    sentence_tokens = Tokenizer().tokenize(sentence)
    result = []

    for token, tag in zip(sentence_tokens, tags):
        formatted_tag = tag + (" " * (len(token) - 1))
        result.append(formatted_tag)

    return " ".join(result)


if __name__ == "__main__":
    """
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

    dataset = datasets.load_dataset("conll2003", split="train")
    _NE_list = get_NEs_from_file("../../NEs_output/test10000_w_aliases.csv")
    _sentence_tokens = dataset[0]["tokens"]
    _tokenizer = Tokenizer()

    BIO_tags = brutal_force_NER(_sentence_tokens, _NE_list, _tokenizer, scheme="BIO")

    BIO_formatted_tags = []

    for token, tag in zip(_sentence_tokens, BIO_tags):
        formatted_tag = tag + (" " * (len(token) - 1))
        BIO_formatted_tags.append(formatted_tag)

    _sentence_ = " ".join(_sentence_tokens)
    _tags_ = " ".join(BIO_formatted_tags)
    print(f"{_NE_list}\n\n{_sentence_}\n{_tags_}")
