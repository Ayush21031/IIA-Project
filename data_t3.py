import pandas as pd
from faker import Faker
import random
import string

# Initialize Faker
fake = Faker('en_IN')  # Using Indian locale for realistic data

# Set seed for reproducibility
Faker.seed(0)
random.seed(0)

# Number of unique individuals
NUM_UNIQUE_PERSONS = 100

# Function to generate a full name with first, middle, and last names
def generate_full_name():
    first_name = fake.first_name()
    middle_name = fake.first_name()
    last_name = fake.last_name()
    full_name = f"{first_name} {middle_name} {last_name}"
    return full_name, first_name, middle_name, last_name

# Function to generate name variations
def generate_name_variations(first_name, middle_name, last_name):
    """
    Generate different variations of a full name.
    E.g., "Ramesh Kumar Singh" -> ["Ramesh Kumar Singh", "RK Singh", "Ramesh K Singh", "Ramkesh K Singh"]
    """
    variations = []
    # Full name
    full_name = f"{first_name} {middle_name} {last_name}"
    variations.append(full_name)
    # Initials version
    initials = f"{first_name[0]}{middle_name[0]} {last_name}"
    variations.append(initials)
    # Middle initial version
    middle_initial = f"{first_name} {middle_name[0]} {last_name}"
    variations.append(middle_initial)
    # Alternate first name (e.g., slight misspelling)
    if len(first_name) > 1:
        alternate_first_name = first_name[:-1] + random.choice(string.ascii_lowercase)
    else:
        alternate_first_name = first_name + random.choice(string.ascii_lowercase)
    alternate_name = f"{alternate_first_name} {middle_name} {last_name}"
    variations.append(alternate_name)
    return variations

# Generate unique individuals
unique_persons = []

for _ in range(NUM_UNIQUE_PERSONS):
    full_name, first_name, middle_name, last_name = generate_full_name()
    name_variations = generate_name_variations(first_name, middle_name, last_name)
    pan = fake.unique.bothify(text='??######?').upper()  # PAN format: 5 letters, 4 digits, 1 letter
    national_id = fake.unique.bothify(text='###########')  # Assuming an 11-digit ID
    email = fake.unique.email()
    phone = fake.unique.phone_number()
    address = fake.address().replace('\n', ', ')
    dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
    account_creation_date = fake.date_between(start_date='-10y', end_date='today')

    unique_persons.append({
        'FullName': full_name,
        'FirstName': first_name,
        'MiddleName': middle_name,
        'LastName': last_name,
        'NameVariations': name_variations,
        'PAN': pan,
        'NationalID': national_id,
        'Email': email,
        'Phone': phone,
        'Address': address,
        'DateOfBirth': dob,
        'AccountCreationDate': account_creation_date
    })

# Assign mutual funds and stock platform investments per person
# Each person can invest in 0 to 3 mutual funds and 0 to 3 stock platforms
mutual_funds = ['SBI', 'Tata', 'Bajaj']
stock_platforms = ['Zerodha', 'Groww', 'SBI_Stocks']
all_platforms = mutual_funds + stock_platforms
person_investments = []

for person in unique_persons:
    pan = person['PAN']
    national_id = person['NationalID']
    # Randomly decide number of mutual fund investments
    num_mf_investments = random.choice([0, 1, 2, 3])
    invested_mfs = random.sample(mutual_funds, num_mf_investments) if num_mf_investments > 0 else []
    
    # Randomly decide number of stock platform investments
    num_stock_investments = random.choice([0, 1, 2, 3])
    invested_stocks = random.sample(stock_platforms, num_stock_investments) if num_stock_investments > 0 else []
    
    # Assign name variations for each mutual fund and stock platform
    fund_name_variations = {}
    for fund in invested_mfs:
        variation_index = mutual_funds.index(fund) % len(person['NameVariations'])
        name_variation = person['NameVariations'][variation_index]
        fund_name_variations[fund] = name_variation
    
    stock_name_variations = {}
    for platform in invested_stocks:
        variation_index = stock_platforms.index(platform) % len(person['NameVariations'])
        name_variation = person['NameVariations'][variation_index]
        stock_name_variations[platform] = name_variation
    
    person_investments.append({
        'PAN': pan,
        'NationalID': national_id,
        'MutualFunds': fund_name_variations,
        'StockPlatforms': stock_name_variations
    })

