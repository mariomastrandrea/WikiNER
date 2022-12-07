from src.model.objects.match import Match
from src.model.tagging_schemes.bilou import represent_BILOU_tags
from src.model.tagging_schemes.bio import represent_BIO_tags


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
    # A match is a dict like: { "start": x, "end": y }
    #   - x is the starting index in the sentence's tokens
    #   - y is the (exclusive) ending index in the sentence's tokens (y token is not included in the match)
    # i.e., in the sentence
    # ["I", "attend", "Iowa", "State", "University", ",", "but", "I", "am", "not", "from", "Ames"]
    # a match with the NE "Iowa State University" would be: {"start":2, "end":5}

    # build a helper data structure to improve detection of overlapping NEs
    # for each sentence's token, it contains the belonging match (if exist)
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


def find_matches_of(entity_tokens, sentence_tokens):
    """
    Return a list of matches of the specified NE in the provided sentence
    (an entity can potentially appear multiple times in the same sentence)
    """
    matches = []
    entity_len = len(entity_tokens)

    # loop over the sentence tokens, and search for the entity tokens
    for i in range(len(sentence_tokens) - entity_len + 1):
        if entity_tokens == sentence_tokens[i: i+entity_len]:
            # there is a match !
            new_match = Match(
                start=i,
                end=i+entity_len
            )
            # save the match
            matches.append(new_match)

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
