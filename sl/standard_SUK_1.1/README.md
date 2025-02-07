# Detailed description of the training process
Parsing models were trained for the SUK 1.1 update, as only UD dependency relations changed in this version. Additionally, NER models were also trained using the NER tags present in the SUK corpus.

## Parser
empty dev and test sets were first generated and populated with upstream annotations (morphosyntactic tags, lemmas) using classla v 2.1.1. Then, parser training was run using the following command:

- python -m classla.models.parser --save_dir models/ --save_name depparse --wordvec_file ../all-token-prelim.ft.sg.vec.xz --train_file conllu/train/sl_ssj-ud-train.conllu --eval_file out/sl_ssj-ud-dev.pos.lemma.conllu --gold_file conllu/dev/sl_ssj-ud-dev.conllu --shorthand sl_ssj --output_file out-temp\sl_ssj-ud-dev.pos.lemma.depparse.conllu --mode train

Evaluation:

- python -m classla.models.parser --save_dir models/ --save_name depparse --eval_file out/sl_ssj-ud-test.pos.lemma.conllu --gold_file conllu/test/sl_ssj-ud-test.conllu --shorthand sl_ssj --output_file out/sl_ssj-ud-test.pos.lemma.depparse.conllu --mode predict > eval_scores/depparse.txt

## NER tagger

The NER tags were first converted to the correct format that CLASSLA-Stanza expects on model training input. The conversion script that converts NER tags from the CoNLL03 format to the appropriate json format can be found in the CLASSLA-Stanza library at classla/utils/prepare_ner_data.py. Training was run with the following command:

- python -m classla.models.ner_tagger --wordvec_file ../all-token-prelim.ft.sg.vec.xz --train_file conllu/train/SUK_train_NER.json --eval_file conllu/dev/SUK_dev_NER.json --lang sl --shorthand sl_ssj --mode train --save_dir models/ --save_name ner --scheme bio --batch_size 128

Evaluation was done directly via the [Slobench evaluation platform](https://slobench.cjvt.si/) to ensure comparability with existing NER taggers.

## Results

### Syntactic parsing

|  | LAS |
| --- | --- |
|  | 90.42 |
