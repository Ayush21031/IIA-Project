import pandas as pd
import mysql.connector
from mysql.connector import errorcode

# MySQL server connection configuration
config = {
    'user': 'root',
    'password': '123456789',  # Replace with your MySQL password
    'host': 'localhost',
    'database': 'Banks',       # Assuming GAV is within the Banks database
    'raise_on_warnings': True
}

# Mapping dictionaries for Accounts and Transactions
accounts_mapping = {
    'ICICI_Accounts': {
        'AccountID': 'ICICI_AccountID',
        'CustomerName': 'CustomerName',
        'AccountNumber': 'AccountNumber',
        'ServiceType': 'ServiceType',
        'NationalID': 'NationalID',
        'Balance': 'Balance',
        'InterestRate': 'InterestRate',
        'LastUpdated': 'LastUpdated',
        'BankName': "'ICICI'"
    },
    'HDFC_Accounts': {
        'AccountID': 'HDFC_AccountID',
        'CustomerName': 'ClientName',
        'AccountNumber': 'AccNo',
        'ServiceType': 'AccountType',
        'NationalID': 'GovtID',
        'Balance': 'CurrentBalance',
        'InterestRate': 'MonthlyInterest',
        'LastUpdated': 'LastUpdate',
        'BankName': "'HDFC'"
    },
    'SBI_Accounts': {
        'AccountID': 'SBI_AccountID',
        'CustomerName': 'AccountHolder',
        'AccountNumber': 'Acc_Number',
        'ServiceType': 'Service_Type',
        'NationalID': 'National_ID',
        'Balance': 'AmountStored',
        'InterestRate': 'Interest_Rate',
        'LastUpdated': 'Last_Updated',
        'BankName': "'SBI'"
    }
}

transactions_mapping = {
    'ICICI_Transactions': {
        'TransactionID': 'TransactionID',
        'AccountID': 'ICICI_AccountID',
        'TransactionDate': 'TransactionDate',
        'TransactionType': 'TransactionType',
        'Amount': 'Amount',
        'Description': 'Description',
        'BankName': "'ICICI'"
    },
    'HDFC_Transactions': {
        'TransactionID': 'TransactionID',
        'AccountID': 'HDFC_AccountID',
        'TransactionDate': 'TransDate',
        'TransactionType': 'Type',
        'Amount': 'TransAmount',
        'Description': 'Notes',
        'BankName': "'HDFC'"
    },
    'SBI_Transactions': {
        'TransactionID': 'TransactionID',
        'AccountID': 'SBI_AccountID',
        'TransactionDate': 'Date',
        'TransactionType': 'Type_of_Transaction',
        'Amount': 'Amount',
        'Description': 'Details',
        'BankName': "'SBI'"
    }
}

# Function to generate SELECT statements based on mapping
def generate_select_statement(table_name, mapping, standard_columns, include_bank_name=True):
    select_parts = []
    for std_col in standard_columns:
        if std_col in mapping[table_name]:
            tbl_col = mapping[table_name][std_col]
            if std_col == 'BankName' and include_bank_name:
                select_parts.append(f"{tbl_col} AS `{std_col}`")
            else:
                select_parts.append(f"`{tbl_col}` AS `{std_col}`")
    select_clause = ",\n    ".join(select_parts)
    return f"SELECT \n    {select_clause}\nFROM `{table_name}`"

# Function to create a view
def create_view(cursor, view_name, select_statements):
    union_all_query = "\nUNION ALL\n".join(select_statements)
    create_view_query = f"CREATE OR REPLACE VIEW `{view_name}` AS\n{union_all_query};"
    cursor.execute(create_view_query)
    print(f"View '{view_name}' created successfully.")

# Connect to MySQL server
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    print("Connected to MySQL server.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

# Define standard columns for Accounts and Transactions, including BankName
standard_accounts_columns = [
    'AccountID',
    'CustomerName',
    'AccountNumber',
    'ServiceType',
    'NationalID',
    'Balance',
    'InterestRate',
    'LastUpdated',
    'BankName'  # New column
]

standard_transactions_columns = [
    'TransactionID',
    'AccountID',
    'TransactionDate',
    'TransactionType',
    'Amount',
    'Description',
    'BankName'  # New column
]

# Generate SELECT statements for Accounts
accounts_select_statements = []
for table in accounts_mapping:
    stmt = generate_select_statement(table, accounts_mapping, standard_accounts_columns)
    accounts_select_statements.append(stmt)

# Generate SELECT statements for Transactions
transactions_select_statements = []
for table in transactions_mapping:
    stmt = generate_select_statement(table, transactions_mapping, standard_transactions_columns)
    transactions_select_statements.append(stmt)

# Create Global_Accounts view
create_view(cursor, 'Global_Accounts', accounts_select_statements)

# Create Global_Transactions view
create_view(cursor, 'Global_Transactions', transactions_select_statements)

# Commit changes
cnx.commit()
print("Global Views created successfully.")

# Close cursor and connection
cursor.close()
cnx.close()
print("Connection closed.")
