# Detailed description of the non-standard model training procedure

Before being fed to Classla as input, the Janes-tag 3.0 data had to be slightly adjusted. The spaces in the 1:n-type tokens were removed, while the n:1-type tokens were kept as they were. The data preparation code can be found in prepare.py

The models were trained in two phases: the first set of models were trained on Janes-tag 3.0 training data (referred to as baseline), the second set was trained on a combination of Janes-tag 3.0 and SUK training data (with an equal representation of both corpora) (referred to as baseline+SUK)

## Janes-only models

### Tagger

Two models were trained for each task - one with the lexicon and one without:

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-lex --wordvec_file all-token-prelim.ft.sg.vec.xz --train_file conllu/train/janes_ud_train.conllu --eval_file conllu/dev/janes_ud_dev.conllu --gold_file conllu/dev/janes_ud_dev.conllu --mode train --shorthand sl_ssj --output_file out-temp/baseline_pos-lex.conllu --inflectional_lexicon_path sloleks_clarin_3.0_classla_ready.tbl
- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-wolex --wordvec_file all-token-prelim.ft.sg.vec.xz --train_file conllu/train/janes_ud_train.conllu --eval_file conllu/dev/janes_ud_dev.conllu --gold_file conllu/dev/janes_ud_dev.conllu --mode train --shorthand sl_ssj --output_file out-temp/baseline_pos-wolex.conllu

The evaluation was carried out using the following commands:

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-lex --eval_file conllu/dev/janes_ud_dev_empty.conllu --output_file out/pos/baseline_pos-lex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --shorthand sl_ssj --mode predict --use_lexicon foo
- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-wolex --eval_file conllu/dev/janes_ud_dev_empty.conllu --output_file out/pos/baseline_pos-wolex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --shorthand sl_ssj --mode predict

As an additional check, the taggers were also evaluated on the subcorpora test sets:

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-lex --eval_file conllu/dev/janes-rsdo_ud_dev_empty.conllu --output_file out/pos/baseline_pos-lex_janes-rsdo.conllu --gold_file conllu/dev/janes-rsdo_ud_dev.conllu --shorthand sl_ssj --mode predict --use_lexicon foo
- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-wolex --eval_file conllu/dev/janes-rsdo_ud_dev_empty.conllu --output_file out/pos/baseline_pos-wolex_janes-rsdo.conllu --gold_file conllu/dev/janes-rsdo_ud_dev.conllu --shorthand sl_ssj --mode predict

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-lex --eval_file conllu/dev/janes-tag_ud_dev_empty.conllu --output_file out/pos/baseline_pos-lex_janes-tag.conllu --gold_file conllu/dev/janes-tag_ud_dev.conllu --shorthand sl_ssj --mode predict --use_lexicon foo
- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-wolex --eval_file conllu/dev/janes-tag_ud_dev_empty.conllu --output_file out/pos/baseline_pos-wolex_janes-tag.conllu --gold_file conllu/dev/janes-tag_ud_dev.conllu --shorthand sl_ssj --mode predict

### Lemmatizer

Similarly to the tagger, two lemmatizers were trained:

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-lex --train_file conllu/train/janes_ud_train.conllu --eval_file out/pos/baseline_pos-lex.conllu --output_file out-temp/baseline_lemma-lex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos --pos_model_path models/pos/baseline_pos-lex
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-wolex --train_file conllu/train/janes_ud_train.conllu --eval_file out/pos/baseline_pos-wolex.conllu --output_file out-temp/baseline_lemma-wolex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos

