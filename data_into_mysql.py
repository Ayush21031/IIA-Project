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

# List of databases to create
databases = ['Banks', 'MutualFunds', 'StockPlatforms']

# Dictionary to hold DataFrames for each database
dataframes = {}

# CSV files mapping for each database
csv_files = {
    'Banks': [
        'ICICI_Accounts.csv',
        'ICICI_Transactions.csv',
        'HDFC_Accounts.csv',
        'HDFC_Transactions.csv',
        'SBI_Accounts.csv',
        'SBI_Transactions.csv'
    ],
    'MutualFunds': [
        'MutualFunds.csv',
        'MutualFundRates.csv',
        'SBI_MF_Clients.csv',
        'SBI_MF_Returns.csv',
        'TataMF_Investors.csv',
        'TataMF_InvestmentReturns.csv',
        'BajajMF_Customers.csv',
        'BajajMF_ClientReturns.csv'
    ],
    'StockPlatforms': [
        'Zerodha_Clients.csv',
        'Zerodha_Stocks.csv',
        'Zerodha_Orders.csv',
        'Zerodha_Stock_Prices.csv',
        'Groww_Clients.csv',
        'Groww_Stocks.csv',
        'Groww_Orders.csv',
        'Groww_Stock_Prices.csv',
        'SBI_Stocks_Clients.csv',
        'SBI_Stocks_List.csv',
        'SBI_Stocks_Orders.csv',
        'SBI_Stocks_Prices.csv'
    ]
}

# Connect to MySQL server
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    print("Connected to MySQL server.")
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

# Create databases
for db_name in databases:
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' created or already exists.")
    except mysql.connector.Error as err:
        print(f"Failed creating database '{db_name}': {err}")
        exit(1)

# Function to read CSV files into DataFrames
def read_csv_files(db_name):
    db_dataframes = {}
    for file_name in csv_files[db_name]:
        try:
            df = pd.read_csv(file_name)
            db_dataframes[file_name] = df
            print(f"Loaded '{file_name}' into DataFrame.")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            exit(1)
    return db_dataframes

# Function to create tables and insert data for a given database
def setup_database(db_name):
    cursor.execute(f"USE {db_name}")
    print(f"Using database '{db_name}'.")
    
    db_dataframes = read_csv_files(db_name)
    
    if db_name == 'Banks':
        setup_banks(db_dataframes)
    elif db_name == 'MutualFunds':
        setup_mutual_funds(db_dataframes)
    elif db_name == 'StockPlatforms':
        setup_stock_platforms(db_dataframes)
    else:
        print(f"No setup function for database '{db_name}'.")

