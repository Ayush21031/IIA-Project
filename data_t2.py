# import pandas as pd
# from faker import Faker
# import random
# import string

# # Initialize Faker
# fake = Faker('en_IN')  # Using Indian locale for realistic data

# # Set seed for reproducibility
# Faker.seed(0)
# random.seed(0)

# # Number of unique individuals
# NUM_UNIQUE_PERSONS = 100

# # Function to generate a full name with first, middle, and last names
# def generate_full_name():
#     first_name = fake.first_name()
#     middle_name = fake.first_name()
#     last_name = fake.last_name()
#     full_name = f"{first_name} {middle_name} {last_name}"
#     return full_name, first_name, middle_name, last_name

# # Function to generate name variations
# def generate_name_variations(first_name, middle_name, last_name):
#     """
#     Generate different variations of a full name.
#     E.g., "Ramesh Kumar Singh" -> ["Ramesh Kumar Singh", "RK Singh", "Ramesh K Singh", "Ramkesh K Singh"]
#     """
#     variations = []
#     # Full name
#     full_name = f"{first_name} {middle_name} {last_name}"
#     variations.append(full_name)
#     # Initials version
#     initials = f"{first_name[0]}{middle_name[0]} {last_name}"
#     variations.append(initials)
#     # Middle initial version
#     middle_initial = f"{first_name} {middle_name[0]} {last_name}"
#     variations.append(middle_initial)
#     # Alternate first name (e.g., slight misspelling)
#     if len(first_name) > 1:
#         alternate_first_name = first_name[:-1] + random.choice(string.ascii_lowercase)
#     else:
#         alternate_first_name = first_name + random.choice(string.ascii_lowercase)
#     alternate_name = f"{alternate_first_name} {middle_name} {last_name}"
#     variations.append(alternate_name)
#     return variations

# # Generate unique individuals
# unique_persons = []

# for _ in range(NUM_UNIQUE_PERSONS):
#     full_name, first_name, middle_name, last_name = generate_full_name()
#     name_variations = generate_name_variations(first_name, middle_name, last_name)
#     pan = fake.unique.bothify(text='??######?').upper()  # PAN format: 5 letters, 4 digits, 1 letter
#     national_id = fake.unique.bothify(text='###########')  # Assuming an 11-digit ID
#     email = fake.unique.email()
#     phone = fake.unique.phone_number()
#     address = fake.address().replace('\n', ', ')
#     dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
#     account_creation_date = fake.date_between(start_date='-10y', end_date='today')

#     unique_persons.append({
#         'FullName': full_name,
#         'FirstName': first_name,
#         'MiddleName': middle_name,
#         'LastName': last_name,
#         'NameVariations': name_variations,
#         'PAN': pan,
#         'NationalID': national_id,
#         'Email': email,
#         'Phone': phone,
#         'Address': address,
#         'DateOfBirth': dob,
#         'AccountCreationDate': account_creation_date
#     })

# # Assign mutual funds investments per person
# # Each person can invest in 0 to 3 mutual funds
# mutual_funds = ['SBI', 'Tata', 'Bajaj']
# person_mutual_funds = []

# for person in unique_persons:
#     num_investments = random.choice([0, 1, 2, 3])  # 0: no investment, 1: one mutual fund, etc.
#     invested_funds = random.sample(mutual_funds, num_investments)
#     fund_name_variations = {}
#     for fund in invested_funds:
#         # Assign a unique name variation for each mutual fund
#         # Cycle through available variations if necessary
#         variation_index = mutual_funds.index(fund) % len(person['NameVariations'])
#         name_variation = person['NameVariations'][variation_index]
#         fund_name_variations[fund] = name_variation
#     person_mutual_funds.append({
#         'PAN': person['PAN'],
#         'NationalID': person['NationalID'],
#         'InvestedFunds': fund_name_variations
#     })

# # Create MutualFunds DataFrame
# mutual_funds_data = [
#     {'MutualFundID': 1, 'FundName': 'SBI Mutual Fund', 'Category': 'Equity', 'RiskProfile': 'Medium', 'ManagerName': fake.name()},
#     {'MutualFundID': 2, 'FundName': 'Tata Mutual Fund', 'Category': 'Debt', 'RiskProfile': 'Low', 'ManagerName': fake.name()},
#     {'MutualFundID': 3, 'FundName': 'Bajaj Mutual Fund', 'Category': 'Hybrid', 'RiskProfile': 'High', 'ManagerName': fake.name()}
# ]
# mutual_funds_df = pd.DataFrame(mutual_funds_data)

