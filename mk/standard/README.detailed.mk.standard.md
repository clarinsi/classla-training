# Detailed description of the training process




## Tagger

The tagger was trained using the following command:

```
python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --wordvec_file all-token-mk-prelim.ft.sg.vec.xz --train_file conllu/train+setmk15k.conllu --eval_file conllu/dev.conllu --gold_file conllu/dev.conllu --mode train --shorthand mk_set --output_file out-temp/pos/baseline_pos.conllu
```

Evaluation:

```
python -m classla.models.tagger --save_dir models/pos/ --save_name baseline_pos --eval_file conllu/test_empty.conllu --output_file out/pos/baseline_pos.conllu --gold_file conllu/test.conllu --shorthand mk_set --mode predict >> eval_scores/baseline_pos.txt
```

## Lemmatizer

The lemmatizer training was carried out using the following:

```
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --train_file conllu/train+setmk15k.conllu --eval_file out/dev_pos.conllu --output_file out-temp/baseline_pos_lemma.conllu --gold_file conllu/dev.conllu --mode train --num_epoch 30 --decay_epoch 20 --pos
```

Evaluation:

```
python -m classla.models.lemmatizer --model_dir models/lemma/ --model_file baseline_lemma --eval_file out/pos/baseline_pos.conllu --output_file out/lemma/baseline_pos_lemma.conllu --gold_file conllu/test.conllu --mode predict >> eval_scores/baseline_lemma.txt
```

## Results:

### morphosyntax:

| model | UPOS | XPOS | UFeats | AllTags |
| --- | --- | --- | --- | --- |
| baseline | 98.47 | 97.14 | 97.54 | 96.99 |

### lemmatization

| model | F1 |
| --- | --- |
| baseline | 98.81 |