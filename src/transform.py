import pandas as pd
import datetime

LOG_FILE = 'logs/etl_progress.log'

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")


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