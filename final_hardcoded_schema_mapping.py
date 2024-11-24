import pandas as pd
import mysql.connector
from mysql.connector import errorcode

# MySQL server connection configuration
config = {
    'user': 'root',
    'password': '123456789',  # Replace with your MySQL password
    'host': 'localhost',
    'raise_on_warnings': True
}

# Function to generate SELECT statements based on mapping
def generate_select_statement(table_name, mapping, standard_columns):
    select_parts = []
    for std_col in standard_columns:
        if std_col in mapping[table_name]:
            tbl_col = mapping[table_name][std_col]
            if std_col in ['BankName', 'CompanyName', 'PlatformName']:
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

# Schema mapping for Banks database
def create_banks_views():
    # Use Banks database
    cursor.execute("USE Banks")
    print("Using database 'Banks'.")

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

    print("Banks Global Views created successfully.")

# Schema mapping for MutualFunds database
def create_mutualfunds_views():
    # Use MutualFunds database
    cursor.execute("USE MutualFunds")
    print("Using database 'MutualFunds'.")

    # Mapping dictionaries for Clients and Returns
    clients_mapping = {
        'SBI_MF_Clients': {
            'ClientID': 'SBI_ClientID',
            'ClientName': 'FullName',
            'Email': 'ClientEmail',
            'PhoneNumber': 'ContactNumber',
            'PAN': 'PAN_Number',
            'Address': 'Address',
            'DateOfBirth': 'DateOfBirth',
            'RegistrationDate': 'RegistrationDate',
            'CompanyName': "'SBI'"
        },
        'TataMF_Investors': {
            'ClientID': 'Tata_ClientID',
            'ClientName': 'InvestorName',
            'Email': 'EmailAddress',
            'PhoneNumber': 'PhoneNumber',
            'PAN': 'PAN',
            'Address': 'ResidentialAddress',
            'DateOfBirth': 'DOB',
            'RegistrationDate': 'JoinDate',
            'CompanyName': "'TataMF'"
        },
        'BajajMF_Customers': {
            'ClientID': 'Bajaj_CustomerID',
            'ClientName': 'Name',
            'Email': 'Email',
            'PhoneNumber': 'Mobile',
            'PAN': 'PAN_Num',
            'Address': 'Addr',
            'DateOfBirth': 'DOB',
            'RegistrationDate': 'DateJoined',
            'CompanyName': "'BajajMF'"
        }
    }

    returns_mapping = {
        'SBI_MF_Returns': {
            'ReturnID': 'ReturnID',
            'MutualFundID': 'MutualFundID',
            'ClientID': 'SBI_ClientID',
            'InvestmentDate': 'InvestmentDate',
            'UnitsPurchased': 'UnitsPurchased',
            'InvestmentAmount': 'InvestmentAmount',
            'PurchaseRate': 'PurchaseRate',
            'CurrentNAV': 'CurrentNAV',
            'CurrentValue': 'CurrentValue',
            'ReturnPercentage': 'ReturnPercentage',
            'LastUpdated': 'LastUpdated',
            'CompanyName': "'SBI'"
        },
        'TataMF_InvestmentReturns': {
            'ReturnID': 'InvestmentReturnID',
            'MutualFundID': 'MutualFundID',
            'ClientID': 'Tata_ClientID',
            'InvestmentDate': 'DateOfInvestment',
            'UnitsPurchased': 'UnitsBought',
            'InvestmentAmount': 'InvestmentINR',
            'PurchaseRate': 'PurchaseRate',
            'CurrentNAV': 'CurrentNAVValue',
            'CurrentValue': 'InvestmentValue',
            'ReturnPercentage': 'GainLossPercentage',
            'LastUpdated': 'LastUpdated',
            'CompanyName': "'TataMF'"
        },
        'BajajMF_ClientReturns': {
            'ReturnID': 'ClientReturnID',
            'MutualFundID': 'MutualFundID',
            'ClientID': 'Bajaj_CustomerID',
            'InvestmentDate': 'InvestmentDate',
            'UnitsPurchased': 'UnitsPurchased',
            'InvestmentAmount': 'AmountInvested',
            'PurchaseRate': 'PurchaseRate',
            'CurrentNAV': 'CurrentNAV',
            'CurrentValue': 'CurrentValue',
            'ReturnPercentage': 'ProfitLossPerc',
            'LastUpdated': 'UpdateDate',
            'CompanyName': "'BajajMF'"
        }
    }

    # Define standard columns
    standard_clients_columns = [
        'ClientID',
        'ClientName',
        'Email',
        'PhoneNumber',
        'PAN',
        'Address',
        'DateOfBirth',
        'RegistrationDate',
        'CompanyName'
    ]

    standard_returns_columns = [
        'ReturnID',
        'MutualFundID',
        'ClientID',
        'InvestmentDate',
        'UnitsPurchased',
        'InvestmentAmount',
        'PurchaseRate',
        'CurrentNAV',
        'CurrentValue',
        'ReturnPercentage',
        'LastUpdated',
        'CompanyName'
    ]

    # Generate SELECT statements for Clients
    clients_select_statements = []
    for table in clients_mapping:
        stmt = generate_select_statement(table, clients_mapping, standard_clients_columns)
        clients_select_statements.append(stmt)

    # Generate SELECT statements for Returns
    returns_select_statements = []
    for table in returns_mapping:
        stmt = generate_select_statement(table, returns_mapping, standard_returns_columns)
        returns_select_statements.append(stmt)

    # Create Global_Clients view
    create_view(cursor, 'Global_MF_Clients', clients_select_statements)

    # Create Global_Returns view
    create_view(cursor, 'Global_MF_Returns', returns_select_statements)

    print("MutualFunds Global Views created successfully.")

