# Detailed description of the training process




## Tagger

The tagger was trained using the following command:

```
python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --wordvec_file all-token-bg-prelim.ft.sg.vec.xz --train_file conllu/train.conllu --eval_file conllu/dev.conllu --gold_file conllu/dev.conllu --mode train --shorthand bg_btb --output_file out-temp/pos/baseline_pos.conllu
```


Evaluation:

```
python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --eval_file conllu/test_empty.conllu --output_file out/pos/baseline_pos.conllu --gold_file conllu/test.conllu --shorthand bg_btb --mode predict >> eval_scores/baseline_pos.txt
```

## Lemmatizer

Lemmatizer training was carried out as follows:


```
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --train_file conllu/train.conllu --eval_file out/dev_pos.conllu --output_file out-temp/baseline_pos_lemma.conllu --gold_file conllu/dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos --external_dict infldict_bg_classla_format.txt
```

Evaluation:

```
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --eval_file out/pos/baseline_pos.conllu --output_file out/lemma/baseline_pos_lemma.conllu --gold_file conllu/test.conllu --mode predict >> eval_scores/baseline_lemma.txt
```

## Parser

The parser was trained on the bg_btb UD dataset:


```
python -m classla.models.parser --save_dir models/depparse/ --save_name baseline_depparse --wordvec_file all-token-bg-prelim.ft.sg.vec.xz --train_file conllu/bg_btb-ud-train.conllu --eval_file out/pre-parsing/bg_btb-ud-dev_pos_lemma.conllu --gold_file conllu/bg_btb-ud-dev.conllu --shorthand bg_btb --output_file out-temp/baseline_pos_lemma_depparse.conllu --mode train
```

Evaluation:

```
python -m classla.models.parser --save_dir models/depparse/ --save_name baseline_depparse --eval_file out/pre-parsing/bg_btb-ud-test_pos_lemma.conllu --gold_file conllu/bg_btb-ud-test.conllu --shorthand bg_btb --output_file out/depparse/baseline_pos_lemma_depparse.conllu --mode predict >> eval_scores/baseline_depparse.txt
```

## Results:

### morphosyntax:

| model | UPOS | XPOS | UFeats | AllTags |
| --- | --- | --- | --- | --- |
| baseline | 97.70 | 96.83 | 96.69 | 94.46 |

### lemmatization

| model | F1 |
| --- | --- |
| baseline | 98.93 |

### parsing

| model | LAS |
| --- | --- |
| baseline_newlex | 91.18 |