# Initialize the mapping dictionary before mutual funds data generation
person_name_variations_mapping = {}

# Create MutualFunds DataFrame
mutual_funds_data = [
    {'MutualFundID': 1, 'FundName': 'SBI Mutual Fund', 'Category': 'Equity', 'RiskProfile': 'Medium', 'ManagerName': fake.name()},
    {'MutualFundID': 2, 'FundName': 'Tata Mutual Fund', 'Category': 'Debt', 'RiskProfile': 'Low', 'ManagerName': fake.name()},
    {'MutualFundID': 3, 'FundName': 'Bajaj Mutual Fund', 'Category': 'Hybrid', 'RiskProfile': 'High', 'ManagerName': fake.name()}
]
mutual_funds_df = pd.DataFrame(mutual_funds_data)

# Generate MutualFundRates DataFrame
# For simplicity, generate 10 rate updates per mutual fund
mutual_fund_rates = []
for fund in mutual_funds_data:
    mutual_fund_id = fund['MutualFundID']
    for _ in range(10):
        rate_date = fake.date_between(start_date='-5y', end_date='today')
        rate_per_quantity = round(random.uniform(50.0, 500.0), 4)
        mutual_fund_rates.append({
            'MutualFundID': mutual_fund_id,
            'RateDate': rate_date,
            'RatePerQuantity': rate_per_quantity
        })
mutual_fund_rates_df = pd.DataFrame(mutual_fund_rates)

# Sort MutualFundRates by MutualFundID and RateDate
mutual_fund_rates_df.sort_values(by=['MutualFundID', 'RateDate'], inplace=True)
mutual_fund_rates_df.reset_index(drop=True, inplace=True)

# Initialize lists for mutual funds clients and investment returns
sbi_mf_clients = []
tata_mf_investors = []
bajaj_mf_customers = []

sbi_mf_returns = []
tata_mf_investment_returns = []
bajaj_mf_client_returns = []

# Initialize lists for stock platforms
zerodha_clients = []
groww_clients = []
sbi_stocks_clients = []

zerodha_orders = []
groww_orders = []
sbi_stocks_orders = []

zerodha_stock_prices = []
groww_stock_prices = []
sbi_stocks_prices = []

# Stock Lists Generation Parameters
num_stocks_per_platform = 50  # Number of unique stocks per platform

# Function to generate unique stock symbols
def generate_stock_symbol(existing_symbols):
    while True:
        symbol = ''.join(random.choices(string.ascii_uppercase, k=4))
        if symbol not in existing_symbols:
            return symbol

# Generate Stocks for each platform
def generate_stocks(platform, num_stocks):
    stocks = []
    existing_symbols = set()
    for _ in range(num_stocks):
        symbol = generate_stock_symbol(existing_symbols)
        existing_symbols.add(symbol)
        stock_name = fake.company()
        sector = random.choice(['Technology', 'Healthcare', 'Finance', 'Energy', 'Consumer Goods', 'Utilities', 'Industrials'])
        exchange = random.choice(['NSE', 'BSE'])
        stocks.append({
            'Symbol': symbol,
            'Name': stock_name,
            'Sector': sector,
            'Exchange': exchange
        })
    return stocks

# Generate Stocks for Zerodha
zerodha_stocks_data = generate_stocks('Zerodha', num_stocks_per_platform)
zerodha_stocks_df = pd.DataFrame(zerodha_stocks_data)
zerodha_stocks_df.rename(columns={'Symbol': 'StockSymbol', 'Name': 'StockName'}, inplace=True)
zerodha_stocks_df['Zerodha_StockID'] = range(1, len(zerodha_stocks_df) + 1)

# Generate Stocks for Groww
groww_stocks_data = generate_stocks('Groww', num_stocks_per_platform)
groww_stocks_df = pd.DataFrame(groww_stocks_data)
groww_stocks_df.rename(columns={'Symbol': 'Symbol', 'Name': 'Name'}, inplace=True)
groww_stocks_df['Groww_StockID'] = range(1, len(groww_stocks_df) + 1)