# Schema mapping for StockPlatforms database
def create_stockplatforms_views():
    # Use StockPlatforms database
    cursor.execute("USE StockPlatforms")
    print("Using database 'StockPlatforms'.")

    # Mapping dictionaries for Clients, Stocks, Orders, and Stock_Prices
    clients_mapping = {
        'Zerodha_Clients': {
            'ClientID': 'Zerodha_ClientID',
            'ClientName': 'ClientName',
            'Email': 'Email',
            'PhoneNumber': 'PhoneNumber',
            'PAN': 'PAN',
            'Address': 'Address',
            'DateOfBirth': 'DateOfBirth',
            'RegistrationDate': 'AccountCreationDate',
            'PlatformName': "'Zerodha'"
        },
        'Groww_Clients': {
            'ClientID': 'Groww_ClientID',
            'ClientName': 'ClientName',
            'Email': 'Email',
            'PhoneNumber': 'PhoneNumber',
            'PAN': 'PAN',
            'Address': 'Address',
            'DateOfBirth': 'DateOfBirth',
            'RegistrationDate': 'AccountCreationDate',
            'PlatformName': "'Groww'"
        },
        'SBI_Stocks_Clients': {
            'ClientID': 'SBI_ClientID',
            'ClientName': 'ClientName',
            'Email': 'Email',
            'PhoneNumber': 'PhoneNumber',
            'PAN': 'PAN',
            'Address': 'Address',
            'DateOfBirth': 'DateOfBirth',
            'RegistrationDate': 'AccountStartDate',
            'PlatformName': "'SBI_Stocks'"
        }
    }

    stocks_mapping = {
        'Zerodha_Stocks': {
            'StockID': 'Zerodha_StockID',
            'StockSymbol': 'StockSymbol',
            'StockName': 'StockName',
            'Sector': 'Sector',
            'Exchange': 'Exchange',
            'PlatformName': "'Zerodha'"
        },
        'Groww_Stocks': {
            'StockID': 'Groww_StockID',
            'StockSymbol': 'Symbol',
            'StockName': 'Name',
            'Sector': 'Sector',
            'Exchange': 'Exchange',
            'PlatformName': "'Groww'"
        },
        'SBI_Stocks_List': {
            'StockID': 'SBI_StockID',
            'StockSymbol': 'StockCode',
            'StockName': 'StockName',
            'Sector': 'Sector',
            'Exchange': 'Exchange',
            'PlatformName': "'SBI_Stocks'"
        }
    }

    orders_mapping = {
        'Zerodha_Orders': {
            'OrderID': 'OrderID',
            'ClientID': 'ClientID',
            'StockID': 'StockID',
            'OrderType': 'OrderType',
            'Quantity': 'Quantity',
            'PricePerShare': 'PricePerShare',
            'TotalAmount': 'TotalAmount',
            'OrderDate': 'OrderDate',
            'OrderStatus': 'OrderStatus',
            'PlatformName': "'Zerodha'"
        },
        'Groww_Orders': {
            'OrderID': 'OrderID',
            'ClientID': 'ClientID',
            'StockID': 'StockID',
            'OrderType': 'Type',
            'Quantity': 'Quantity',
            'PricePerShare': 'Price',
            'TotalAmount': 'TotalValue',
            'OrderDate': 'Timestamp',
            'OrderStatus': 'Status',
            'PlatformName': "'Groww'"
        },
        'SBI_Stocks_Orders': {
            'OrderID': 'OrderID',
            'ClientID': 'ClientID',
            'StockID': 'StockID',
            'OrderType': 'TradeType',
            'Quantity': 'Quantity',
            'PricePerShare': 'PricePerShare',
            'TotalAmount': 'TotalValue',
            'OrderDate': 'TradeTimestamp',
            'OrderStatus': 'TradeStatus',
            'PlatformName': "'SBI_Stocks'"
        }
    }

    prices_mapping = {
        'Zerodha_Stock_Prices': {
            'PriceID': 'PriceID',
            'StockID': 'StockID',
            'Date': 'Date',
            'OpenPrice': 'OpenPrice',
            'ClosePrice': 'ClosePrice',
            'HighPrice': 'HighPrice',
            'LowPrice': 'LowPrice',
            'Volume': 'Volume',
            'LastUpdated': 'LastUpdated',
            'PlatformName': "'Zerodha'"
        },
        'Groww_Stock_Prices': {
            'PriceID': 'PriceID',
            'StockID': 'StockID',
            'Date': 'Date',
            'OpenPrice': 'Open',
            'ClosePrice': 'Close',
            'HighPrice': 'High',
            'LowPrice': 'Low',
            'Volume': 'Volume',
            'LastUpdated': 'LastUpdated',
            'PlatformName': "'Groww'"
        },
        'SBI_Stocks_Prices': {
            'PriceID': 'PriceID',
            'StockID': 'StockID',
            'Date': 'Date',
            'OpenPrice': 'Open_Price',
            'ClosePrice': 'Close_Price',
            'HighPrice': 'High_Price',
            'LowPrice': 'Low_Price',
            'Volume': 'Trade_Volume',
            'LastUpdated': 'LastUpdated',
            'PlatformName': "'SBI_Stocks'"
        }
    }

    # Define standard columns
    standard_clients_columns = [
        'ClientID',
        'ClientName',
        'Email',
        'PhoneNumber',
        'PAN',
        'Address',
        'DateOfBirth',
        'RegistrationDate',
        'PlatformName'
    ]

    standard_stocks_columns = [
        'StockID',
        'StockSymbol',
        'StockName',
        'Sector',
        'Exchange',
        'PlatformName'
    ]

    standard_orders_columns = [
        'OrderID',
        'ClientID',
        'StockID',
        'OrderType',
        'Quantity',
        'PricePerShare',
        'TotalAmount',
        'OrderDate',
        'OrderStatus',
        'PlatformName'
    ]

    standard_prices_columns = [
        'PriceID',
        'StockID',
        'Date',
        'OpenPrice',
        'ClosePrice',
        'HighPrice',
        'LowPrice',
        'Volume',
        'LastUpdated',
        'PlatformName'
    ]

    # Generate SELECT statements for Clients
    clients_select_statements = []
    for table in clients_mapping:
        stmt = generate_select_statement(table, clients_mapping, standard_clients_columns)
        clients_select_statements.append(stmt)

    # Generate SELECT statements for Stocks
    stocks_select_statements = []
    for table in stocks_mapping:
        stmt = generate_select_statement(table, stocks_mapping, standard_stocks_columns)
        stocks_select_statements.append(stmt)

    # Generate SELECT statements for Orders
    orders_select_statements = []
    for table in orders_mapping:
        stmt = generate_select_statement(table, orders_mapping, standard_orders_columns)
        orders_select_statements.append(stmt)

    # Generate SELECT statements for Prices
    prices_select_statements = []
    for table in prices_mapping:
        stmt = generate_select_statement(table, prices_mapping, standard_prices_columns)
        prices_select_statements.append(stmt)

    # Create Global Clients View
    create_view(cursor, 'Global_Stock_Clients', clients_select_statements)

    # Create Global Stocks View
    create_view(cursor, 'Global_Stocks', stocks_select_statements)

    # Create Global Orders View
    create_view(cursor, 'Global_Orders', orders_select_statements)

    # Create Global Stock Prices View
    create_view(cursor, 'Global_Stock_Prices', prices_select_statements)

    print("StockPlatforms Global Views created successfully.")

# Now run the functions to create views for each database
create_banks_views()
create_mutualfunds_views()
create_stockplatforms_views()

# Commit changes
cnx.commit()
print("Global Views created successfully.")

# Close cursor and connection
cursor.close()
cnx.close()
print("Connection closed.")