# Function to setup Banks database
def setup_banks(db_dataframes):
    # Create ICICI tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ICICI_Accounts (
            ICICI_AccountID INT PRIMARY KEY,
            CustomerName VARCHAR(100),
            AccountNumber VARCHAR(50),
            ServiceType VARCHAR(50),
            NationalID VARCHAR(20),
            Balance FLOAT,
            InterestRate FLOAT,
            LastUpdated DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ICICI_Transactions (
            TransactionID INT PRIMARY KEY,
            ICICI_AccountID INT,
            TransactionDate DATE,
            TransactionType VARCHAR(50),
            Amount FLOAT,
            Description VARCHAR(255),
            FOREIGN KEY (ICICI_AccountID) REFERENCES ICICI_Accounts(ICICI_AccountID)
        )
    """)
    # Insert data into ICICI tables
    insert_data_into_table(cursor, db_dataframes['ICICI_Accounts.csv'], 'ICICI_Accounts')
    insert_data_into_table(cursor, db_dataframes['ICICI_Transactions.csv'], 'ICICI_Transactions')
    
    # Create HDFC tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS HDFC_Accounts (
            HDFC_AccountID INT PRIMARY KEY,
            ClientName VARCHAR(100),
            AccNo VARCHAR(50),
            AccountType VARCHAR(50),
            GovtID VARCHAR(20),
            CurrentBalance FLOAT,
            MonthlyInterest FLOAT,
            LastUpdate DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS HDFC_Transactions (
            TransactionID INT PRIMARY KEY,
            HDFC_AccountID INT,
            TransDate DATE,
            Type VARCHAR(50),
            TransAmount FLOAT,
            Notes VARCHAR(255),
            FOREIGN KEY (HDFC_AccountID) REFERENCES HDFC_Accounts(HDFC_AccountID)
        )
    """)
    # Insert data into HDFC tables
    insert_data_into_table(cursor, db_dataframes['HDFC_Accounts.csv'], 'HDFC_Accounts')
    insert_data_into_table(cursor, db_dataframes['HDFC_Transactions.csv'], 'HDFC_Transactions')
    
    # Create SBI tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_Accounts (
            SBI_AccountID INT PRIMARY KEY,
            AccountHolder VARCHAR(100),
            Acc_Number VARCHAR(50),
            Service_Type VARCHAR(50),
            National_ID VARCHAR(20),
            AmountStored FLOAT,
            Interest_Rate FLOAT,
            Last_Updated DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_Transactions (
            TransactionID INT PRIMARY KEY,
            SBI_AccountID INT,
            Date DATE,
            Type_of_Transaction VARCHAR(50),
            Amount FLOAT,
            Details VARCHAR(255),
            FOREIGN KEY (SBI_AccountID) REFERENCES SBI_Accounts(SBI_AccountID)
        )
    """)
    # Insert data into SBI tables
    insert_data_into_table(cursor, db_dataframes['SBI_Accounts.csv'], 'SBI_Accounts')
    insert_data_into_table(cursor, db_dataframes['SBI_Transactions.csv'], 'SBI_Transactions')

    cnx.commit()
    print("Banks database setup completed.")

# Function to setup MutualFunds database
def setup_mutual_funds(db_dataframes):
    # Create MutualFunds and MutualFundRates tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MutualFunds (
            MutualFundID INT PRIMARY KEY,
            FundName VARCHAR(100),
            Category VARCHAR(50),
            RiskProfile VARCHAR(50),
            ManagerName VARCHAR(100)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MutualFundRates (
            RateID INT AUTO_INCREMENT PRIMARY KEY,
            MutualFundID INT,
            RateDate DATE,
            RatePerQuantity FLOAT,
            FOREIGN KEY (MutualFundID) REFERENCES MutualFunds(MutualFundID)
        )
    """)
    # Insert data into MutualFunds and MutualFundRates tables
    insert_data_into_table(cursor, db_dataframes['MutualFunds.csv'], 'MutualFunds')
    insert_data_into_table(cursor, db_dataframes['MutualFundRates.csv'], 'MutualFundRates', include_id=False)
    
    # Create SBI Mutual Fund tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_MF_Clients (
            SBI_ClientID INT PRIMARY KEY,
            FullName VARCHAR(100),
            ClientEmail VARCHAR(100),
            ContactNumber VARCHAR(50),
            PAN_Number VARCHAR(20),
            Address VARCHAR(255),
            DateOfBirth DATE,
            RegistrationDate DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_MF_Returns (
            ReturnID INT PRIMARY KEY,
            MutualFundID INT,
            SBI_ClientID INT,
            InvestmentDate DATE,
            UnitsPurchased FLOAT,
            InvestmentAmount FLOAT,
            PurchaseRate FLOAT,
            CurrentNAV FLOAT,
            CurrentValue FLOAT,
            ReturnPercentage FLOAT,
            LastUpdated DATE,
            FOREIGN KEY (MutualFundID) REFERENCES MutualFunds(MutualFundID),
            FOREIGN KEY (SBI_ClientID) REFERENCES SBI_MF_Clients(SBI_ClientID)
        )
    """)
    # Insert data into SBI Mutual Fund tables
    insert_data_into_table(cursor, db_dataframes['SBI_MF_Clients.csv'], 'SBI_MF_Clients')
    insert_data_into_table(cursor, db_dataframes['SBI_MF_Returns.csv'], 'SBI_MF_Returns')
    
    # Create Tata Mutual Fund tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TataMF_Investors (
            Tata_ClientID INT PRIMARY KEY,
            InvestorName VARCHAR(100),
            EmailAddress VARCHAR(100),
            PhoneNumber VARCHAR(50),
            PAN VARCHAR(20),
            ResidentialAddress VARCHAR(255),
            DOB DATE,
            JoinDate DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TataMF_InvestmentReturns (
            InvestmentReturnID INT PRIMARY KEY,
            MutualFundID INT,
            Tata_ClientID INT,
            DateOfInvestment DATE,
            UnitsBought FLOAT,
            InvestmentINR FLOAT,
            PurchaseRate FLOAT,
            CurrentNAVValue FLOAT,
            InvestmentValue FLOAT,
            GainLossPercentage FLOAT,
            LastUpdated DATE,
            FOREIGN KEY (MutualFundID) REFERENCES MutualFunds(MutualFundID),
            FOREIGN KEY (Tata_ClientID) REFERENCES TataMF_Investors(Tata_ClientID)
        )
    """)
    # Insert data into Tata Mutual Fund tables
    insert_data_into_table(cursor, db_dataframes['TataMF_Investors.csv'], 'TataMF_Investors')
    insert_data_into_table(cursor, db_dataframes['TataMF_InvestmentReturns.csv'], 'TataMF_InvestmentReturns')
    
    # Create Bajaj Mutual Fund tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BajajMF_Customers (
            Bajaj_CustomerID INT PRIMARY KEY,
            Name VARCHAR(100),
            Email VARCHAR(100),
            Mobile VARCHAR(50),
            PAN_Num VARCHAR(20),
            Addr VARCHAR(255),
            DOB DATE,
            DateJoined DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BajajMF_ClientReturns (
            ClientReturnID INT PRIMARY KEY,
            MutualFundID INT,
            Bajaj_CustomerID INT,
            InvestmentDate DATE,
            UnitsPurchased FLOAT,
            AmountInvested FLOAT,
            PurchaseRate FLOAT,
            CurrentNAV FLOAT,
            CurrentValue FLOAT,
            ProfitLossPerc FLOAT,
            UpdateDate DATE,
            FOREIGN KEY (MutualFundID) REFERENCES MutualFunds(MutualFundID),
            FOREIGN KEY (Bajaj_CustomerID) REFERENCES BajajMF_Customers(Bajaj_CustomerID)
        )
    """)
    # Insert data into Bajaj Mutual Fund tables
    insert_data_into_table(cursor, db_dataframes['BajajMF_Customers.csv'], 'BajajMF_Customers')
    insert_data_into_table(cursor, db_dataframes['BajajMF_ClientReturns.csv'], 'BajajMF_ClientReturns')

    cnx.commit()
    print("MutualFunds database setup completed.")


def setup_stock_platforms(db_dataframes):
    # Create Zerodha tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Zerodha_Clients (
            Zerodha_ClientID INT PRIMARY KEY,
            ClientName VARCHAR(100),
            Email VARCHAR(100),
            PhoneNumber VARCHAR(50),
            PAN VARCHAR(20),
            Address VARCHAR(255),
            DateOfBirth DATE,
            AccountCreationDate DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Zerodha_Stocks (
            Zerodha_StockID INT PRIMARY KEY,
            StockSymbol VARCHAR(10),
            StockName VARCHAR(100),
            Sector VARCHAR(50),
            Exchange VARCHAR(10)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Zerodha_Orders (
            OrderID INT PRIMARY KEY,
            ClientID INT,
            StockID INT,
            OrderType VARCHAR(10),
            Quantity INT,
            PricePerShare FLOAT,
            TotalAmount FLOAT,
            OrderDate DATETIME,
            OrderStatus VARCHAR(20),
            FOREIGN KEY (ClientID) REFERENCES Zerodha_Clients(Zerodha_ClientID),
            FOREIGN KEY (StockID) REFERENCES Zerodha_Stocks(Zerodha_StockID)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Zerodha_Stock_Prices (
            PriceID INT AUTO_INCREMENT PRIMARY KEY,
            StockID INT,
            Date DATE,
            OpenPrice FLOAT,
            ClosePrice FLOAT,
            HighPrice FLOAT,
            LowPrice FLOAT,
            Volume INT,
            LastUpdated DATETIME,
            FOREIGN KEY (StockID) REFERENCES Zerodha_Stocks(Zerodha_StockID)
        )
    """)
    # Insert data into Zerodha tables
    insert_data_into_table(cursor, db_dataframes['Zerodha_Clients.csv'], 'Zerodha_Clients')
    insert_data_into_table(cursor, db_dataframes['Zerodha_Stocks.csv'], 'Zerodha_Stocks')
    insert_data_into_table(cursor, db_dataframes['Zerodha_Orders.csv'], 'Zerodha_Orders')
    
    # Insert Stock_Prices with include_id=True
    zerodha_prices_df = db_dataframes['Zerodha_Stock_Prices.csv']
    print("Zerodha_Stock_Prices DataFrame columns:", zerodha_prices_df.columns)
    print("Zerodha_Stock_Prices DataFrame sample:", zerodha_prices_df.head())
    print("Zerodha_Stock_Prices 'StockID' null count:", zerodha_prices_df['StockID'].isnull().sum())
    insert_data_into_table(cursor, zerodha_prices_df, 'Zerodha_Stock_Prices', include_id=True)
    
    # Create Groww tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Groww_Clients (
            Groww_ClientID INT PRIMARY KEY,
            ClientName VARCHAR(100),
            Email VARCHAR(100),
            PhoneNumber VARCHAR(50),
            PAN VARCHAR(20),
            Address VARCHAR(255),
            DateOfBirth DATE,
            AccountCreationDate DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Groww_Stocks (
            Groww_StockID INT PRIMARY KEY,
            Symbol VARCHAR(10),
            Name VARCHAR(100),
            Sector VARCHAR(50),
            Exchange VARCHAR(10)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Groww_Orders (
            OrderID INT PRIMARY KEY,
            ClientID INT,
            StockID INT,
            Type VARCHAR(10),
            Quantity INT,
            Price FLOAT,
            TotalValue FLOAT,
            Timestamp DATETIME,
            Status VARCHAR(20),
            FOREIGN KEY (ClientID) REFERENCES Groww_Clients(Groww_ClientID),
            FOREIGN KEY (StockID) REFERENCES Groww_Stocks(Groww_StockID)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Groww_Stock_Prices (
            PriceID INT AUTO_INCREMENT PRIMARY KEY,
            StockID INT,
            Date DATE,
            Open FLOAT,
            Close FLOAT,
            High FLOAT,
            Low FLOAT,
            Volume INT,
            LastUpdated DATETIME,
            FOREIGN KEY (StockID) REFERENCES Groww_Stocks(Groww_StockID)
        )
    """)
    # Insert data into Groww tables
    insert_data_into_table(cursor, db_dataframes['Groww_Clients.csv'], 'Groww_Clients')
    insert_data_into_table(cursor, db_dataframes['Groww_Stocks.csv'], 'Groww_Stocks')
    insert_data_into_table(cursor, db_dataframes['Groww_Orders.csv'], 'Groww_Orders')
    
    # Insert Stock_Prices with include_id=True
    groww_prices_df = db_dataframes['Groww_Stock_Prices.csv']
    print("Groww_Stock_Prices DataFrame columns:", groww_prices_df.columns)
    print("Groww_Stock_Prices DataFrame sample:", groww_prices_df.head())
    print("Groww_Stock_Prices 'StockID' null count:", groww_prices_df['StockID'].isnull().sum())
    insert_data_into_table(cursor, groww_prices_df, 'Groww_Stock_Prices', include_id=True)
    
    # Create SBI_Stocks tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_Stocks_Clients (
            SBI_ClientID INT PRIMARY KEY,
            ClientName VARCHAR(100),
            Email VARCHAR(100),
            PhoneNumber VARCHAR(50),
            PAN VARCHAR(20),
            Address VARCHAR(255),
            DateOfBirth DATE,
            AccountStartDate DATE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_Stocks_List (
            SBI_StockID INT PRIMARY KEY,
            StockCode VARCHAR(10),
            StockName VARCHAR(100),
            Sector VARCHAR(50),
            Exchange VARCHAR(10)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_Stocks_Orders (
            OrderID INT PRIMARY KEY,
            ClientID INT,
            StockID INT,
            TradeType VARCHAR(10),
            Quantity INT,
            PricePerShare FLOAT,
            TotalValue FLOAT,
            TradeTimestamp DATETIME,
            TradeStatus VARCHAR(20),
            FOREIGN KEY (ClientID) REFERENCES SBI_Stocks_Clients(SBI_ClientID),
            FOREIGN KEY (StockID) REFERENCES SBI_Stocks_List(SBI_StockID)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SBI_Stocks_Prices (
            PriceID INT AUTO_INCREMENT PRIMARY KEY,
            StockID INT,
            Date DATE,
            Open_Price FLOAT,
            Close_Price FLOAT,
            High_Price FLOAT,
            Low_Price FLOAT,
            Trade_Volume INT,
            LastUpdated DATETIME,
            FOREIGN KEY (StockID) REFERENCES SBI_Stocks_List(SBI_StockID)
        )
    """)
    # Insert data into SBI_Stocks tables
    insert_data_into_table(cursor, db_dataframes['SBI_Stocks_Clients.csv'], 'SBI_Stocks_Clients')
    insert_data_into_table(cursor, db_dataframes['SBI_Stocks_List.csv'], 'SBI_Stocks_List')
    insert_data_into_table(cursor, db_dataframes['SBI_Stocks_Orders.csv'], 'SBI_Stocks_Orders')
    
    # Insert Stock_Prices with include_id=True
    sbi_prices_df = db_dataframes['SBI_Stocks_Prices.csv']
    print("SBI_Stocks_Prices DataFrame columns:", sbi_prices_df.columns)
    print("SBI_Stocks_Prices DataFrame sample:", sbi_prices_df.head())
    print("SBI_Stocks_Prices 'StockID' null count:", sbi_prices_df['StockID'].isnull().sum())
    insert_data_into_table(cursor, sbi_prices_df, 'SBI_Stocks_Prices', include_id=True)

    cnx.commit()
    print("StockPlatforms database setup completed.")


# Function to insert data into a table
def insert_data_into_table(cursor, df, table_name, include_id=True):
    # Prepare column names and placeholders
    columns = df.columns.tolist()
    if not include_id:
        columns = columns[1:]  # Skip the first column (auto-increment ID)
    placeholders = ', '.join(['%s'] * len(columns))
    columns_formatted = ', '.join(columns)
    insert_stmt = f"INSERT INTO {table_name} ({columns_formatted}) VALUES ({placeholders})"
    data_tuples = df[columns].apply(tuple, axis=1).tolist()
    cursor.executemany(insert_stmt, data_tuples)
    print(f"Inserted data into '{table_name}'.")

# Setup each database
for db_name in databases:
    setup_database(db_name)

# Close cursor and connection
cursor.close()
cnx.close()
print("Data insertion completed and connection closed.")
