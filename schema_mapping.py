import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from fuzzywuzzy import fuzz

# Download NLTK data files (run once)
nltk.download('stopwords')

# -------------------- Configuration --------------------

# MySQL server connection configuration
config = {
    'user': 'root',
    'password': '123456789',  # Replace with your MySQL password
    'host': 'localhost',
    'raise_on_warnings': True
}

# Databases to connect to
databases = ['Banks', 'MutualFunds', 'StockPlatforms']

# -------------------- Global Schemas Definition --------------------

# Define the global schema for Accounts
global_accounts_schema = {
    'AccountID': 'INT',
    'CustomerName': 'VARCHAR(255)',
    'AccountNumber': 'VARCHAR(50)',
    'AccountType': 'VARCHAR(50)',
    'NationalID': 'VARCHAR(20)',
    'Balance': 'FLOAT',
    'InterestRate': 'FLOAT',
    'LastUpdated': 'DATE'
}

# Define the global schema for Transactions
global_transactions_schema = {
    'TransactionID': 'INT',
    'AccountID': 'INT',
    'TransactionDate': 'DATE',
    'TransactionType': 'VARCHAR(50)',
    'Amount': 'FLOAT',
    'Description': 'VARCHAR(255)'
}

# -------------------- Utility Functions --------------------

def connect_to_mysql(config):
    """
    Establish a connection to the MySQL server.
    """
    try:
        cnx = mysql.connector.connect(**config)
        print("Successfully connected to MySQL server.")
        return cnx
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)

def get_table_columns(cursor, db_name, table_name):
    """
    Retrieve the column names and data types for a given table.
    """
    query = f"""
    SELECT COLUMN_NAME, DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = '{db_name}' AND TABLE_NAME = '{table_name}';
    """
    cursor.execute(query)
    result = cursor.fetchall()
    columns = pd.DataFrame(result, columns=['COLUMN_NAME', 'DATA_TYPE'])
    return columns

def preprocess_column_names(column_names):
    """
    Preprocess column names by replacing underscores with spaces,
    removing special characters, converting to lowercase,
    and removing stopwords.
    """
    stop_words = set(stopwords.words('english'))
    processed_names = []
    for name in column_names:
        # Replace underscores with space
        name_clean = name.replace('_', ' ')
        # Remove special characters except space
        name_clean = re.sub(r'[^a-zA-Z ]', '', name_clean)
        # Convert to lowercase
        name_clean = name_clean.lower()
        # Tokenize and remove stopwords
        tokens = name_clean.split()
        tokens = [token for token in tokens if token not in stop_words]
        # Rejoin tokens
        name_processed = ' '.join(tokens)
        processed_names.append(name_processed)
    return processed_names

def match_columns_fuzzy(global_schema, source_columns, threshold=50):
    """
    Match source columns to global schema columns using fuzzy string matching.
    Returns a mapping dictionary with similarity scores.
    """
    global_col_names = list(global_schema.keys())
    source_col_names = source_columns['COLUMN_NAME'].tolist()
    
    mapping = {}
    for source_col in source_col_names:
        best_match = None
        highest_score = 0
        best_score1 = 0
        best_score2 = 0
        for global_col in global_col_names:
            # Compute similarity score using token_set_ratio and partial_ratio
            score1 = fuzz.token_set_ratio(source_col.lower(), global_col.lower())
            score2 = fuzz.partial_ratio(source_col.lower(), global_col.lower())
            score = max(score1, score2)
            if score > highest_score:
                highest_score = score
                best_match = global_col
                best_score1 = score1
                best_score2 = score2
        if highest_score >= threshold:
            mapping[source_col] = best_match
            print(f"  {source_col} --> {best_match} (Score: {highest_score})")
        else:
            mapping[source_col] = None
            print(f"  {source_col} --> None (Score: {highest_score})")
    return mapping

# -------------------- Main Script --------------------

def main():
    # Connect to MySQL server
    cnx = connect_to_mysql(config)
    cursor = cnx.cursor()

    # Dictionaries to hold mappings for each table
    schema_mappings = {}

    # Focus on the Banks database and map account and transaction tables
    db_name = 'Banks'
    cursor.execute(f"USE {db_name};")
    print(f"\n--- Processing Database: {db_name} ---")

    # Tables to process for Accounts and Transactions
    accounts_tables = ['ICICI_Accounts', 'HDFC_Accounts', 'SBI_Accounts']
    transactions_tables = ['ICICI_Transactions', 'HDFC_Transactions', 'SBI_Transactions']

    # Process Accounts Tables
    print("\nMapping Accounts Tables:")
    for table in accounts_tables:
        source_columns = get_table_columns(cursor, db_name, table)
        print(f"\nMapping for table '{table}':")
        mapping = match_columns_fuzzy(global_accounts_schema, source_columns)
        schema_mappings[table] = mapping

    # Process Transactions Tables
    print("\nMapping Transactions Tables:")
    for table in transactions_tables:
        source_columns = get_table_columns(cursor, db_name, table)
        print(f"\nMapping for table '{table}':")
        mapping = match_columns_fuzzy(global_transactions_schema, source_columns)
        schema_mappings[table] = mapping

    # Close cursor and connection
    cursor.close()
    cnx.close()
    print("\nSchema mapping completed.")

if __name__ == "__main__":
    main()