# Generate Stocks for SBI_Stocks
sbi_stocks_data = generate_stocks('SBI_Stocks', num_stocks_per_platform)
sbi_stocks_df = pd.DataFrame(sbi_stocks_data)
sbi_stocks_df.rename(columns={'Symbol': 'StockCode', 'Name': 'StockName'}, inplace=True)
sbi_stocks_df['SBI_StockID'] = range(1, len(sbi_stocks_df) + 1)

# Function to generate clients for stock platforms
def generate_stock_clients(platform, platform_clients_list, person_investments, client_id_col, name_col, email_col, phone_col, pan_col, address_col, dob_col, account_date_col):
    """
    Generates clients for a given stock platform based on person investments.
    """
    for investment in person_investments:
        pan = investment['PAN']
        if platform in investment['StockPlatforms']:
            name_variation = investment['StockPlatforms'][platform]
            # Find the person
            person = next((p for p in unique_persons if p['PAN'] == pan), None)
            if person:
                client = {
                    'ClientName': name_variation,
                    'Email': fake.unique.email(),
                    'PhoneNumber': fake.phone_number(),
                    'PAN': pan,
                    'Address': person['Address'],
                    'DateOfBirth': person['DateOfBirth'],
                    'AccountCreationDate': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
                }
                platform_clients_list.append(client)
    return pd.DataFrame(platform_clients_list)

# Generate Zerodha Clients
zerodha_clients_df = generate_stock_clients(
    platform='Zerodha',
    platform_clients_list=zerodha_clients,
    person_investments=person_investments,
    client_id_col='Zerodha_ClientID',
    name_col='ClientName',
    email_col='Email',
    phone_col='PhoneNumber',
    pan_col='PAN',
    address_col='Address',
    dob_col='DateOfBirth',
    account_date_col='AccountCreationDate'
)
zerodha_clients_df.insert(0, 'Zerodha_ClientID', range(1, len(zerodha_clients_df) + 1))

# Generate Groww Clients
groww_clients_df = generate_stock_clients(
    platform='Groww',
    platform_clients_list=groww_clients,
    person_investments=person_investments,
    client_id_col='Groww_ClientID',
    name_col='ClientName',
    email_col='Email',
    phone_col='PhoneNumber',
    pan_col='PAN',
    address_col='Address',
    dob_col='DateOfBirth',
    account_date_col='AccountCreationDate'
)
groww_clients_df.insert(0, 'Groww_ClientID', range(1, len(groww_clients_df) + 1))

# Generate SBI_Stocks Clients
sbi_stocks_clients_df = generate_stock_clients(
    platform='SBI_Stocks',
    platform_clients_list=sbi_stocks_clients,
    person_investments=person_investments,
    client_id_col='SBI_ClientID',
    name_col='ClientName',
    email_col='Email',
    phone_col='PhoneNumber',
    pan_col='PAN',
    address_col='Address',
    dob_col='DateOfBirth',
    account_date_col='AccountStartDate'
)
sbi_stocks_clients_df.insert(0, 'SBI_ClientID', range(1, len(sbi_stocks_clients_df) + 1))

