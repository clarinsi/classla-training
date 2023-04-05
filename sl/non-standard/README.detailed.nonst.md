# Detailed description of the non-standard model training procedure

Before being fed to Classla as input, the Janes-tag 3.0 data had to be slightly adjusted. The spaces in the n:1-type tokens were removed, while the 1:n-type tokens were kept as they were. The data preparation code can be found in prepare.py

The models were trained in two phases: the first set of models were trained on Janes-tag 3.0 training data (referred to as baseline), the second set was trained on a combination of Janes-tag 3.0 and SUK training data (with an equal representation of both corpora) (referred to as baseline+SUK)

## Janes-only models

### Tagger

Two models were trained for each task - one with the lexicon and one without:

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-lex --wordvec_file all-token-prelim.ft.sg.vec.xz --train_file conllu/train/janes_ud_train.conllu --eval_file conllu/dev/janes_ud_dev.conllu --gold_file conllu/dev/janes_ud_dev.conllu --mode train --shorthand sl_ssj --output_file out-temp/baseline_pos-lex.conllu --inflectional_lexicon_path sloleks_clarin_3.0_classla_ready.tbl
- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-wolex --wordvec_file all-token-prelim.ft.sg.vec.xz --train_file conllu/train/janes_ud_train.conllu --eval_file conllu/dev/janes_ud_dev.conllu --gold_file conllu/dev/janes_ud_dev.conllu --mode train --shorthand sl_ssj --output_file out-temp/baseline_pos-wolex.conllu

The evaluation was carried out on both the janes dev set and SUK dev set:

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-lex --eval_file conllu/dev/janes_ud_dev_empty.conllu --output_file out/pos/baseline_pos-lex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --shorthand sl_ssj --mode predict --use_lexicon foo
- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-wolex --eval_file conllu/dev/janes_ud_dev_empty.conllu --output_file out/pos/baseline_pos-wolex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --shorthand sl_ssj --mode predict

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-lex --eval_file conllu/dev/SUK_ud_dev_empty.conllu --output_file out/pos/SUK_dev_eval/suk-dev-eval-baseline_pos-lex.conllu --gold_file conllu/dev/SUK_ud_dev.conllu --shorthand sl_ssj --mode predict --use_lexicon foo
- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-wolex --eval_file conllu/dev/SUK_ud_dev_empty.conllu --output_file out/pos/SUK_dev_eval/suk-dev-eval-baseline_pos-wolex.conllu --gold_file conllu/dev/SUK_ud_dev.conllu --shorthand sl_ssj --mode predict

As an additional check, the taggers were also evaluated on the janes subcorpora test sets:

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-lex --eval_file conllu/dev/janes-rsdo_ud_dev_empty.conllu --output_file out/pos/baseline_pos-lex_janes-rsdo.conllu --gold_file conllu/dev/janes-rsdo_ud_dev.conllu --shorthand sl_ssj --mode predict --use_lexicon foo
- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-wolex --eval_file conllu/dev/janes-rsdo_ud_dev_empty.conllu --output_file out/pos/baseline_pos-wolex_janes-rsdo.conllu --gold_file conllu/dev/janes-rsdo_ud_dev.conllu --shorthand sl_ssj --mode predict

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-lex --eval_file conllu/dev/janes-tag_ud_dev_empty.conllu --output_file out/pos/baseline_pos-lex_janes-tag.conllu --gold_file conllu/dev/janes-tag_ud_dev.conllu --shorthand sl_ssj --mode predict --use_lexicon foo
- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos-wolex --eval_file conllu/dev/janes-tag_ud_dev_empty.conllu --output_file out/pos/baseline_pos-wolex_janes-tag.conllu --gold_file conllu/dev/janes-tag_ud_dev.conllu --shorthand sl_ssj --mode predict

### Lemmatizer

