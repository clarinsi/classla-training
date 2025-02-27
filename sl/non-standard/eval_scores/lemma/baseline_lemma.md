# Lemmatizer results 

"baseline_lemma-lex_pos-lex" refers to lexicon used during lemma prediction and lexicon-predicted upstream pos annotations, "baseline_lemma-lex_pos-wolex" refers to lexicon used during lemma prediction and upstream pos annotations predicted without lexicon,
"baseline_lemma-wolex_pos-lex" refers to no lexicon used during lemma prediction and lexicon-predicted upstream pos annotations, "baseline_lemma-wolex_pos-wolex" refers to no lexicon used during lemma prediction and upstream pos annotations predicted without lexicon:

## Entire dataset

### Evaluated on janes dev set

| model | F1 |
| --- | --- |
| baseline_lemma-lex_pos-lex | 91.29 |
| baseline_lemma-lex_pos-wolex | 91.51 |
| baseline_lemma-wolex_pos-lex | 93.38 |
| baseline_lemma-wolex_pos-wolex | 93.75 |

### Evaluated on SUK dev set

| model | F1 |
| --- | --- |
| baseline_lemma-lex_pos-lex | 97.67 |
| baseline_lemma-lex_pos-wolex | 96.83 |
| baseline_lemma-wolex_pos-lex | 95.34 |
| baseline_lemma-wolex_pos-wolex | 94.96 |

