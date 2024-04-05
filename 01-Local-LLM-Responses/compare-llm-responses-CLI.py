import os
import time
import logging
import traceback

import ollama

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)

# Turn File into a variable value
current_directory = os.path.dirname(os.path.abspath(__file__))
file_name = 'data.txt'
file_path = os.path.join(current_directory, file_name)
try:
    with open(file_path, 'r') as file:
        data = file.read()
except Exception as e:
    logging.error(f"Error reading file: {e}")
    print(traceback.format_exc())
    raise e

def ask(query, llm, data):
    query = f"Answer this user query: {query} based on the information in this data: {data} -- be as succinct as possible -- just answer the specific question with no other information"
    start_time = time.time()
    try:
        response = ollama.chat(model=llm, messages=[{'role': 'user', 'content': query}])
    except Exception as e:
        logging.error(f"Error while calling LLM: {e}")
        print(traceback.format_exc())
        return None, None
    response_time = time.time() - start_time
    response = response['message']['content']
    return response, response_time

if __name__ == "__main__":
    while True:
        try:
            query = input("How can I assist you? ")
            print("\nQuestion:", query)
            for model_type in ['llama2', 'phi', 'mistral']:
                answer, response_time = ask(query, model_type, data)
                if answer is not None:
                    print(f"\nModel: {model_type}\nResponse:\n{answer}\nTime taken: {response_time}")
        except KeyboardInterrupt:
            break