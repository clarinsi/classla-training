# Detailed description of the training process

The Croatian models are trained in a slightly different way than the Slovene models. The lexicon is only applied to the lemmatizer, while the morphosyntactic tagger has no lexicon option. Two versions of the lemmatizer were thus trained, one with the lexicon and one without.

## Tagger

The tagger was trained using the following command:

-python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --wordvec_file all-token-hr-prelim.ft.sg.vec.xz --train_file conllu/hr500k-train.conllu --eval_file conllu/hr500k-dev.conllu --gold_file conllu/hr500k-dev.conllu --mode train --shorthand hr_set --output_file out-temp/pos/baseline_pos.conllu

Evaluation:

- python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --eval_file conllu/hr500k-test_empty.conllu --output_file out/pos/baseline_pos.conllu --gold_file conllu/hr500k-test.conllu --shorthand hr_set --mode predict >> eval_scores/baseline_pos.txt

## Lemmatizer

The lemmatizer was trained once with the [hrLex 1.3](http://hdl.handle.net/11356/1232) Croatian inflectional lexicon and once without the lexicon (this is referred to as "wolex") using the following commands:

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline-wolex_lemma --train_file conllu/hr500k-train.conllu --eval_file out/hr500k-dev_pos.conllu --output_file out-temp/baseline-wolex_pos_lemma.conllu --gold_file conllu/hr500k-dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos 

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --train_file conllu/hr500k-train.conllu --eval_file out/hr500k-dev_pos.conllu --output_file out-temp/baseline_pos_lemma.conllu --gold_file conllu/hr500k-dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos --external_dict hrLex_v1.3_classla-format

Evaluation:

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline-wolex_lemma --eval_file out/pos/baseline_pos.conllu --output_file out/lemma/baseline-wolex_pos_lemma.conllu --gold_file conllu/hr500k-test.conllu --mode predict >> eval_scores/baseline-wolex_lemma.txt

- python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --eval_file out/pos/baseline_pos.conllu --output_file out/lemma/baseline_pos_lemma.conllu --gold_file conllu/hr500k-test.conllu --mode predict >> eval_scores/baseline_lemma.txt

## Parser

The parser was trained on the hr_set-ud subset of the hr500k dataset. The dataset was first annotated for the upstream (morphosyntax, lemmas) using the freshly-trained models (the lemmatizer included the lexicon). The files with the annotated upstream are contained in out/pre-parsing/ The training was then carried out using the following commands:

- python -m classla.models.parser --save_dir models/depparse/ --save_name baseline_depparse --wordvec_file all-token-hr-prelim.ft.sg.vec.xz --train_file conllu/hr_set-ud-train.conllu --eval_file out/pre-parsing/hr_set-ud-dev_pos_lemma.conllu --gold_file conllu/hr_set-ud-dev.conllu --shorthand hr_set --output_file out-temp\temp_hr_set-ud-dev_pos_lemma_depparse.conllu --mode train

Evaluation:

- python -m classla.models.parser --save_dir models/depparse/ --save_name baseline_depparse --eval_file out/pre-parsing/hr_set-ud-test_pos_lemma.conllu --gold_file conllu/hr_set-ud-test.conllu --shorthand hr_set --output_file out/depparse/baseline_pos_lemma_depparse.conllu --mode predict >> eval_scores/baseline_depparse.txt

## SRL tagger

SRL NEEDS TO BE RESOLVED!!!! First the sentences containing SRL tags had to be extracted from the hr500k corpus and properly formatted. The extraction script is contained in conllu/extract_srl.py.

Training:

- python -m classla.models.srl_tagger --pretrain_file models/depparse/hr_set.pretrain.pt --train_file conllu/hr500k-train_srl.conllu --eval_file out/srl_dev_pos_lemma_depparse.conllu --gold_file conllu/hr500k-dev_srl.conllu --lang hr --shorthand hr_set --mode train --save_dir models/srl/ --save_name baseline_srl --output_file out-temp/temp_hr500k-dev.conllu


## Results:

### morphosyntax:

| model | UPOS | XPOS | UFeats | AllTags |
| --- | --- | --- | --- | --- |
| baseline | 97.73 | 94.87 | 95.37 | 94.33 |

### lemmatization

| model | lexicon used? | F1 |
| --- | --- | --- |
| baseline | Yes | 98.02 |
| baseline-wolex | No | 97.49 |

### parsing

| model | LAS |
| --- | --- |
| baseline_newlex | 87.46 |

It was decided that, moving forward, only one version of the lemmatizer (the lexicon version) is to be trained for the other languages.