# # Generate MutualFundRates DataFrame
# # For simplicity, generate 10 rate updates per mutual fund
# mutual_fund_rates = []
# for fund in mutual_funds_data:
#     mutual_fund_id = fund['MutualFundID']
#     for _ in range(10):
#         rate_date = fake.date_between(start_date='-5y', end_date='today')
#         rate_per_quantity = round(random.uniform(50.0, 500.0), 4)
#         mutual_fund_rates.append({
#             'MutualFundID': mutual_fund_id,
#             'RateDate': rate_date,
#             'RatePerQuantity': rate_per_quantity
#         })
# mutual_fund_rates_df = pd.DataFrame(mutual_fund_rates)

# # Sort MutualFundRates by MutualFundID and RateDate
# mutual_fund_rates_df.sort_values(by=['MutualFundID', 'RateDate'], inplace=True)
# mutual_fund_rates_df.reset_index(drop=True, inplace=True)

# # Initialize lists for clients and investment returns
# sbi_mf_clients = []
# tata_mf_investors = []
# bajaj_mf_customers = []

# sbi_mf_returns = []
# tata_mf_investment_returns = []
# bajaj_mf_client_returns = []

# # Client ID counters
# sbi_client_id_counter = 1
# tata_client_id_counter = 1
# bajaj_customer_id_counter = 1

# # Iterate through each person's mutual fund investments
# for person_funds in person_mutual_funds:
#     pan = person_funds['PAN']
#     national_id = person_funds['NationalID']
#     invested_funds = person_funds['InvestedFunds']
    
#     for fund, name_variation in invested_funds.items():
#         # Get MutualFundID
#         fund_id = mutual_funds_df[mutual_funds_df['FundName'] == f"{fund} Mutual Fund"]['MutualFundID'].values[0]
        
#         # Prepare client data based on mutual fund
#         if fund == 'SBI':
#             client = {
#                 'SBI_ClientID': sbi_client_id_counter,
#                 'FullName': name_variation,
#                 'ClientEmail': fake.unique.email(),
#                 'ContactNumber': fake.phone_number(),
#                 'PAN_Number': pan,
#                 'Address': fake.address().replace('\n', ', '),
#                 'DateOfBirth': fake.date_of_birth(minimum_age=18, maximum_age=80),
#                 'RegistrationDate': fake.date_between(start_date='-10y', end_date='today')
#             }
#             sbi_mf_clients.append(client)
#             current_client_id = sbi_client_id_counter
#             sbi_client_id_counter += 1
            
#             # Generate investment returns
#             # Get the latest rate before investment date
#             investment_date = fake.date_between(start_date='-5y', end_date='today')
#             rates_before = mutual_fund_rates_df[
#                 (mutual_fund_rates_df['MutualFundID'] == fund_id) &
#                 (mutual_fund_rates_df['RateDate'] <= investment_date)
#             ].sort_values(by='RateDate', ascending=False)
#             if not rates_before.empty:
#                 purchase_rate = rates_before.iloc[0]['RatePerQuantity']
#             else:
#                 purchase_rate = round(random.uniform(50.0, 500.0), 4)  # Default rate if no prior rate
#             units_purchased = round(random.uniform(10.0, 1000.0), 4)
#             investment_amount = round(units_purchased * purchase_rate, 2)
#             # Current NAV is the latest rate
#             current_nav = mutual_fund_rates_df[
#                 mutual_fund_rates_df['MutualFundID'] == fund_id
#             ]['RatePerQuantity'].max()
#             current_value = round(units_purchased * current_nav, 2)
#             return_percentage = round(((current_value - investment_amount) / investment_amount) * 100, 2)
#             last_updated = fake.date_between(start_date=investment_date, end_date='today')
            
#             investment = {
#                 'ReturnID': len(sbi_mf_returns) + 1,
#                 'MutualFundID': fund_id,
#                 'SBI_ClientID': current_client_id,
#                 'InvestmentDate': investment_date,
#                 'UnitsPurchased': units_purchased,
#                 'InvestmentAmount': investment_amount,
#                 'PurchaseRate': purchase_rate,
#                 'CurrentNAV': current_nav,
#                 'CurrentValue': current_value,
#                 'ReturnPercentage': return_percentage,
#                 'LastUpdated': last_updated
#             }
#             sbi_mf_returns.append(investment)
        
