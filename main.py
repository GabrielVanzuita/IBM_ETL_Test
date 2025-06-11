import requests
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup
import datetime
from io import StringIO

LOG_FILE = 'etl_progress.log'
url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs = {'class': 'wikitable'}
exchange_rate_csv = '/home/gabriel/Desktop/Projects/worldkbankibm/exchange_rate.csv'
output_csv = 'country_gdp_transformed.csv'
db_path = 'country_gdp.db'
table_name = 'CountryGDP'

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")


def extract(url, table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    log_progress('Starting data extraction')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', attrs=table_attribs)
    if table is None:
        log_progress('No table found with the given attributes')
        return None
    df = pd.read_html(StringIO(str(table)))[0]
    log_progress('Data extraction completed')
    return df 

def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    log_progress('Starting data transformation')
    rates = pd.read_csv(csv_path, index_col=0).squeeze().to_dict()
    # Use the correct column name 'Market cap (US$ billion)'
    df['MC_GBP_Billion'] = (df['Market cap (US$ billion)'] * rates['GBP']).round(2)
    df['MC_EUR_Billion'] = (df['Market cap (US$ billion)'] * rates['EUR']).round(2)
    df['MC_INR_Billion'] = (df['Market cap (US$ billion)'] * rates['INR']).round(2)
    log_progress('Data transformation completed')
    return df


def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    log_progress(f'Saving data to CSV at {output_path}')
    df.to_csv(output_path, index=False)
    log_progress('Data saved to CSV')


def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    log_progress(f'Loading data to database table {table_name}')
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
    log_progress('Data loaded to database')


def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    log_progress(f'Running query: {query_statement}')
    result = pd.read_sql_query(query_statement, sql_connection)
    print(result)
    log_progress('Query executed')


if __name__ == '__main__':
    # ETL steps
    log_progress('ETL process started')
    df = extract(url, table_attribs)
    df = transform(df, exchange_rate_csv)
    load_to_csv(df, output_csv)

    # Connect to the database
    conn = sqlite3.connect(db_path)

    # Load data to the database
    load_to_db(df, conn, table_name)

    # Run a query
    query = f'SELECT * FROM {table_name} LIMIT 5;'
    run_query(query, conn)

    # Close the connection
    conn.close()
    log_progress('ETL process completed')



