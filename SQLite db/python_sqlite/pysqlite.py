import sqlite3
from sqlite3 import Error
import os

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file.

    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ Create a table from the create_table_sql statement.

    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r"pythonsqlite.db"

    # Create a database connection
    conn = create_connection(database)
    with conn:
        # Create projects table
        sql_create_projects_table = """
            CREATE TABLE IF NOT EXISTS projects (
                id integer PRIMARY KEY,
                name text NOT NULL,
                begin_date text,
                end_date text
            );
        """
        create_table(conn, sql_create_projects_table)

        # Create tasks table
        sql_create_tasks_table = """
            CREATE TABLE IF NOT EXISTS tasks (
                id integer PRIMARY KEY,
                name text NOT NULL,
                priority integer,
                status_id integer,
                project_id integer NOT NULL,
                begin_date text NOT NULL,
                end_date text NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            );
        """
        create_table(conn, sql_create_tasks_table)

        # Create a new project
        project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
        create_project(conn, project)

        # Tasks
        task_1 = ('Analyze the requirements of the app', 1, 1, 1, '2015-01-01', '2015-01-02')
        task_2 = ('Confirm with user about the top requirements', 1, 1, 1, '2015-01-03', '2015-01-05')

        # Create tasks
        create_task(conn, task_1)
        create_task(conn, task_2)

def create_project(conn, project):
    """
    Create a new project into the projects table.

    :param conn: Connection object
    :param project: A tuple containing project data: (name, begin_date, end_date)
    :return: project id
    """
    sql = '''
        INSERT INTO projects(name, begin_date, end_date)
        VALUES(?, ?, ?)
    '''
    cursor = conn.cursor()
    cursor.execute(sql, project)
    conn.commit()
    return cursor.lastrowid

def create_task(conn, task):
    """
    Create a new task.

    :param conn: Connection object
    :param task: A tuple containing task data: (name, priority, status_id, project_id, begin_date, end_date)
    :return:
    """

    sql = '''
        INSERT INTO tasks(name, priority, status_id, project_id, begin_date, end_date)
        VALUES(?, ?, ?, ?, ?, ?)
    '''
    cursor = conn.cursor()
    cursor.execute(sql, task)
    conn.commit()

# Update data
# update task()
def update_task(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
              SET priority = ?,
                  begin_date = ?,
                  end_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    
if __name__ == '__main__':
    main()