#         elif fund == 'Tata':
#             client = {
#                 'Tata_ClientID': tata_client_id_counter,
#                 'InvestorName': name_variation,
#                 'EmailAddress': fake.unique.email(),
#                 'PhoneNumber': fake.phone_number(),
#                 'PAN': pan,
#                 'ResidentialAddress': fake.address().replace('\n', ', '),
#                 'DOB': fake.date_of_birth(minimum_age=18, maximum_age=80),
#                 'JoinDate': fake.date_between(start_date='-10y', end_date='today')
#             }
#             tata_mf_investors.append(client)
#             current_client_id = tata_client_id_counter
#             tata_client_id_counter += 1
            
#             # Generate investment returns
#             investment_date = fake.date_between(start_date='-5y', end_date='today')
#             rates_before = mutual_fund_rates_df[
#                 (mutual_fund_rates_df['MutualFundID'] == fund_id) &
#                 (mutual_fund_rates_df['RateDate'] <= investment_date)
#             ].sort_values(by='RateDate', ascending=False)
#             if not rates_before.empty:
#                 purchase_rate = rates_before.iloc[0]['RatePerQuantity']
#             else:
#                 purchase_rate = round(random.uniform(50.0, 500.0), 4)
#             units_bought = round(random.uniform(10.0, 1000.0), 4)
#             investment_inr = round(units_bought * purchase_rate, 2)
#             current_nav = mutual_fund_rates_df[
#                 mutual_fund_rates_df['MutualFundID'] == fund_id
#             ]['RatePerQuantity'].max()
#             investment_value = round(units_bought * current_nav, 2)
#             gain_loss_percentage = round(((investment_value - investment_inr) / investment_inr) * 100, 2)
#             last_updated = fake.date_between(start_date=investment_date, end_date='today')
            
#             investment = {
#                 'InvestmentReturnID': len(tata_mf_investment_returns) + 1,
#                 'MutualFundID': fund_id,
#                 'Tata_ClientID': current_client_id,
#                 'DateOfInvestment': investment_date,
#                 'UnitsBought': units_bought,
#                 'InvestmentINR': investment_inr,
#                 'PurchaseRate': purchase_rate,
#                 'CurrentNAVValue': current_nav,
#                 'InvestmentValue': investment_value,
#                 'GainLossPercentage': gain_loss_percentage,
#                 'LastUpdated': last_updated
#             }
#             tata_mf_investment_returns.append(investment)
        
#         elif fund == 'Bajaj':
#             client = {
#                 'Bajaj_CustomerID': bajaj_customer_id_counter,
#                 'Name': name_variation,
#                 'Email': fake.unique.email(),
#                 'Mobile': fake.phone_number(),
#                 'PAN_Num': pan,
#                 'Addr': fake.address().replace('\n', ', '),
#                 'DOB': fake.date_of_birth(minimum_age=18, maximum_age=80),
#                 'DateJoined': fake.date_between(start_date='-10y', end_date='today')
#             }
#             bajaj_mf_customers.append(client)
#             current_customer_id = bajaj_customer_id_counter
#             bajaj_customer_id_counter += 1
            
#             # Generate investment returns
#             investment_date = fake.date_between(start_date='-5y', end_date='today')
#             rates_before = mutual_fund_rates_df[
#                 (mutual_fund_rates_df['MutualFundID'] == fund_id) &
#                 (mutual_fund_rates_df['RateDate'] <= investment_date)
#             ].sort_values(by='RateDate', ascending=False)
#             if not rates_before.empty:
#                 purchase_rate = rates_before.iloc[0]['RatePerQuantity']
#             else:
#                 purchase_rate = round(random.uniform(50.0, 500.0), 4)
#             units_purchased = round(random.uniform(10.0, 1000.0), 4)
#             amount_invested = round(units_purchased * purchase_rate, 2)
#             current_nav = mutual_fund_rates_df[
#                 mutual_fund_rates_df['MutualFundID'] == fund_id
#             ]['RatePerQuantity'].max()
#             current_value = round(units_purchased * current_nav, 2)
#             profit_loss_perc = round(((current_value - amount_invested) / amount_invested) * 100, 2)
#             update_date = fake.date_between(start_date=investment_date, end_date='today')
            
