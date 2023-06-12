# Detailed description of the training process

Before training the non-standard tagger, the train dataset for the morphosyntactic tagger was constructed using standard data and non-standard data in a 1:1 ratio. The standard Serbian train dataset was first expanded with a similar amount of data from the Croatian standard train dataset (but only from the part that does not originate from SETimes - in accordance with this, about 22 % of the non-SETimes Croatian data was required). Afterwards this combined standard data was merged with two repetitions of the non-standard Serbian train data (one of which had its diacritics removed), so as to reach the 1:1 ratio of standard to non-standard.

## Tagger

The script for constructing the non-standard train set for morphosyntactic tagging is at conllu/make_tagger_train_set.py. The resulting train dataset is sr-nonst_tagger_train.conllu. 

Tagger training:

```
python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --wordvec_file all-token-sr-prelim.ft.sg.vec.xz --train_file conllu/pos/sr-nonst_tagger_train.conllu --eval_file conllu/reldi-normtagner-sr-dev.conllu --gold_file conllu/reldi-normtagner-sr-dev.conllu --mode train --shorthand sr_set --output_file out-temp/pos/baseline_pos.conllu
```

The evaluation was performed on the standard and non-standard dev sets:

```
python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --eval_file conllu/sr_set-ud-dev_empty.conllu --output_file out/pos/baseline_pos_st-dev.conllu --gold_file conllu/sr_set-ud-dev.conllu --shorthand sr_set --mode predict >> eval_scores/baseline_pos_st-dev.txt

python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --eval_file conllu/reldi-normtagner-sr-dev_empty.conllu --output_file out/pos/baseline_pos_nonst-dev.conllu --gold_file conllu/reldi-normtagner-sr-dev.conllu --shorthand sr_set --mode predict >> eval_scores/baseline_pos_nonst-dev.txt
```

## Lemmatizer

The lemmatizer was trained on the Serbian standard dataset and non-standard dataset merged into one train dataset. The following command was used: 


```
cat conllu/sr_set-ud-train.conllu conllu/reldi-normtagner-sr-train.conllu > conllu/lemma/sr_nonst_train.conllu
```

As with the Serbian standard lemmatizer, the srLex lexicon was used during training as an external lexicon:

```
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --train_file conllu/lemma/sr_nonst_train.conllu --eval_file out/pos/baseline_pos_nonst-dev.conllu --output_file out-temp/baseline_pos_lemma.conllu --gold_file conllu/reldi-normtagner-sr-dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos --external_dict srLex_v1.3_classla_format.tsv
```

Evaluation:

```
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --eval_file out/pos/baseline_pos_st-dev.conllu --output_file out/lemma/baseline_pos_lemma_st-dev.conllu --gold_file conllu/sr_set-ud-dev.conllu --mode predict >> eval_scores/baseline_lemma_st-dev.txt

python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --eval_file out/pos/baseline_pos_nonst-dev.conllu --output_file out/lemma/baseline_pos_lemma_nonst-dev.conllu --gold_file conllu/reldi-normtagner-sr-dev.conllu --mode predict >> eval_scores/baseline_lemma_nonst-dev.txt
```

## Results

The evaluation results are listed below. The models were evaluated on the standard and non-standard dev sets:

| model | dev set | AllTags/F1 |
| --- | --- | --- |
| tagger | sr-set_ud | 94.52 |
| lemmatizer | sr-set_ud | 97.71 |
| tagger | reldi-normtagner-sr | 92.11 |
| lemmatizer | reldi-normtagner-sr | 94.92 |

At the end, after everything was finallized, the non-standard models were evaluated on the test set as well:

```
python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --eval_file conllu/sr_set-ud-test_empty.conllu --output_file out/pos/baseline_pos_st-test.conllu --gold_file conllu/sr_set-ud-test.conllu --shorthand sr_set --mode predict >> eval_scores/baseline_pos_st-test.txt

python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --eval_file conllu/reldi-normtagner-sr-test_empty.conllu --output_file out/pos/baseline_pos_nonst-test.conllu --gold_file conllu/reldi-normtagner-sr-test.conllu --shorthand sr_set --mode predict >> eval_scores/baseline_pos_nonst-test.txt

python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --eval_file out/pos/baseline_pos_st-test.conllu --output_file out/lemma/baseline_pos_lemma_st-test.conllu --gold_file conllu/sr_set-ud-test.conllu --mode predict >> eval_scores/baseline_lemma_st-test.txt

python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --eval_file out/pos/baseline_pos_nonst-test.conllu --output_file out/lemma/baseline_pos_lemma_nonst-test.conllu --gold_file conllu/reldi-normtagner-sr-test.conllu --mode predict >> eval_scores/baseline_lemma_nonst-test.txt
```

The final evaluation results on the test set are shown below:

| model | test set | AllTags/F1 |
| --- | --- | --- |
| tagger | sr-set_ud | 95.32 |
| lemmatizer | sr-set_ud | 98.02 |
| tagger | reldi-normtagner-sr | 92.56 |
| lemmatizer | reldi-normtagner-sr | 94.92 |