# Function to generate orders for stock platforms
def generate_stock_orders(platform, clients_df, stocks_df, orders_list, client_id_col, stock_id_col, order_type_col, quantity_col, price_col, total_col, order_date_col, status_col):
    """
    Generates orders for a given stock platform.
    """
    for _, client in clients_df.iterrows():
        # Random number of orders per client
        num_orders = random.randint(1, 10)
        for _ in range(num_orders):
            stock = stocks_df.sample(1).iloc[0]
            order_type = random.choice(['Buy', 'Sell'])
            quantity = random.randint(1, 1000)
            # Determine price per share based on latest stock price
            # For simplicity, generate a random price
            price_per_share = round(random.uniform(50.0, 5000.0), 2)
            total_amount = round(quantity * price_per_share, 2)
            order_date = fake.date_time_between(start_date='-1y', end_date='now')
            status = random.choice(['Pending', 'Completed', 'Cancelled'])
            
            if platform == 'Groww':
                order = {
                    'ClientID': client[client_id_col],
                    'StockID': stock[stock_id_col],
                    'Type': order_type,  # Column name differs for Groww
                    'Quantity': quantity,
                    'Price': price_per_share,  # Column name differs for Groww
                    'TotalValue': total_amount,  # Column name differs for Groww
                    'Timestamp': order_date,  # Column name differs for Groww
                    'Status': status  # Column name differs for Groww
                }
            elif platform == 'SBI_Stocks':
                order = {
                    'ClientID': client[client_id_col],
                    'StockID': stock[stock_id_col],
                    'TradeType': order_type,  # Column name differs for SBI_Stocks
                    'Quantity': quantity,
                    'PricePerShare': price_per_share,  # Column name differs for SBI_Stocks
                    'TotalValue': total_amount,  # Column name differs for SBI_Stocks
                    'TradeTimestamp': order_date,  # Column name differs for SBI_Stocks
                    'TradeStatus': status  # Column name differs for SBI_Stocks
                }
            else:
                order = {
                    'ClientID': client[client_id_col],
                    'StockID': stock[stock_id_col],
                    'OrderType': order_type,
                    'Quantity': quantity,
                    'PricePerShare': price_per_share,
                    'TotalAmount': total_amount,
                    'OrderDate': order_date,
                    'OrderStatus': status
                }
            orders_list.append(order)
    return

# Generate Zerodha Orders
generate_stock_orders(
    platform='Zerodha',
    clients_df=zerodha_clients_df,
    stocks_df=zerodha_stocks_df,
    orders_list=zerodha_orders,
    client_id_col='Zerodha_ClientID',
    stock_id_col='Zerodha_StockID',
    order_type_col='OrderType',
    quantity_col='Quantity',
    price_col='PricePerShare',
    total_col='TotalAmount',
    order_date_col='OrderDate',
    status_col='OrderStatus'
)
zerodha_orders_df = pd.DataFrame(zerodha_orders)
zerodha_orders_df.insert(0, 'OrderID', range(1, len(zerodha_orders_df) + 1))

# Generate Groww Orders
generate_stock_orders(
    platform='Groww',
    clients_df=groww_clients_df,
    stocks_df=groww_stocks_df,
    orders_list=groww_orders,
    client_id_col='Groww_ClientID',
    stock_id_col='Groww_StockID',
    order_type_col='Type',
    quantity_col='Quantity',
    price_col='Price',
    total_col='TotalValue',
    order_date_col='Timestamp',
    status_col='Status'
)
groww_orders_df = pd.DataFrame(groww_orders)
groww_orders_df.insert(0, 'OrderID', range(1, len(groww_orders_df) + 1))

# Generate SBI_Stocks Orders
generate_stock_orders(
    platform='SBI_Stocks',
    clients_df=sbi_stocks_clients_df,
    stocks_df=sbi_stocks_df,
    orders_list=sbi_stocks_orders,
    client_id_col='SBI_ClientID',
    stock_id_col='SBI_StockID',
    order_type_col='TradeType',
    quantity_col='Quantity',
    price_col='PricePerShare',
    total_col='TotalValue',
    order_date_col='TradeTimestamp',
    status_col='TradeStatus'
)
sbi_stocks_orders_df = pd.DataFrame(sbi_stocks_orders)
sbi_stocks_orders_df.insert(0, 'OrderID', range(1, len(sbi_stocks_orders_df) + 1))

