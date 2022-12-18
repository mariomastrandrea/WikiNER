from transformers import AutoTokenizer, AutoModelForTokenClassification, Trainer, TrainingArguments, \
    DataCollatorForTokenClassification
from src.test.conll2003_test import get_huggingface_dataset
import numpy as np
import evaluate



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


def compute_metrics(eval_prediction, metric, label_names):
    logits, labels = eval_prediction
    predictions = np.argmax(logits, axis=2)

    true_labels = [[label_names[l] for l in label if l != -100] for label in labels]
    true_predictions = [
        [label_names[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    all_metrics = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": all_metrics["overall_precision"],
        "recall": all_metrics["overall_recall"],
        "f1": all_metrics["overall_f1"],
        "accuracy": all_metrics["overall_accuracy"],
}


if __name__ == "__main__":
    # create the BERT tokenizer
    bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

    # retrieve the conll2003 dataset (training + test)
    train_set_conll2003 = get_huggingface_dataset("conll2003", split="train")
    eval_set_conll2003 = get_huggingface_dataset("conll2003", split="validation")

    # encode training set and test set for the BERT model
    bert_encoded_train_set = encode_dataset(train_set_conll2003, bert_tokenizer)
    bert_encoded_eval_set  = encode_dataset(eval_set_conll2003, bert_tokenizer)

    # create BERT model for token classification tasks
    bert_model = AutoModelForTokenClassification.from_pretrained("bert-base-cased", num_labels=9)

    # specify training arguments to pass to the trainer
    training_args = TrainingArguments(
        output_dir="bert-conll2003-test-output",
        evaluation_strategy="epoch",
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        learning_rate=2e-5,
        weight_decay=0.01
    )

    metric = evaluate.load('seqeval')
    label_names = train_set_conll2003.features['ner_tags'].feature.names

    # create the model trainer object
    trainer = Trainer(
        model=bert_model,
        args=training_args,
        train_dataset=bert_encoded_train_set,
        eval_dataset=bert_encoded_eval_set,
        data_collator=DataCollatorForTokenClassification(tokenizer=bert_tokenizer),
        compute_metrics=lambda eval_prediction: compute_metrics(eval_prediction, metric, label_names),
        tokenizer=bert_tokenizer
    )

    # launch training phase
    trainer.train()

