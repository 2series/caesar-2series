import torch
import gradio as gr

# Use a pipeline as a high-level helper
from transformers import pipeline

# question_answer = pipeline(
#     "question-answering", 
#     model="deepset/roberta-base-squad2")

model_path = ("./models--deepset--roberta-base-squad2/snapshots"
              "/cbf50ba81465d4d8676b8bab348e31835147541b/")

question_answer = pipeline("question-answering",
                           model="deepset/roberta-base-squad2")


# context = ("Enzo Ferrari was born on 18 February 1898 in Modena, Italy, while his birth certificate states 20 February.[3] His parents were Alfredo Ferrari and Adalgisa Bisbini; he had an older brother Alfredo Junior (Dino). Alfredo Senior was the son of a grocer from Carpi, and began a workshop fabricating metal parts at the family home.[4] Enzo grew up with little formal education. When he was 10 he witnessed Felice Nazzaro's win at the 1908 Circuito di Bologna, an event which inspired him to become a racing driver.[5] During World War I, he served in the 3rd Mountain Artillery Regiment of the Italian Army. His father Alfredo, and his older brother, Alfredo Jr., died in 1916 as a result of a widespread Italian flu outbreak. Ferrari became seriously sick himself during the 1918 flu pandemic and was consequently discharged from the Italian service.[citation needed]")

# # question = "who is Enzo?"

# question = "when was Enzo born?"

# answer = question_answer(question=question, 
#                          context=context )
# print(answer["answer"])


def read_file_content(file_obj):
    """
    Reads the content of a file object and returns it.
    Parameters:
    file_obj (file object): The file object to read from.
    Returns:
    str: The content of the file.
    """
    try:
        with open(file_obj.name, 'r', encoding='utf-8') as file:
            context = file.read()
            return context
    except Exception as e:
        return f"An error occurred: {e}"
    
def get_answer(file, question):
    context = read_file_content(file)
    answer = question_answer(question=question, context=context)
    return answer["answer"]

demo = gr.Interface(fn=get_answer, inputs=[gr.File(label="File Upload"), gr.Textbox(label="Prompt Input", lines=1)],
                     outputs=[gr.Textbox(label="Response", lines=1)],
                     title="@caesar-2series: Rag Application",
                     description="Retrieval Augmented Generation Questions-Answering Application")
demo.launch()