# Function to generate stock prices for stock platforms
def generate_stock_prices(platform, stocks_df, prices_list, stock_id_col, price_id_col):
    """
    Generates daily stock prices for each stock in a platform.
    """
    for _, stock in stocks_df.iterrows():
        # Generate prices for the last 365 days
        for day_offset in range(365):
            date = fake.date_between(start_date='-1y', end_date='today')
            open_price = round(random.uniform(50.0, 5000.0), 2)
            close_price = round(random.uniform(50.0, 5000.0), 2)
            high_price = max(open_price, close_price) + round(random.uniform(0.0, 100.0), 2)
            low_price = min(open_price, close_price) - round(random.uniform(0.0, 100.0), 2)
            volume = random.randint(1000, 1000000)
            last_updated = fake.date_time_between(start_date=date, end_date='now')
            
            if platform == 'Zerodha':
                price = {
                    'StockID': stock[stock_id_col],
                    'Date': date,
                    'OpenPrice': open_price,
                    'ClosePrice': close_price,
                    'HighPrice': high_price,
                    'LowPrice': low_price,
                    'Volume': volume,
                    'LastUpdated': last_updated
                }
            elif platform == 'Groww':
                price = {
                    'StockID': stock[stock_id_col],
                    'Date': date,
                    'Open': open_price,
                    'Close': close_price,
                    'High': high_price,
                    'Low': low_price,
                    'Volume': volume,
                    'LastUpdated': last_updated
                }
            elif platform == 'SBI_Stocks':
                price = {
                    'StockID': stock[stock_id_col],
                    'Date': date,
                    'Open_Price': open_price,
                    'Close_Price': close_price,
                    'High_Price': high_price,
                    'Low_Price': low_price,
                    'Trade_Volume': volume,
                    'LastUpdated': last_updated
                }
            prices_list.append(price)
    return

# Generate Zerodha Stock Prices
generate_stock_prices(
    platform='Zerodha',
    stocks_df=zerodha_stocks_df,
    prices_list=zerodha_stock_prices,
    stock_id_col='Zerodha_StockID',
    price_id_col='PriceID'
)
zerodha_stock_prices_df = pd.DataFrame(zerodha_stock_prices)

# Generate Groww Stock Prices
generate_stock_prices(
    platform='Groww',
    stocks_df=groww_stocks_df,
    prices_list=groww_stock_prices,
    stock_id_col='Groww_StockID',
    price_id_col='PriceID'
)
groww_stock_prices_df = pd.DataFrame(groww_stock_prices)

# Generate SBI_Stocks Stock Prices
generate_stock_prices(
    platform='SBI_Stocks',
    stocks_df=sbi_stocks_df,
    prices_list=sbi_stocks_prices,
    stock_id_col='SBI_StockID',
    price_id_col='PriceID'
)
sbi_stocks_prices_df = pd.DataFrame(sbi_stocks_prices)

# -------------------- Mutual Funds Data Generation --------------------

# Client ID counters
sbi_client_id_counter = 1
tata_client_id_counter = 1
bajaj_customer_id_counter = 1

