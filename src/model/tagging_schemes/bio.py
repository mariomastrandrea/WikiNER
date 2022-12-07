

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
