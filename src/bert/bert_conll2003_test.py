from transformers import BertTokenizerFast, AutoModelForTokenClassification, Trainer, TrainingArguments
from src.test.conll2003_test import get_huggingface_dataset


def adjust_bert_labels(word_ids, ner_tags):
    special_tag = -100

    current_id = None

    for i, word_id in enumerate(word_ids):
        if word_id is None:
            ner_tags.insert(i, special_tag)
            continue

        # word_id is an index
        if word_id != current_id:
            current_id = word_id
        else:
            # add a special tag
            ner_tags.insert(i, special_tag)

    return ner_tags


def encode_row_and_adjust_tags(row, tokenizer):
    # create new row from the tokens, encoding them in bert integers ids
    new_row = tokenizer(
        row["tokens"],
        padding="max_length",
        truncation=True,
        is_split_into_words=True
    )

    # adjust labels according to BERT model
    # add the labels attribute and adjust the existing tags/labels
    new_row["labels"] = adjust_bert_labels(new_row.word_ids(), row["ner_tags"])

    return new_row


def encode_dataset(dataset, tokenizer):
    # encode the dataset sentences
    dataset = dataset.map(lambda row: encode_row_and_adjust_tags(row, tokenizer))
    return dataset


if __name__ == "__main__":
    # create the BERT tokenizer
    bert_tokenizer = BertTokenizerFast.from_pretrained("bert-base-cased")

    # retrieve the conll2003 dataset (training + test)
    train_set_conll2003 = get_huggingface_dataset("conll2003", split="train")
    test_set_conll2003 = get_huggingface_dataset("conll2003", split="test")

    # encode training set and test set for the BERT model
    bert_encoded_train_set = encode_dataset(train_set_conll2003, bert_tokenizer)
    bert_encoded_test_set  = encode_dataset(test_set_conll2003, bert_tokenizer)

    # create BERT model for token classification tasks
    bert_model = AutoModelForTokenClassification.from_pretrained("bert-base-cased", num_labels=10)

    # specify training arguments to pass to the trainer
    training_args = TrainingArguments(
        output_dir="bert-conll2003-test-output",
        evaluation_strategy="epoch",
        weight_decay=0.01,
        num_train_epochs=3,
        learning_rate=5e-5
    )

    # create the model trainer object
    trainer = Trainer(
        model=bert_model,
        train_dataset=bert_encoded_train_set,
        eval_dataset=bert_encoded_test_set,
        args=training_args,
        tokenizer=bert_tokenizer
    )

    # launch training phase
    trainer.train()