Similarly to the tagger, two lemmatizers were trained:

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-lex --train_file conllu/train/janes_ud_train.conllu --eval_file out/pos/baseline_pos-lex.conllu --output_file out-temp/baseline_lemma-lex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos --pos_model_path models/pos/baseline_pos-lex
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-wolex --train_file conllu/train/janes_ud_train.conllu --eval_file out/pos/baseline_pos-wolex.conllu --output_file out-temp/baseline_lemma-wolex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos

The following commands were used for lemmatizer evaluation. They cover four different combinations of lexicon usage: "baseline_lemma-lex_pos-lex" refers to lexicon used during lemma prediction and lexicon-predicted upstream pos annotations, "baseline_lemma-lex_pos-wolex" refers to lexicon used during lemma prediction and upstream pos annotations predicted without lexicon,
"baseline_lemma-wolex_pos-lex" refers to no lexicon used during lemma prediction and lexicon-predicted upstream pos annotations, "baseline_lemma-wolex_pos-wolex" refers to no lexicon used during lemma prediction and upstream pos annotations predicted without lexicon. The lemmatizer evaluation was carried out on both the janes dev set and SUK dev set:

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-lex --eval_file out/pos/baseline_pos-lex.conllu --output_file out/lemma/baseline_lemma-lex_pos-lex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --pos_model_path models/pos/baseline_pos-lex --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-lex --eval_file out/pos/baseline_pos-wolex.conllu --output_file out/lemma/baseline_lemma-lex_pos-wolex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --pos_model_path models/pos/baseline_pos-lex --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-wolex --eval_file out/pos/baseline_pos-lex.conllu --output_file out/lemma/baseline_lemma-wolex_pos-lex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-wolex --eval_file out/pos/baseline_pos-wolex.conllu --output_file out/lemma/baseline_lemma-wolex_pos-wolex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --mode predict

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-lex --eval_file out/pos/SUK_dev_eval/suk-dev-eval-baseline_pos-lex.conllu --output_file out/lemma/SUK_dev_eval/suk-dev-eval-baseline_lemma-lex_pos-lex.conllu --gold_file conllu/dev/SUK_ud_dev.conllu --pos_model_path models/pos/baseline_pos-lex --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-lex --eval_file out/pos/SUK_dev_eval/suk-dev-eval-baseline_pos-wolex.conllu --output_file out/lemma/SUK_dev_eval/suk-dev-eval-baseline_lemma-lex_pos-wolex.conllu --gold_file conllu/dev/SUK_ud_dev.conllu --pos_model_path models/pos/baseline_pos-lex --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-wolex --eval_file out/pos/SUK_dev_eval/suk-dev-eval-baseline_pos-lex.conllu --output_file out/lemma/SUK_dev_eval/suk-dev-eval-baseline_lemma-wolex_pos-lex.conllu --gold_file conllu/dev/SUK_ud_dev.conllu --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma-wolex --eval_file out/pos/SUK_dev_eval/suk-dev-eval-baseline_pos-wolex.conllu --output_file out/lemma/SUK_dev_eval/suk-dev-eval-baseline_lemma-wolex_pos-wolex.conllu --gold_file conllu/dev/SUK_ud_dev.conllu --mode predict



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

### Lemmatizer

the lemmatizer training was carried out as follows:

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline+suk_lemma-lex --train_file conllu/train/combined_ud_train.conllu --eval_file out/pos/combined_dev_pos-lex_predict.conllu --output_file out-temp/baseline+suk_lemma-lex.conllu --gold_file conllu/dev/combined_ud_dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos --pos_model_path models/pos/baseline+suk_pos-lex
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline+suk_lemma-wolex --train_file conllu/train/combined_ud_train.conllu --eval_file out/pos/combined_dev_pos-wolex_predict.conllu --output_file out-temp/baseline+suk_lemma-wolex.conllu --gold_file conllu/dev/combined_ud_dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos

