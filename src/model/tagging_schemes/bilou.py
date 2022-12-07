

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