The following commands were used for lemmatizer evaluation. They cover four different combinations of lexicon usage: "baseline_lemma-lex_pos-lex" refers to lexicon used during lemma prediction and lexicon-predicted upstream pos annotations, "baseline_lemma-lex_pos-wolex" refers to lexicon used during lemma prediction and upstream pos annotations predicted without lexicon,
"baseline_lemma-wolex_pos-lex" refers to no lexicon used during lemma prediction and lexicon-predicted upstream pos annotations, "baseline_lemma-wolex_pos-wolex" refers to no lexicon used during lemma prediction and upstream pos annotations predicted without lexicon:

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-lex --eval_file out/pos/baseline_pos-lex.conllu --output_file out/lemma/baseline_lemma-lex_pos-lex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --pos_model_path models/pos/baseline_pos-lex --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-lex --eval_file out/pos/baseline_pos-wolex.conllu --output_file out/lemma/baseline_lemma-lex_pos-wolex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --pos_model_path models/pos/baseline_pos-lex --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-wolex --eval_file out/pos/baseline_pos-lex.conllu --output_file out/lemma/baseline_lemma-wolex_pos-lex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-wolex --eval_file out/pos/baseline_pos-wolex.conllu --output_file out/lemma/baseline_lemma-wolex_pos-wolex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --mode predict

## Combined Janes+SUK models

### Tagger

In the next phase, a combined model was trained on both Janes and SUK training data and evaluated on SUK dev data. To reach a 1:1 ratio of both training sets, the Janes-tag 3.0 training data was repeated 4.7 times. The code for oversampling Janes-tag 3.0 is contained in oversampling.py.
The combined training dataset is located at conllu/train/combined_ud_train.conllu. This combined model is henceforth referred to as baseline+suk. The tagger training was carried out as follows:

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline+suk_pos-lex --wordvec_file all-token-prelim.ft.sg.vec.xz --train_file conllu/train/combined_ud_train.conllu --eval_file conllu/dev/combined_ud_dev.conllu --gold_file conllu/dev/combined_ud_dev.conllu --mode train --shorthand sl_ssj --output_file out-temp/baseline+suk_pos-lex.conllu --inflectional_lexicon_path sloleks_clarin_3.0_classla_ready.tbl
- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline+suk_pos-wolex --wordvec_file all-token-prelim.ft.sg.vec.xz --train_file conllu/train/combined_ud_train.conllu --eval_file conllu/dev/combined_ud_dev.conllu --gold_file conllu/dev/combined_ud_dev.conllu --mode train --shorthand sl_ssj --output_file out-temp/baseline+suk_pos-wolex.conllu

Evaluation was carried out on both the janes dev set and SUK dev set:

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline+suk_pos-lex --eval_file conllu/dev/janes_ud_dev_empty.conllu --output_file out/pos/baseline+suk_pos-lex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --shorthand sl_ssj --mode predict --use_lexicon foo
- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline+suk_pos-wolex --eval_file conllu/dev/janes_ud_dev_empty.conllu --output_file out/pos/baseline+suk_pos-wolex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --shorthand sl_ssj --mode predict

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline+suk_pos-lex --eval_file conllu/dev/SUK_ud_dev_empty.conllu --output_file out/pos/SUK_dev_eval/suk-dev-eval-baseline+suk_pos-lex.conllu --gold_file conllu/dev/SUK_ud_dev.conllu --shorthand sl_ssj --mode predict --use_lexicon foo
- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline+suk_pos-wolex --eval_file conllu/dev/SUK_ud_dev_empty.conllu --output_file out/pos/SUK_dev_eval/suk-dev-eval-baseline+suk_pos-wolex.conllu --gold_file conllu/dev/SUK_ud_dev.conllu --shorthand sl_ssj --mode predict







results should include:

tagger:
--------

baseline_pos-lex
baseline_pos-wolex

baseline+suk_pos-lex
baseline+suk_pos-wolex


lemmatizer:
--------

baseline_lemma-lex_pos-lex
baseline_lemma-lex_pos-wolex
baseline_lemma-wolex_pos-lex
baseline_lemma-wolex_pos-wolex

baseline+suk_lemma-lex_pos-lex
baseline+suk_lemma-lex_pos-wolex
baseline+suk_lemma-wolex_pos-lex
baseline+suk_lemma-wolex_pos-wolex
