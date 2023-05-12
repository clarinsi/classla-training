# Detailed description of the training process

For Serbian, the data had to first be combined with Croatian data in a special way to ensure sufficient representation of certain labels. The prepared datasets for each annotation layer are contained in conllu/pos, conllu/lemma, and conllu/depparse. The preparation process is described in detail below.

## Tagger

For morphosyntactic tagging the serbian sr_set-ud corpus was combined with the Croatian hr500k dataset and the Serbian data was repeated 5.4 times so that the ratio of Serbian to Croatian is 1:1. The oversampling script is contained in conllu/Oversampling.py.

The tagger was then trained:

```
python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --wordvec_file all-token-sr-prelim.ft.sg.vec.xz --train_file conllu/pos/sr_standard_train.conllu --eval_file conllu/sr_set-ud-dev.conllu --gold_file conllu/sr_set-ud-dev.conllu --mode train --shorthand sr_set --output_file out-temp/pos/baseline_pos.conllu
```

Evaluation:

```
python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --eval_file conllu/sr_set-ud-test_empty.conllu --output_file out/pos/baseline_pos.conllu --gold_file conllu/sr_set-ud-test.conllu --shorthand sr_set --mode predict >> eval_scores/baseline_pos.txt
```

## Lemmatizer

For lemmatization the Serbian standard and non-standard train datasets were merged using the following command:

```
cat reldi-normtagner-sr-train.conllu sr_set-ud-train.conllu > lemma/sr_standard+nonst_train.conllu
```

The resulting dataset was then used to train the lemmatizer:

```
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --train_file conllu/lemma/sr_standard+nonst_train.conllu --eval_file out/sr_set-ud-dev_pos.conllu --output_file out-temp/baseline_pos_lemma.conllu --gold_file conllu/sr_set-ud-dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos --external_dict srLex_v1.3_classla_format.tsv
```

Evaluation:

```
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --eval_file out/pos/baseline_pos.conllu --output_file out/lemma/baseline_pos_lemma.conllu --gold_file conllu/sr_set-ud-test.conllu --mode predict >> eval_scores/baseline_lemma.txt
```

## Parser

For dependency parsing only the Serbian standard train dataset was used to train the model:

```
python -m classla.models.parser --save_dir models/depparse/ --save_name baseline_depparse --wordvec_file all-token-sr-prelim.ft.sg.vec.xz --train_file conllu/sr_set-ud-train.conllu --eval_file out/sr_set-ud-dev_pos_lemma.conllu --gold_file conllu/sr_set-ud-dev.conllu --shorthand sr_set --output_file out-temp\temp_baseline_pos_lemma_depparse.conllu --mode train
```

```
python -m classla.models.parser --save_dir models/depparse/ --save_name baseline_depparse --eval_file out/lemma/baseline_pos_lemma.conllu --gold_file conllu/sr_set-ud-test.conllu --shorthand sr_set --output_file out/depparse/baseline_pos_lemma_depparse.conllu --mode predict >> eval_scores/baseline_depparse.txt
```

## Results:

### morphosyntax:

| model | UPOS | XPOS | UFeats | AllTags |
| --- | --- | --- | --- | --- |
| baseline | 98.94 | 96.19 | 96.41 | 95.79 |

### lemmatization

| model | F1 |
| --- | --- |
| baseline | 98.02 |

### parsing

| model | LAS |
| --- | --- |
| baseline_newlex | 89.83 |