# Iterate through each person's mutual fund investments
for person_funds in person_investments:
    pan = person_funds['PAN']
    national_id = person_funds['NationalID']
    invested_funds = person_funds['MutualFunds']
    
    # Find the person in unique_persons list
    person = next((p for p in unique_persons if p['PAN'] == pan and p['NationalID'] == national_id), None)
    if person is None:
        continue  # Skip if person not found
    
    # Initialize mapping if not already
    if pan not in person_name_variations_mapping:
        person_name_variations_mapping[pan] = {
            'FullName': person['FullName'],
            'NameVariations': person['NameVariations'],
            'MutualFunds': {},
            'StockPlatforms': {}
        }
    
    for fund, name_variation in invested_funds.items():
        # Get MutualFundID
        fund_id = mutual_funds_df[mutual_funds_df['FundName'] == f"{fund} Mutual Fund"]['MutualFundID'].values[0]
        
        # Store investment in mapping
        person_name_variations_mapping[pan]['MutualFunds'][fund] = name_variation
        
        # Prepare client data based on mutual fund
        if fund == 'SBI':
            client = {
                'SBI_ClientID': sbi_client_id_counter,
                'FullName': name_variation,
                'ClientEmail': fake.unique.email(),
                'ContactNumber': fake.phone_number(),
                'PAN_Number': pan,
                'Address': person['Address'],
                'DateOfBirth': person['DateOfBirth'],
                'RegistrationDate': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
            }
            sbi_mf_clients.append(client)
            current_client_id = sbi_client_id_counter
            sbi_client_id_counter += 1
            
            # Generate investment returns
            # Get the latest rate before investment date
            investment_date = fake.date_between(start_date='-5y', end_date='today')
            rates_before = mutual_fund_rates_df[
                (mutual_fund_rates_df['MutualFundID'] == fund_id) &
                (mutual_fund_rates_df['RateDate'] <= investment_date)
            ].sort_values(by='RateDate', ascending=False)
            if not rates_before.empty:
                purchase_rate = rates_before.iloc[0]['RatePerQuantity']
            else:
                purchase_rate = round(random.uniform(50.0, 500.0), 4)  # Default rate if no prior rate
            units_purchased = round(random.uniform(10.0, 1000.0), 4)
            investment_amount = round(units_purchased * purchase_rate, 2)
            # Current NAV is the latest rate
            current_nav = mutual_fund_rates_df[
                mutual_fund_rates_df['MutualFundID'] == fund_id
            ]['RatePerQuantity'].max()
            current_value = round(units_purchased * current_nav, 2)
            return_percentage = round(((current_value - investment_amount) / investment_amount) * 100, 2)
            last_updated = fake.date_between(start_date=investment_date, end_date='today')
            
            investment = {
                'ReturnID': len(sbi_mf_returns) + 1,
                'MutualFundID': fund_id,
                'SBI_ClientID': current_client_id,
                'InvestmentDate': investment_date,
                'UnitsPurchased': units_purchased,
                'InvestmentAmount': investment_amount,
                'PurchaseRate': purchase_rate,
                'CurrentNAV': current_nav,
                'CurrentValue': current_value,
                'ReturnPercentage': return_percentage,
                'LastUpdated': last_updated
            }
            sbi_mf_returns.append(investment)
        
        elif fund == 'Tata':
            client = {
                'Tata_ClientID': tata_client_id_counter,
                'InvestorName': name_variation,
                'EmailAddress': fake.unique.email(),
                'PhoneNumber': fake.phone_number(),
                'PAN': pan,
                'ResidentialAddress': person['Address'],
                'DOB': person['DateOfBirth'],
                'JoinDate': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
            }
            tata_mf_investors.append(client)
            current_client_id = tata_client_id_counter
            tata_client_id_counter += 1
            
            # Generate investment returns
            investment_date = fake.date_between(start_date='-5y', end_date='today')
            rates_before = mutual_fund_rates_df[
                (mutual_fund_rates_df['MutualFundID'] == fund_id) &
                (mutual_fund_rates_df['RateDate'] <= investment_date)
            ].sort_values(by='RateDate', ascending=False)
            if not rates_before.empty:
                purchase_rate = rates_before.iloc[0]['RatePerQuantity']
            else:
                purchase_rate = round(random.uniform(50.0, 500.0), 4)
            units_bought = round(random.uniform(10.0, 1000.0), 4)
            investment_inr = round(units_bought * purchase_rate, 2)
            current_nav = mutual_fund_rates_df[
                mutual_fund_rates_df['MutualFundID'] == fund_id
            ]['RatePerQuantity'].max()
            investment_value = round(units_bought * current_nav, 2)
            gain_loss_percentage = round(((investment_value - investment_inr) / investment_inr) * 100, 2)
            last_updated = fake.date_between(start_date=investment_date, end_date='today')
            
            investment = {
                'InvestmentReturnID': len(tata_mf_investment_returns) + 1,
                'MutualFundID': fund_id,
                'Tata_ClientID': current_client_id,
                'DateOfInvestment': investment_date,
                'UnitsBought': units_bought,
                'InvestmentINR': investment_inr,
                'PurchaseRate': purchase_rate,
                'CurrentNAVValue': current_nav,
                'InvestmentValue': investment_value,
                'GainLossPercentage': gain_loss_percentage,
                'LastUpdated': last_updated
            }
            tata_mf_investment_returns.append(investment)
        
        elif fund == 'Bajaj':
            client = {
                'Bajaj_CustomerID': bajaj_customer_id_counter,
                'Name': name_variation,
                'Email': fake.unique.email(),
                'Mobile': fake.phone_number(),
                'PAN_Num': pan,
                'Addr': person['Address'],
                'DOB': person['DateOfBirth'],
                'DateJoined': fake.date_between(start_date='-10y', end_date='today')
            }
            bajaj_mf_customers.append(client)
            current_customer_id = bajaj_customer_id_counter
            bajaj_customer_id_counter += 1
            
            # Generate investment returns
            investment_date = fake.date_between(start_date='-5y', end_date='today')
            rates_before = mutual_fund_rates_df[
                (mutual_fund_rates_df['MutualFundID'] == fund_id) &
                (mutual_fund_rates_df['RateDate'] <= investment_date)
            ].sort_values(by='RateDate', ascending=False)
            if not rates_before.empty:
                purchase_rate = rates_before.iloc[0]['RatePerQuantity']
            else:
                purchase_rate = round(random.uniform(50.0, 500.0), 4)
            units_purchased = round(random.uniform(10.0, 1000.0), 4)
            amount_invested = round(units_purchased * purchase_rate, 2)
            current_nav = mutual_fund_rates_df[
                mutual_fund_rates_df['MutualFundID'] == fund_id
            ]['RatePerQuantity'].max()
            current_value = round(units_purchased * current_nav, 2)
            profit_loss_perc = round(((current_value - amount_invested) / amount_invested) * 100, 2)
            update_date = fake.date_between(start_date=investment_date, end_date='today')
            
            investment = {
                'ClientReturnID': len(bajaj_mf_client_returns) + 1,
                'MutualFundID': fund_id,
                'Bajaj_CustomerID': current_customer_id,
                'InvestmentDate': investment_date,
                'UnitsPurchased': units_purchased,
                'AmountInvested': amount_invested,
                'PurchaseRate': purchase_rate,
                'CurrentNAV': current_nav,
                'CurrentValue': current_value,
                'ProfitLossPerc': profit_loss_perc,
                'UpdateDate': update_date
            }
            bajaj_mf_client_returns.append(investment)

