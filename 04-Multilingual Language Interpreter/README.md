# Multilingual Language Interpreter using NLLB-200 a research MT model that supports 200 languages

## Overview
What It Does: NLLB-200 is a 600M parameter machine translation model that translates between 200 languages

For English to Foreign Translation

## Main Pointts
NLLB-200 is intended for research in machine translation, particularly for low-resource languages.
It enables single-sentence translation and is not meant for production deployment or document translation.
The model uses SentencePiece for preprocessing, and the model is publicly available.
Evaluation metrics include BLEU, spBLEU, chrF++, XSTS protocol, and toxicity assessment.
Flores-200 dataset was used for evaluation due to its comprehensive language coverage.
Training data involved parallel multilingual data from various public sources and monolingual data from Common Crawl.
Ethical considerations focus on human-centered design, minimizing risk for low-resource language users, and data privacy.
Potential risks include vulnerability to misinformation, unintended use by bad actors, and the presence of residual personally identifiable information in training data.
Users should be aware of potential mistranslations and their impact on decision-making, particularly in critical domains.

## Description
This code implements a multilingual language interpreter using the NLLB-200 pre-trained language translation model. It provides a Gradio interface with the following features:

[multilingual language interpreter](https://huggingface.co/spaces/2seriescs/Multilingual-Lang-Interpreter)

Text input field for the user to enter the text they want to translate.
Dropdown menu to select the desired destination language.
Translated text output field where the translated text will be displayed.

## Key Features
FLORES-200 Code Retrieval: The code retrieves the FLORES-200 code for the selected destination language from the language.json file.
Translation Function: The translate_text(<wbr>) function performs the translation using the NLLB-200 model and returns the translated text.
Gradio Interface: The code creates a Gradio interface with the necessary inputs, outputs, and title/description.

## Usage
Run the code to launch the language interpreter interface.
Enter the text you want to translate in the input field.
Select the desired destination language from the dropdown menu.
Click the "Translate" button to obtain the translated text