# Lemmatizer results 

"baseline+suk_lemma-lex_pos-lex" refers to lexicon used during lemma prediction and lexicon-predicted upstream pos annotations, "baseline+suk_lemma-lex_pos-wolex" refers to lexicon used during lemma prediction and upstream pos annotations predicted without lexicon,
"baseline+suk_lemma-wolex_pos-lex" refers to no lexicon used during lemma prediction and lexicon-predicted upstream pos annotations, "baseline+suk_lemma-wolex_pos-wolex" refers to no lexicon used during lemma prediction and upstream pos annotations predicted without lexicon:

## Evaluating on the janes dev set

| model | F1 |
| --- | --- |
| baseline+suk_lemma-lex_pos-lex | 91.24 |
| baseline+suk_lemma-lex_pos-wolex | 91.52 |
| baseline+suk_lemma-wolex_pos-lex | 93.62 |
| baseline+suk_lemma-wolex_pos-wolex | 93.97 |

## Evaluating on the SUK dev set

| model | F1 |
| --- | --- |
| baseline+suk_lemma-lex_pos-lex | 98.78 |
| baseline+suk_lemma-lex_pos-wolex | 98.70 |
| baseline+suk_lemma-wolex_pos-lex | 98.66 |
| baseline+suk_lemma-wolex_pos-wolex | 98.62 |