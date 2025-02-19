# Detailed description of the training process

The spoken slovenian model was trained on a combination of spoken (the SST-UD corpus v2.16(pre-release, taken from the dev branch on Jan 10 2025)) and written data (SUK v1.1). Different levels of oversampling had to be performed for different levels, as UD dependency parsing has less data available in SUK than morphosyntactic tagging and lemmatization. For morphosyntactic tagging and lemmatization, 11 repetitions of the spoken training data were first combined with one instance of SUK training data. In order to checke whether there is any overfitting of the spoken data, an additional combination with 6 repetitions of spoken data and one instance of SUK was also tested. For dependency parsing, only 3 repetitions of spoken data were combined with one instance of the part of SUK that contains dependency parsing annotations. The same training splits for SUK were taken as in the previous training of Slovenian standard models (SUK v1.0), while the original SST-UD splits were preserved.

## Tagger

The tagger was trained on 11 repetitions of the spoken training data and one instance of SUK 1.1 data using the following command:

- python -m classla.models.tagger --save_dir models/pos/ --save_name pos --wordvec_file ../all-token-prelim.ft.sg.vec.xz --train_file conllu/train/combined_train_sst11.conllu --eval_file conllu/dev/sl_sst-ud-dev_empty.conllu --gold_file conllu/dev/sl_sst-ud-dev.conllu --mode train --shorthand sl_sst --output_file out-temp/sl_sst-ud-dev.pos.conllu --inflectional_lexicon_path ../sloleks_clarin_3.0_classla_ready.tbl

Evaluation was carried out on both the SST and SUK test sets:

- python -m classla.models.tagger --save_dir models/pos/ --save_name pos --eval_file conllu/test/sl_sst-ud-test_empty.conllu --output_file out/sl_sst-ud-test.pos.conllu --gold_file conllu/test/sl_sst-ud-test.conllu --shorthand sl_sst --mode predict > eval_scores/pos_on_sst.txt

- python -m classla.models.tagger --save_dir models/pos/ --save_name pos --eval_file conllu/test/suk_1.1_test_empty.conllu --output_file out/suk_1.1_test.pos.conllu --gold_file conllu/test/suk_1.1_test.conllu --shorthand sl_sst --mode predict > eval_scores/pos_on_suk.txt

Afterwards, to test for overfitting, another tagger was trained on 6 repetitions of the spoken training data and a proportional amount of SUK 1.1 training data using the following command:

- python -m classla.models.tagger --save_dir models/pos/ --save_name pos_sst6 --wordvec_file ../all-token-prelim.ft.sg.vec.xz --train_file conllu/train/combined_train_sst6.conllu --eval_file conllu/dev/sl_sst-ud-dev_empty.conllu --gold_file conllu/dev/sl_sst-ud-dev.conllu --mode train --shorthand sl_sst --output_file out-temp/sl_sst-ud-dev_sst6.pos.conllu --inflectional_lexicon_path ../sloleks_clarin_3.0_classla_ready.tbl

Evaluation:

- python -m classla.models.tagger --save_dir models/pos/ --save_name pos_sst6 --eval_file conllu/test/sl_sst-ud-test_empty.conllu --output_file out/sl_sst-ud-test_sst6.pos.conllu --gold_file conllu/test/sl_sst-ud-test.conllu --shorthand sl_sst --mode predict > eval_scores/pos_sst6_on_sst.txt

- python -m classla.models.tagger --save_dir models/pos/ --save_name pos_sst6 --eval_file conllu/test/suk_1.1_test_empty.conllu --output_file out/suk_1.1_test_sst6.pos.conllu --gold_file conllu/test/suk_1.1_test.conllu --shorthand sl_sst --mode predict > eval_scores/pos_sst6_on_suk.txt

Overfitting did not occur, so the model trained on 11 repetitions was chosen as the one to be published.

## Lemmatizer

The lemmatizer was also trained on the 11-times oversampled training data file:

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file lemma --train_file conllu/train/combined_train_sst11.conllu --eval_file out/sl_sst-ud-dev.pos.conllu --output_file out-temp/sl_sst-ud-dev.pos.lemma.conllu --gold_file conllu/dev/sl_sst-ud-dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos --pos_model_path models/pos/pos

evaluation was carried out on both the SST and SUK test sets:

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file lemma --eval_file out/sl_sst-ud-test.pos.conllu --output_file out/sl_sst-ud-test.pos.lemma.conllu --gold_file conllu/test/sl_sst-ud-test.conllu --pos_model_path models/pos/pos --mode predict > eval_scores/lemma_on_sst.txt

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file lemma --eval_file out/suk_1.1_test.pos.conllu --output_file out/suk_1.1_test.pos.lemma.conllu --gold_file conllu/test/suk_1.1_test.conllu --pos_model_path models/pos/pos --mode predict > eval_scores/lemma_on_suk.txt

## Parser

Due to a different amount of available training data, the parser was trained on 3 repetitions of the spoken training data and one instance of SUK 1.1 data using the following command:

- python -m classla.models.parser --save_dir models/depparse/ --save_name depparse --wordvec_file ../all-token-prelim.ft.sg.vec.xz --train_file conllu/train/combined_train_syn_sst3.conllu --eval_file out/sl_sst-ud-dev.pos.lemma.conllu --gold_file conllu/dev/sl_sst-ud-dev.conllu --shorthand sl_sst --output_file out-temp\sl_sst-ud-dev.pos.lemma.depparse.conllu --mode train

evaluation was carried out on both the SST and SUK test sets:

- python -m classla.models.parser --save_dir models/depparse/ --save_name depparse --eval_file out/sl_sst-ud-test.pos.lemma.conllu --gold_file conllu/test/sl_sst-ud-test.conllu --shorthand sl_sst --output_file out/sl_sst-ud-test.pos.lemma.depparse.conllu --mode predict > eval_scores/depparse_on_sst.txt

- python -m classla.models.parser --save_dir models/depparse/ --save_name depparse --eval_file out/suk_1.1_syn_test.pos.lemma.conllu --gold_file conllu/test/suk_1.1_syn_test.conllu --shorthand sl_sst --output_file out/suk_1.1_syn_test.pos.lemma.depparse.conllu --mode predict > eval_scores/depparse_on_suk.txt

## Results

### Morphosyntactic tagging

sst11:

| test set | UPOS | XPOS | UFeats | AllTags |
| --- | --- | --- | --- | --- |
| SST | 98.15 | 96.76 | 96.59 | 95.60 |
| SUK | 98.66 | 96.65 | 96.80 | 95.84 |

sst6:

| test set | UPOS | XPOS | UFeats | AllTags |
| --- | --- | --- | --- | --- |
| SST | 98.01 | 96.38 | 96.36 | 95.26 |
| SUK | 98.50 | 96.44 | 96.55 | 95.59 |

### Lemmatization

| test set | F1 |
| --- | --- |
| SST | 99.23 |
| SUK | 98.80 |

### Syntactic parsing

| test set | LAS |
| --- | --- |
| SST | 81.91 |
| SUK | 90.09 |