#             investment = {
#                 'ClientReturnID': len(bajaj_mf_client_returns) + 1,
#                 'MutualFundID': fund_id,
#                 'Bajaj_CustomerID': current_customer_id,
#                 'InvestmentDate': investment_date,
#                 'UnitsPurchased': units_purchased,
#                 'AmountInvested': amount_invested,
#                 'PurchaseRate': purchase_rate,
#                 'CurrentNAV': current_nav,
#                 'CurrentValue': current_value,
#                 'ProfitLossPerc': profit_loss_perc,
#                 'UpdateDate': update_date
#             }
#             bajaj_mf_client_returns.append(investment)

# # Convert clients and investments lists to DataFrames
# sbi_mf_clients_df = pd.DataFrame(sbi_mf_clients)
# tata_mf_investors_df = pd.DataFrame(tata_mf_investors)
# bajaj_mf_customers_df = pd.DataFrame(bajaj_mf_customers)

# sbi_mf_returns_df = pd.DataFrame(sbi_mf_returns)
# tata_mf_investment_returns_df = pd.DataFrame(tata_mf_investment_returns)
# bajaj_mf_client_returns_df = pd.DataFrame(bajaj_mf_client_returns)

# # Save banks data to CSV files
# sbi_mf_clients_df.to_csv('SBI_MF_Clients.csv', index=False)
# tata_mf_investors_df.to_csv('TataMF_Investors.csv', index=False)
# bajaj_mf_customers_df.to_csv('BajajMF_Customers.csv', index=False)

# sbi_mf_returns_df.to_csv('SBI_MF_Returns.csv', index=False)
# tata_mf_investment_returns_df.to_csv('TataMF_InvestmentReturns.csv', index=False)
# bajaj_mf_client_returns_df.to_csv('BajajMF_ClientReturns.csv', index=False)

# mutual_funds_df.to_csv('MutualFunds.csv', index=False)
# mutual_fund_rates_df.to_csv('MutualFundRates.csv', index=False)

# # Display sample data
# print("MutualFunds Sample Data:")
# print(mutual_funds_df.head(), "\n")

# print("MutualFundRates Sample Data:")
# print(mutual_fund_rates_df.head(), "\n")

# print("SBI_MF_Clients Sample Data:")
# print(sbi_mf_clients_df.head(), "\n")

# print("TataMF_Investors Sample Data:")
# print(tata_mf_investors_df.head(), "\n")

# print("BajajMF_Customers Sample Data:")
# print(bajaj_mf_customers_df.head(), "\n")

# print("SBI_MF_Returns Sample Data:")
# print(sbi_mf_returns_df.head(), "\n")

# print("TataMF_InvestmentReturns Sample Data:")
# print(tata_mf_investment_returns_df.head(), "\n")

# print("BajajMF_ClientReturns Sample Data:")
# print(bajaj_mf_client_returns_df.head(), "\n")

# # -------------------- Print Detailed Mutual Funds Investment Details --------------------

# def print_investment_details(bank_name, clients_df, returns_df, mutual_funds_df, client_id_col, name_col, fund_name_col):
#     """
#     Prints detailed investment information for each client in a mutual funds bank.
#     """
#     for idx, client in clients_df.iterrows():
#         try:
#             client_id = client[client_id_col]
#         except KeyError:
#             print(f"Error: Column '{client_id_col}' not found in clients DataFrame for {bank_name}.")
#             continue

#         try:
#             client_name = client[name_col]
#         except KeyError:
#             print(f"Error: Column '{name_col}' not found in clients DataFrame for {bank_name}.")
#             continue

#         # Determine PAN column based on bank
#         if bank_name == 'SBI':
#             pan_col = 'PAN_Number'
#         elif bank_name == 'Tata':
#             pan_col = 'PAN'
#         elif bank_name == 'Bajaj':
#             pan_col = 'PAN_Num'
#         else:
#             pan_col = None

#         if pan_col and pan_col in client:
#             client_pan = client[pan_col]
#         else:
#             client_pan = 'N/A'

#         # Filter investments for this client
#         client_returns = returns_df[returns_df[client_id_col] == client_id]

