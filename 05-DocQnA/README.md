# Rag Questions-Answering Application using Pre-trained language model roberta-base for QA

## Description:
This project utilizes the `transformers` library to develop a Retrieval Augmented Generation (RAG) application for QA. The application allows users to upload a file and enter a question, with the RAG model providing an answer based on the context of the document.

[Rag Qustion-Answer App](https://huggingface.co/spaces/2seriescs/Question-Answering)


**Key Features:**

* Uses the `transformers` library for question-answering with Retrieval Augmented Generation.
* Reads the content of uploaded files.
* Provides a user-friendly interface for input and output.

**Installation:**

pip install requirements.txt

**Usage:**

1. Run the code.
2. Upload a file containing relevant context.
3. Enter a question in the prompt input field.
4. Click the "Submit" button to get the answer.

**Dependencies:**

* `transformers`
* `gradio`

**Running the application:**

**Note:**

* The specific model used in this application is `deepset/roberta-base-squad2`.
* The context provided in the example code can be replaced with text from any source.
* The application can be further extended with features such as user authentication and storage of uploaded files.

**Additional Information:**

* The source code is available on GitHub.
* Please feel free to contribute to the project.

**Disclaimer:**

This application is provided as is without any warranty. Please use it at your own risk.