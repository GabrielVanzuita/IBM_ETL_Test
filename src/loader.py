import pandas as pd
import sqlite3
import datetime

class Loader:
    def __init__(self, log_file='logs/etl_progress.log'):
        self.log_file = log_file

    def log_progress(self, message):
        ''' This function logs the mentioned message of a given stage of the
        code execution to a log file. Function returns nothing'''
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a') as f:
            f.write(f"[{timestamp}] {message}\n")

    def load_to_csv(self, df, output_path):
        ''' This function saves the final data frame as a CSV file in
        the provided path. Function returns nothing.'''
        self.log_progress(f'Saving data to CSV at {output_path}')
        df.to_csv(output_path, index=False)
        self.log_progress('Data saved to CSV')

    def load_to_db(self, df, sql_connection, table_name):
        ''' This function saves the final data frame to a database
        table with the provided name. Function returns nothing.'''
        self.log_progress(f'Loading data to database table {table_name}')
        df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
        self.log_progress('Data loaded to database')

    def run_query(self, query_statement, sql_connection):
        ''' This function runs the query on the database table and
        prints the output on the terminal. Function returns nothing. '''
        self.log_progress(f'Running query: {query_statement}')
        result = pd.read_sql_query(query_statement, sql_connection)
        print(result)
        self.log_progress('Query executed') 