# Convert mutual funds clients and investments lists to DataFrames
sbi_mf_clients_df = pd.DataFrame(sbi_mf_clients)
tata_mf_investors_df = pd.DataFrame(tata_mf_investors)
bajaj_mf_customers_df = pd.DataFrame(bajaj_mf_customers)

sbi_mf_returns_df = pd.DataFrame(sbi_mf_returns)
tata_mf_investment_returns_df = pd.DataFrame(tata_mf_investment_returns)
bajaj_mf_client_returns_df = pd.DataFrame(bajaj_mf_client_returns)

# Save mutual funds data to CSV files
sbi_mf_clients_df.to_csv('SBI_MF_Clients.csv', index=False)
tata_mf_investors_df.to_csv('TataMF_Investors.csv', index=False)
bajaj_mf_customers_df.to_csv('BajajMF_Customers.csv', index=False)

sbi_mf_returns_df.to_csv('SBI_MF_Returns.csv', index=False)
tata_mf_investment_returns_df.to_csv('TataMF_InvestmentReturns.csv', index=False)
bajaj_mf_client_returns_df.to_csv('BajajMF_ClientReturns.csv', index=False)

# Save mutual funds master data to CSV
mutual_funds_df.to_csv('MutualFunds.csv', index=False)
mutual_fund_rates_df.to_csv('MutualFundRates.csv', index=False)

# Save Stock Platform Data to CSV
zerodha_clients_df.to_csv('Zerodha_Clients.csv', index=False)
zerodha_stocks_df.to_csv('Zerodha_Stocks.csv', index=False)
zerodha_orders_df.to_csv('Zerodha_Orders.csv', index=False)
zerodha_stock_prices_df.to_csv('Zerodha_Stock_Prices.csv', index=False)

groww_clients_df.to_csv('Groww_Clients.csv', index=False)
groww_stocks_df.to_csv('Groww_Stocks.csv', index=False)
groww_orders_df.to_csv('Groww_Orders.csv', index=False)
groww_stock_prices_df.to_csv('Groww_Stock_Prices.csv', index=False)

sbi_stocks_clients_df.to_csv('SBI_Stocks_Clients.csv', index=False)
sbi_stocks_df.to_csv('SBI_Stocks_List.csv', index=False)
sbi_stocks_orders_df.to_csv('SBI_Stocks_Orders.csv', index=False)
sbi_stocks_prices_df.to_csv('SBI_Stocks_Prices.csv', index=False)