#         num_investments = len(client_returns)
#         if num_investments > 0:
#             print(f"Client: {client_name} (PAN: {client_pan}) has {num_investments} investment(s) in {bank_name} Mutual Fund:")
#             for _, investment in client_returns.iterrows():
#                 mutual_fund_id = investment['MutualFundID']
#                 # Retrieve mutual fund details
#                 mutual_fund = mutual_funds_df[mutual_funds_df['MutualFundID'] == mutual_fund_id]
#                 if mutual_fund.empty:
#                     print(f"  - Mutual Fund ID {mutual_fund_id} not found in MutualFunds DataFrame.")
#                     continue
#                 mutual_fund = mutual_fund.iloc[0]
#                 mutual_fund_name = mutual_fund[fund_name_col]
#                 # Additional investment details based on bank
#                 if bank_name == 'SBI':
#                     amount = investment['InvestmentAmount']
#                     current_value = investment['CurrentValue']
#                     return_pct = investment['ReturnPercentage']
#                     print(f"  - Fund: {mutual_fund_name}, Amount Invested: INR {amount}, Current Value: INR {current_value}, Return: {return_pct}%")
#                 elif bank_name == 'Tata':
#                     amount = investment['InvestmentINR']
#                     current_value = investment['InvestmentValue']
#                     gain_loss_pct = investment['GainLossPercentage']
#                     print(f"  - Fund: {mutual_fund_name}, Amount Invested: INR {amount}, Current Value: INR {current_value}, Gain/Loss: {gain_loss_pct}%")
#                 elif bank_name == 'Bajaj':
#                     amount = investment['AmountInvested']
#                     current_value = investment['CurrentValue']
#                     profit_loss_pct = investment['ProfitLossPerc']
#                     print(f"  - Fund: {mutual_fund_name}, Amount Invested: INR {amount}, Current Value: INR {current_value}, Profit/Loss: {profit_loss_pct}%")
#             print("\n")

# print("\n--- Detailed Mutual Funds Investment Details ---\n")

# for fund in mutual_funds:
#     print(f"--- {fund} Mutual Funds Investments ---\n")
#     if fund == 'SBI':
#         clients_df = sbi_mf_clients_df
#         returns_df = sbi_mf_returns_df
#         fund_name = 'SBI Mutual Fund'
#         fund_id = mutual_funds_df[mutual_funds_df['FundName'] == fund_name]['MutualFundID'].values[0]
#         mutual_funds_subset_df = mutual_funds_df[mutual_funds_df['MutualFundID'] == fund_id]
#         client_id_col = 'SBI_ClientID'
#         name_col = 'FullName'
#         fund_name_col = 'FundName'
#     elif fund == 'Tata':
#         clients_df = tata_mf_investors_df
#         returns_df = tata_mf_investment_returns_df
#         fund_name = 'Tata Mutual Fund'
#         fund_id = mutual_funds_df[mutual_funds_df['FundName'] == fund_name]['MutualFundID'].values[0]
#         mutual_funds_subset_df = mutual_funds_df[mutual_funds_df['MutualFundID'] == fund_id]
#         client_id_col = 'Tata_ClientID'
#         name_col = 'InvestorName'
#         fund_name_col = 'FundName'
#     elif fund == 'Bajaj':
#         clients_df = bajaj_mf_customers_df
#         returns_df = bajaj_mf_client_returns_df
#         fund_name = 'Bajaj Mutual Fund'
#         fund_id = mutual_funds_df[mutual_funds_df['FundName'] == fund_name]['MutualFundID'].values[0]
#         mutual_funds_subset_df = mutual_funds_df[mutual_funds_df['MutualFundID'] == fund_id]
#         client_id_col = 'Bajaj_CustomerID'
#         name_col = 'Name'
#         fund_name_col = 'FundName'
    
#     print_investment_details(
#         bank_name=fund,
#         clients_df=clients_df,
#         returns_df=returns_df,
#         mutual_funds_df=mutual_funds_subset_df,
#         client_id_col=client_id_col,
#         name_col=name_col,
#         fund_name_col=fund_name_col
#     )

# print("Synthetic mutual funds data generation completed and saved to CSV files.")
























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

# Assign mutual funds investments per person
# Each person can invest in 0 to 3 mutual funds
mutual_funds = ['SBI', 'Tata', 'Bajaj']
person_mutual_funds = []

