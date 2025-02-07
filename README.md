# classla-training
This repository contains the training scripts for the CLASSLA pipeline and the evaluation results for the new models.

The latest training process for standard Slovenian was carried out in January 2023 on the Slovenian [SUK training corpus](https://www.clarin.si/repository/xmlui/handle/11356/1747).
The following train-dev-test [splits](https://github.com/clarinsi/suk-split) for the SUK training corpus were used.

A detailed description of the training and evaluation processes can be found in sl/standard/README.detailed.md, along with a table of evaluation results. The conllu/ directory contains the gold data for SUK, eval_scores/ contains detailed evaluation results, and out/ contains all of the predictions.

Latest training of Slovenian non-standard models was performed in March 2023 on the [Janes-Tag 3.0 corpus](http://hdl.handle.net/11356/1732). The training and evaluation processes for sl non-standard models is detailed in sl/non-standard/README.detailed.nonst.md.

The first training of spoken models for Slovenian and a new model for Slovenian UD dependency parsing (trained on SUK v1.1) were performed in January 2025. The training processes are detailed in sl/spoken/ and sl/standard_SUK_1.1/.

