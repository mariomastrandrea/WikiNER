from nltk.tokenize import word_tokenize


class Tokenizer:
    def tokenize(self, sentence):
        """
        It split a string sentence in a sequence of tokens
        :param sentence: string with the sentence
        :return: list of strings, one for each token
        """
        # todo: improve the tokenization with a tokenizer from a lib
        return word_tokenize(sentence)
