# Detailed description of the training process

Before training the models, the train and dev subsets of the standard (hr500k) and nonstandard (reldi-normtagner-hr) datasets were merged into a combined set and 20% of the diacritics were removed. Similarly to the Slovene nonstandard models, the ratio of standard data to non-standard data was to be 1:1, so the non-standard data had to be repeated 5.5 times. The python script for this process is Oversampling+less_diacritics.py. This time around, diacritics were removed from two whole repetitions of the nonstandard data.

## Tagger

The tagger training was carried out using the following command:

```
python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --wordvec_file all-token-hr-prelim.ft.sg.vec.xz --train_file conllu/hr_combined_train.conllu --eval_file conllu/hr_combined_dev.conllu --gold_file conllu/hr_combined_dev.conllu --mode train --shorthand hr_set --output_file out-temp/pos/baseline_pos.conllu
```

Evaluation was performed on the non-standard dev set and the standard dev set:

```
python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --eval_file conllu/hr500k-dev_empty.conllu --output_file out/pos/baseline_pos_st-dev.conllu --gold_file conllu/hr500k-dev.conllu --shorthand hr_set --mode predict >> eval_scores/baseline_pos_st-dev.txt

python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --eval_file conllu/reldi-normtagner-hr-dev_empty.conllu --output_file out/pos/baseline_pos_nonst-dev.conllu --gold_file conllu/reldi-normtagner-hr-dev.conllu --shorthand hr_set --mode predict >> eval_scores/baseline_pos_nonst-dev.txt
```

## Lemmatizer

The lemmatizer was trained using the hrLex inflectional lexicon:

```
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --train_file conllu/hr_combined_train.conllu --eval_file out/hr_combined_dev_pos.conllu --output_file out-temp/baseline_pos_lemma.conllu --gold_file conllu/hr_combined_dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos --external_dict hrLex_v1.3_classla_format
```

Evaluation:

```
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --eval_file out/pos/baseline_pos_st-dev.conllu --output_file out/lemma/baseline_pos_lemma_st-dev.conllu --gold_file conllu/hr500k-dev.conllu --mode predict >> eval_scores/baseline_lemma_st-dev.txt

python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --eval_file out/pos/baseline_pos_nonst-dev.conllu --output_file out/lemma/baseline_pos_lemma_nonst-dev.conllu --gold_file conllu/reldi-normtagner-hr-dev.conllu --mode predict >> eval_scores/baseline_lemma_nonst-dev.txt
```

## Results

The evaluation results are listed below. The models were evaluated on the standard and non-standard dev sets:

| model | dev set | AllTags/F1 |
| --- | --- | --- |
| tagger | hr500k | 94.09 |
| lemmatizer | hr500k | 97.59 |
| tagger | reldi-normtagner-hr | 91.96 |
| lemmatizer | reldi-normtagner-hr | 94.23 |

At the end, after everything was finallized, the non-standard models were evaluated on the test set as well:

```
python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --eval_file conllu/hr500k-test_empty.conllu --output_file out/pos/baseline_pos_st-test.conllu --gold_file conllu/hr500k-test.conllu --shorthand hr_set --mode predict >> eval_scores/baseline_pos_st-test.txt

python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --eval_file conllu/reldi-normtagner-hr-test_empty.conllu --output_file out/pos/baseline_pos_nonst-test.conllu --gold_file conllu/reldi-normtagner-hr-test.conllu --shorthand hr_set --mode predict >> eval_scores/baseline_pos_nonst-test.txt

python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --eval_file out/pos/baseline_pos_st-test.conllu --output_file out/lemma/baseline_pos_lemma_st-test.conllu --gold_file conllu/hr500k-test.conllu --mode predict >> eval_scores/baseline_lemma_st-test.txt

python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --eval_file out/pos/baseline_pos_nonst-test.conllu --output_file out/lemma/baseline_pos_lemma_nonst-test.conllu --gold_file conllu/reldi-normtagner-hr-test.conllu --mode predict >> eval_scores/baseline_lemma_nonst-test.txt
```

The final evaluation results on the test set are shown below:

| model | test set | AllTags/F1 |
| --- | --- | --- |
| tagger | hr500k | 94.03 |
| lemmatizer | hr500k | 97.68 |
| tagger | reldi-normtagner-hr | 91.09 |
| lemmatizer | reldi-normtagner-hr | 93.61 |