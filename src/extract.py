import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
import datetime

LOG_FILE = 'logs/etl_progress.log'

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