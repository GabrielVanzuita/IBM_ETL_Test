from extractor import Extractor
from transformer import Transformer
from loader import Loader
import sqlite3

# Define parameters
url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs = {'class': 'wikitable sortable mw-collapsible jquery-tablesorter mw-made-collapsible'}
exchange_rate_csv = 'data/exchange_rates.csv'
output_csv = 'data/output/country_gdp_transformed.csv'
db_path = 'data/country_gdp.db'
table_name = 'CountryGDP'

if __name__ == '__main__':
    # Initialize ETL components
    extractor = Extractor()
    transformer = Transformer()
    loader = Loader()

    # ETL steps
    df = extractor.extract(url, table_attribs)
    df = transformer.transform(df, exchange_rate_csv)
    loader.load_to_csv(df, output_csv)

    # Connect to the database
    conn = sqlite3.connect(db_path)

    # Load data to the database
    loader.load_to_db(df, conn, table_name)

    # Run a query
    query = f'SELECT * FROM {table_name} LIMIT 5;'
    loader.run_query(query, conn)

    # Close the connection
    conn.close() 