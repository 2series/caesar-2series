import json

import gradio as gr
import torch
# Use a pipeline as a high-level helper
from transformers import pipeline

# pipe = pipeline(
#     "translation", 
#     model="facebook/nllb-200-distilled-600M",
#     torch_dtype=torch.bfloat16)

model_path = ("./models--facebook--nllb-200-distilled-600M/snapshots"     
              "/f8d333a098d19b4fd9a8b18f94170487ad3f821d/")

text_translator = pipeline("translation", 
                           model=model_path,
                           torch_dtype=torch.bfloat16)

# Load the JSON data from the file
with open('language.json', 'r') as file:
    language_data = json.load(file)

def get_FLORES_code_from_language(language):
    for entry in language_data:
        if entry['Language'].lower() == language.lower():
            return entry['FLORES-200 code']
    return None


def translate_text(text, destination_language):
    dest_code = get_FLORES_code_from_language(destination_language)
    if dest_code is None:
        return "Invalid destination language."

    translation = text_translator(text, src_lang="eng_Latn", tgt_lang=dest_code)
    return translation[0]["translation_text"]

gr.close_all()

# demo = gr.Interface(fn=summary, inputs="text",outputs="text")
demo = gr.Interface(fn=translate_text,
                    inputs=[gr.Textbox(label="Input text for translation",lines=6), gr.Dropdown(
                        ["Arabic", "Afrikaans", "Bengali", "Greek", "Estonian", "Portuguese", "Spanish"], 
                        label="Select Destination Language")
                        ],
                    outputs=[gr.Textbox(label="Translated Text",lines=4)],
                    title="@caesar-2series: Multilingual Language Interpreter",
                    description="Translations from English into a few foreign languages")
demo.launch()