# Display sample data
print("MutualFunds Sample Data:")
print(mutual_funds_df.head(), "\n")

print("MutualFundRates Sample Data:")
print(mutual_fund_rates_df.head(), "\n")

print("SBI_MF_Clients Sample Data:")
print(sbi_mf_clients_df.head(), "\n")

print("TataMF_Investors Sample Data:")
print(tata_mf_investors_df.head(), "\n")

print("BajajMF_Customers Sample Data:")
print(bajaj_mf_customers_df.head(), "\n")

print("SBI_MF_Returns Sample Data:")
print(sbi_mf_returns_df.head(), "\n")

print("TataMF_InvestmentReturns Sample Data:")
print(tata_mf_investment_returns_df.head(), "\n")

print("BajajMF_ClientReturns Sample Data:")
print(bajaj_mf_client_returns_df.head(), "\n")

print("Zerodha_Clients Sample Data:")
print(zerodha_clients_df.head(), "\n")

print("Zerodha_Stocks Sample Data:")
print(zerodha_stocks_df.head(), "\n")

print("Zerodha_Orders Sample Data:")
print(zerodha_orders_df.head(), "\n")

print("Zerodha_Stock_Prices Sample Data:")
print(zerodha_stock_prices_df.head(), "\n")

print("Groww_Clients Sample Data:")
print(groww_clients_df.head(), "\n")

print("Groww_Stocks Sample Data:")
print(groww_stocks_df.head(), "\n")

print("Groww_Orders Sample Data:")
print(groww_orders_df.head(), "\n")

print("Groww_Stock_Prices Sample Data:")
print(groww_stock_prices_df.head(), "\n")

print("SBI_Stocks_Clients Sample Data:")
print(sbi_stocks_clients_df.head(), "\n")

print("SBI_Stocks_List Sample Data:")
print(sbi_stocks_df.head(), "\n")

print("SBI_Stocks_Orders Sample Data:")
print(sbi_stocks_orders_df.head(), "\n")

print("SBI_Stocks_Prices Sample Data:")
print(sbi_stocks_prices_df.head(), "\n")

# -------------------- Verification: Print Detailed Mutual Funds and Stock Platforms Investment Details --------------------

def print_investment_details(person_mapping, mutual_funds_df, stock_platforms_df_dict):
    """
    Prints detailed investment information for each person, showing which name variation
    is associated with which mutual fund and stock platform.
    """
    print("\n--- Detailed Investment Details ---\n")
    for pan, details in person_mapping.items():
        full_name = details['FullName']
        name_variations = details['NameVariations']
        mf_investments = details['MutualFunds']
        stock_investments = details['StockPlatforms']
        
        print(f"Person: {full_name}")
        print("Name Versions:")
        for variation in name_variations:
            print(f" - {variation}")
        
        if mf_investments or stock_investments:
            print("Investments:")
            for fund, name_variation in mf_investments.items():
                fund_info = mutual_funds_df[mutual_funds_df['FundName'] == f"{fund} Mutual Fund"]
                if not fund_info.empty:
                    fund_id = fund_info['MutualFundID'].values[0]
                    print(f" - {fund} Mutual Fund: {name_variation} (FundID: {fund_id})")
                else:
                    print(f" - {fund} Mutual Fund: Fund information not found.")
            for platform, name_variation in stock_investments.items():
                # Fetch platform-specific information if needed
                # For simplicity, just print the platform and name variation
                print(f" - {platform} Platform: {name_variation}")
        else:
            print("Investments: None")
        print("\n" + "-"*50 + "\n")

# Create a dictionary of stock platforms DataFrames for easy access (optional)
stock_platforms_df_dict = {
    'Zerodha': zerodha_clients_df,
    'Groww': groww_clients_df,
    'SBI_Stocks': sbi_stocks_clients_df
}

# Call the verification function with the correct mapping
print_investment_details(person_name_variations_mapping, mutual_funds_df, stock_platforms_df_dict)

print("Synthetic mutual funds and stock platforms data generation completed and saved to CSV files.")
