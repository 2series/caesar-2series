# Import necessary libraries
from bottle import route, post, run, request
import sqlite3
import os
import ollama
import time

# Set the current directory and file path for the data file
current_directory = os.path.dirname(os.path.abspath(__file__))
file_name = 'data.txt'
file_path = os.path.join(current_directory, file_name)

# Read the data file
with open(file_path, 'r') as file:
    data = file.read()

# Class for interacting with the database
class database:
    # Get the file path for the database
    @staticmethod
    def path():
        current_directory = os.path.dirname(os.path.abspath(__file__))
        db_name = 'query.db'
        file_path = os.path.join(current_directory, db_name)
        return file_path

    # Create the database table if it doesn't exist
    @staticmethod
    def db_create():
        file_path = database.path()
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()

        create_table = '''
                        create table if not exists result(
                            id integer primary key,
                            model text,
                            query text,
                            response text,
                            time text
                        )
                        '''

        cursor.execute(create_table)
        conn.commit()
        conn.close()

    # Select all records from the database table
    @staticmethod
    def db_select():
        file_path = database.path()
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        sql = 'select * from result order by id desc'
        cursor.execute(sql)
        record = cursor.fetchall()
        conn.commit()
        conn.close()

        return record

    # Insert a new record into the database table
    @staticmethod
    def db_insert(model, query, response, time):
        file_path = database.path()
        conn = sqlite3.connect(file_path)
        cursor = conn.cursor()
        sql = 'insert into result(model, query, response, time) values(?,?,?,?)'
        cursor.execute(sql,(model, query, response, time))
        conn.commit()
        conn.close()

# Function for interacting with the LLM model
def ask(query, llm, data):
    # Start the timer
    time_start = time.time()

    # Format the query for the LLM model
    query = f'Answer this user query: {query} \
            based on the information in this data: {data} \
            -- be as succinct as possible \
            -- just answer the specific question with no other information'

    # Send the query to the LLM model and get the response
    response = ollama.chat(model=llm, messages=[
    {
        'role': 'user',
        'content': query,
    },
    ])
    response = response['message']['content']

    # Stop the timer and calculate the elapsed time
    time_elapse = time.time() - time_start

    return response, time_elapse

# Index page for the web application
@route('/')
@post('/')
def index():
    # Get the user's query from the form
    query = request.forms.get('query')

    # List of LLM models to use
    model = ['llama2', 'mistral', 'phi']

    # If a query was submitted, send it to each LLM model and insert the results into the database
    if query!= None:
        for version in model:
            response = ask(query, version, data)
            database.db_insert(version, query, response[0], response[1])
            print(response)

    # Select all records from the database table
    record_set = database.db_select()

    # Generate the HTML for the form and previous results
    form = f'''
                <form action="./" method="post">
                Question: <textarea cols="50" rows="1" name="query" value="{query}"></textarea>
                <br>
                <input type="submit">
                </form>
            '''

    previous = ''
    set_new = ''
    set_old = ''
    for record in record_set:
        set_new = record[2]
        if set_new!= set_old:
            previous = f'{previous}</div><br><div style="border:solid 3px black;">\
                        <span style="font-size:20;font-weight:bold;">{set_new}</span>'
            set_old = set_new
        previous = f'''
                        {previous} 
                        <div style="border:solid 1px black">
                            <strong>Model:</strong> {record[1]} <br>
                            <strong>Response:</strong><br> {record[3]}
                            <strong>Time:</strong> {record[4]}
                        </div>
                    '''

    page = f'''
                {form}
                {previous}
            '''

    return page

# Create the database table if it doesn't exist
database.db_create()

# Start the web application
run(host='localhost', port=8080)