Lemmatizer evaluation was carried out on both the janes dev set and SUK dev set:

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline+suk_lemma-lex --eval_file out/pos/baseline+suk_pos-lex.conllu --output_file out/lemma/baseline+suk_lemma-lex_pos-lex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --pos_model_path models/pos/baseline+suk_pos-lex --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline+suk_lemma-lex --eval_file out/pos/baseline+suk_pos-wolex.conllu --output_file out/lemma/baseline+suk_lemma-lex_pos-wolex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --pos_model_path models/pos/baseline+suk_pos-lex --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline+suk_lemma-wolex --eval_file out/pos/baseline+suk_pos-lex.conllu --output_file out/lemma/baseline+suk_lemma-wolex_pos-lex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline+suk_lemma-wolex --eval_file out/pos/baseline+suk_pos-wolex.conllu --output_file out/lemma/baseline+suk_lemma-wolex_pos-wolex.conllu --gold_file conllu/dev/janes_ud_dev.conllu --mode predict

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline+suk_lemma-lex --eval_file out/pos/SUK_dev_eval/suk-dev-eval-baseline+suk_pos-lex.conllu --output_file out/lemma/SUK_dev_eval/suk-dev-eval-baseline+suk_lemma-lex_pos-lex.conllu --gold_file conllu/dev/SUK_ud_dev.conllu --pos_model_path models/pos/baseline+suk_pos-lex --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline+suk_lemma-lex --eval_file out/pos/SUK_dev_eval/suk-dev-eval-baseline+suk_pos-wolex.conllu --output_file out/lemma/SUK_dev_eval/suk-dev-eval-baseline+suk_lemma-lex_pos-wolex.conllu --gold_file conllu/dev/SUK_ud_dev.conllu --pos_model_path models/pos/baseline+suk_pos-lex --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline+suk_lemma-wolex --eval_file out/pos/SUK_dev_eval/suk-dev-eval-baseline+suk_pos-lex.conllu --output_file out/lemma/SUK_dev_eval/suk-dev-eval-baseline+suk_lemma-wolex_pos-lex.conllu --gold_file conllu/dev/SUK_ud_dev.conllu --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline+suk_lemma-wolex --eval_file out/pos/SUK_dev_eval/suk-dev-eval-baseline+suk_pos-wolex.conllu --output_file out/lemma/SUK_dev_eval/suk-dev-eval-baseline+suk_lemma-wolex_pos-wolex.conllu --gold_file conllu/dev/SUK_ud_dev.conllu --mode predict



# Results

## Experimenting with diacritics

The janes dev set was then stripped of diacritics and evaluated using the baseline+suk model (using the lexicon on all levels). The conversion was between the following characters: 
["č", "š", "ž", "ć", "ś", "ź", "đ", "Č", "Š", "Ž", "Ć", "Ś", "Ź", "Đ"]  --------> ["c", "s", "z", "dj", "C", "S", "Z", "Dj"]. The conversion script and resulting file is in conllu/dev/no_diacritics/.

evaluation:

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline+suk_pos-lex --eval_file conllu/dev/no_diacritics/janes_ud_dev_dediacritized_empty.conllu --output_file out/pos/no_diacritics/baseline+suk_pos-lex_dediacritized.conllu --gold_file conllu/dev/no_diacritics/janes_ud_dev_dediacritized.conllu --shorthand sl_ssj --mode predict --use_lexicon foo

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline+suk_lemma-lex --eval_file out/pos/no_diacritics/baseline+suk_pos-lex_dediacritized.conllu --output_file out/lemma/no_diacritics/baseline+suk_lemma-lex_pos-lex_dediacritized.conllu --gold_file conllu/dev/no_diacritics/janes_ud_dev_dediacritized.conllu --pos_model_path models/pos/baseline+suk_pos-lex --mode predict

results for the baseline+suk model on janes dev with and without diacritics and SUK:


| model | dev set | AllTags/F1 |
| --- | --- | --- |
| tagger | janes | 91.17 |
| lemmatizer | janes | 91.24 |
| tagger | janes no diacritics | 89.91 |
| lemmatizer | janes no diacritics | 89.27 |
| tagger | SUK | 96.42 |
| lemmatizer | SUK | 98.78 |