for person in unique_persons:
    num_investments = random.choice([0, 1, 2, 3])  # 0: no investment, 1: one mutual fund, etc.
    invested_funds = random.sample(mutual_funds, num_investments)
    fund_name_variations = {}
    for fund in invested_funds:
        # Assign a unique name variation for each mutual fund
        # Cycle through available variations if necessary
        variation_index = mutual_funds.index(fund) % len(person['NameVariations'])
        name_variation = person['NameVariations'][variation_index]
        fund_name_variations[fund] = name_variation
    person_mutual_funds.append({
        'PAN': person['PAN'],
        'NationalID': person['NationalID'],
        'InvestedFunds': fund_name_variations
    })

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

# Initialize lists for clients and investment returns
sbi_mf_clients = []
tata_mf_investors = []
bajaj_mf_customers = []

sbi_mf_returns = []
tata_mf_investment_returns = []
bajaj_mf_client_returns = []

# Client ID counters
sbi_client_id_counter = 1
tata_client_id_counter = 1
bajaj_customer_id_counter = 1

# Mapping dictionary to store name variations per person
person_name_variations_mapping = {}

# Iterate through each person's mutual fund investments
for person_funds in person_mutual_funds:
    pan = person_funds['PAN']
    national_id = person_funds['NationalID']
    invested_funds = person_funds['InvestedFunds']
    
    # Find the person in unique_persons list
    person = next((p for p in unique_persons if p['PAN'] == pan and p['NationalID'] == national_id), None)
    if person is None:
        continue  # Skip if person not found
    
    # Initialize mapping if not already
    if pan not in person_name_variations_mapping:
        person_name_variations_mapping[pan] = {
            'FullName': person['FullName'],
            'NameVariations': person['NameVariations'],
            'Investments': {}
        }
    
    for fund, name_variation in invested_funds.items():
        # Get MutualFundID
        fund_id = mutual_funds_df[mutual_funds_df['FundName'] == f"{fund} Mutual Fund"]['MutualFundID'].values[0]
        
        # Store investment in mapping
        person_name_variations_mapping[pan]['Investments'][fund] = name_variation
        
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

# Convert clients and investments lists to DataFrames
sbi_mf_clients_df = pd.DataFrame(sbi_mf_clients)
tata_mf_investors_df = pd.DataFrame(tata_mf_investors)
bajaj_mf_customers_df = pd.DataFrame(bajaj_mf_customers)

sbi_mf_returns_df = pd.DataFrame(sbi_mf_returns)
tata_mf_investment_returns_df = pd.DataFrame(tata_mf_investment_returns)
bajaj_mf_client_returns_df = pd.DataFrame(bajaj_mf_client_returns)

# Save data to CSV files
sbi_mf_clients_df.to_csv('SBI_MF_Clients.csv', index=False)
tata_mf_investors_df.to_csv('TataMF_Investors.csv', index=False)
bajaj_mf_customers_df.to_csv('BajajMF_Customers.csv', index=False)

sbi_mf_returns_df.to_csv('SBI_MF_Returns.csv', index=False)
tata_mf_investment_returns_df.to_csv('TataMF_InvestmentReturns.csv', index=False)
bajaj_mf_client_returns_df.to_csv('BajajMF_ClientReturns.csv', index=False)

mutual_funds_df.to_csv('MutualFunds.csv', index=False)
mutual_fund_rates_df.to_csv('MutualFundRates.csv', index=False)

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

# -------------------- Verification: Print Detailed Mutual Funds Investment Details --------------------

def print_investment_details(person_mapping, mutual_funds_df):
    """
    Prints detailed investment information for each person, showing which name variation
    is associated with which mutual fund.
    """
    print("\n--- Detailed Mutual Funds Investment Details ---\n")
    for pan, details in person_mapping.items():
        full_name = details['FullName']
        name_variations = details['NameVariations']
        investments = details['Investments']
        
        print(f"Person: {full_name}")
        print("Name Versions:")
        for variation in name_variations:
            print(f" - {variation}")
        
        if investments:
            print("Investments:")
            for fund, name_variation in investments.items():
                fund_info = mutual_funds_df[mutual_funds_df['FundName'] == f"{fund} Mutual Fund"]
                if not fund_info.empty:
                    fund_id = fund_info['MutualFundID'].values[0]
                    print(f" - {fund} Mutual Fund: {name_variation} (FundID: {fund_id})")
                else:
                    print(f" - {fund} Mutual Fund: Fund information not found.")
        else:
            print("Investments: None")
        print("\n" + "-"*50 + "\n")

# Call the verification function
print_investment_details(person_name_variations_mapping, mutual_funds_df)

print("Synthetic mutual funds data generation completed and saved to CSV files.")