The results are significantly lower, so a new set of models was trained on a train set in which one janes repetition (out of the 4.7 in the combined set) has no diacritics and another repetition has a 50% chance of diacritic drop. The script for compiling the dediacritized train set is contained in Oversampling+less_diacritics.py. The models were trained with maximum lexicon usage.

Training was carried out in the following way:

### Tagger

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline+suk+dediacritized --wordvec_file all-token-prelim.ft.sg.vec.xz --train_file conllu/train/combined+dediacritized_ud_train.conllu --eval_file conllu/dev/combined_ud_dev.conllu --gold_file conllu/dev/combined_ud_dev.conllu --mode train --shorthand sl_ssj --output_file out-temp/baseline+suk+dediacritized_pos.conllu --inflectional_lexicon_path sloleks_clarin_3.0_classla_ready.tbl

### Lemmatizer

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline+suk+dediacritized --train_file conllu/train/combined+dediacritized_ud_train.conllu --eval_file out/pos/combined+suk+dediacritized_pos_predictions.conllu --output_file out-temp/baseline+suk_lemma-lex.conllu --gold_file conllu/dev/combined_ud_dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos --pos_model_path models/pos/baseline+suk_pos-lex

### Evaluation 

commands used:

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline+suk+dediacritized --eval_file conllu/dev/janes_ud_dev_empty.conllu --output_file out/pos/dediacritized_model/baseline+suk+dediacritized_janes-dia_pos.conllu --gold_file conllu/dev/janes_ud_dev.conllu --shorthand sl_ssj --mode predict --use_lexicon foo
- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline+suk+dediacritized --eval_file conllu/dev/no_diacritics/janes_ud_dev_dediacritized_empty.conllu --output_file out/pos/dediacritized_model/baseline+suk+dediacritized_janes-no-dia_pos.conllu --gold_file conllu/dev/no_diacritics/janes_ud_dev_dediacritized.conllu --shorthand sl_ssj --mode predict --use_lexicon foo
- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline+suk+dediacritized --eval_file conllu/dev/SUK_ud_dev_empty.conllu --output_file out/pos/dediacritized_model/baseline+suk+dediacritized_SUK_pos.conllu --gold_file conllu/dev/SUK_ud_dev.conllu --shorthand sl_ssj --mode predict --use_lexicon foo

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline+suk+dediacritized --eval_file out/pos/dediacritized_model/baseline+suk+dediacritized_janes-dia_pos.conllu --output_file out/lemma/dediacritized_model/baseline+suk+dediacritized_janes-dia_lemma.conllu --gold_file conllu/dev/janes_ud_dev.conllu --pos_model_path models/pos/baseline+suk+dediacritized --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline+suk+dediacritized --eval_file out/pos/dediacritized_model/baseline+suk+dediacritized_janes-no-dia_pos.conllu --output_file out/lemma/dediacritized_model/baseline+suk+dediacritized_janes-no-dia_lemma.conllu --gold_file conllu/dev/no_diacritics/janes_ud_dev_dediacritized.conllu --pos_model_path models/pos/baseline+suk+dediacritized --mode predict
- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline+suk+dediacritized --eval_file out/pos/dediacritized_model/baseline+suk+dediacritized_SUK_pos.conllu --output_file out/lemma/dediacritized_model/baseline+suk+dediacritized_SUK_lemma.conllu --gold_file conllu/dev/SUK_ud_dev.conllu --pos_model_path models/pos/baseline+suk+dediacritized --mode predict

Eval results for the baseline+suk+dediacritized model on janes dev with and without diacritics and SUK:

| model | dev set | AllTags/F1 |
| --- | --- | --- |
| tagger | janes | 91.20 |
| lemmatizer | janes | 91.45 |
| tagger | janes no diacritics | 90.53 |
| lemmatizer | janes no diacritics | 90.29 |
| tagger | SUK | 96.39 |
| lemmatizer | SUK | 98.75 |

This baseline+suk+dediacritized model was chosen as the one that is to be published, since it displays a lower performance drop on the dev set without diacritics and its performance on the dev set with diacritics is better than the baseline+suk model. In addition, the performance drop on the SUK dev set is also very small.