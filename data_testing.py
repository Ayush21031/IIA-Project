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

# Select 25 unique persons to have multiple bank accounts
MULTI_BANK_COUNT = 25
multi_bank_indices = random.sample(range(NUM_UNIQUE_PERSONS), MULTI_BANK_COUNT)

# List to track name variations across banks for multi-bank individuals
multi_bank_persons_names = []

# Prepare data for each bank
icici_data = []
hdfc_data = []
sbi_data = []

for idx, person in enumerate(unique_persons):
    if idx in multi_bank_indices:
        # This person will have multiple bank accounts
        # Decide randomly to have 2 or 3 bank accounts
        num_banks = random.choice([2, 3])
        banks = random.sample(['ICICI', 'HDFC', 'SBI'], num_banks)

        # Dictionary to store name used in each bank
        name_bank_mapping = {}

        # Assign different name variations to each bank
        for bank_idx, bank in enumerate(banks):
            # Assign a unique name variation to each bank
            # If there are enough variations, use them; else, cycle through
            variations = person['NameVariations']
            name = variations[bank_idx % len(variations)]

            name_bank_mapping[bank] = name  # Store the name used for this bank

            if bank == 'ICICI':
                icici_acc_no = fake.unique.bothify(text='IC###-####-####')
                icici_account = {
                    'ICICI_AccountID': len(icici_data) + 1,
                    'CustomerName': name,
                    'AccountNumber': icici_acc_no,
                    'ServiceType': random.choice(['Savings', 'Current']),
                    'NationalID': person['NationalID'],
                    'PAN': person['PAN'],
                    'Balance': round(random.uniform(1000, 100000), 2),
                    'InterestRate': round(random.uniform(1.0, 5.0), 2),
                    'LastUpdated': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
                }
                icici_data.append(icici_account)
            elif bank == 'HDFC':
                hdfc_acc_no = fake.unique.bothify(text='HDFC-####-####')
                hdfc_account = {
                    'HDFC_AccountID': len(hdfc_data) + 1,
                    'ClientName': name,
                    'AccNo': hdfc_acc_no,
                    'AccountType': random.choice(['Fixed Deposit', 'Savings']),
                    'GovtID': person['NationalID'],
                    'PAN': person['PAN'],
                    'CurrentBalance': round(random.uniform(5000, 200000), 2),
                    'MonthlyInterest': round(random.uniform(0.5, 3.0), 2),
                    'LastUpdate': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
                }
                hdfc_data.append(hdfc_account)
            elif bank == 'SBI':
                sbi_acc_no = fake.unique.bothify(text='SBI-####-####')
                sbi_account = {
                    'SBI_AccountID': len(sbi_data) + 1,
                    'AccountHolder': name,
                    'Acc_Number': sbi_acc_no,
                    'Service_Type': random.choice(['Current', 'Savings']),
                    'National_ID': person['NationalID'],
                    'PAN': person['PAN'],
                    'AmountStored': round(random.uniform(2000, 150000), 2),
                    'Interest_Rate': round(random.uniform(1.5, 4.5), 2),
                    'Last_Updated': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
                }
                sbi_data.append(sbi_account)

        # Append the mapping to the tracking list
        multi_bank_persons_names.append({
            'PAN': person['PAN'],
            'NationalID': person['NationalID'],
            'NameBankMapping': name_bank_mapping
        })
    else:
        # This person will have at most one bank account
        # Decide randomly which bank to assign
        banks = ['ICICI', 'HDFC', 'SBI']
        bank = random.choice(banks)

        # Select a random name variation
        name = random.choice(person['NameVariations'])

        if bank == 'ICICI':
            icici_acc_no = fake.unique.bothify(text='IC###-####-####')
            icici_account = {
                'ICICI_AccountID': len(icici_data) + 1,
                'CustomerName': name,
                'AccountNumber': icici_acc_no,
                'ServiceType': random.choice(['Savings', 'Current']),
                'NationalID': person['NationalID'],
                'PAN': person['PAN'],
                'Balance': round(random.uniform(1000, 100000), 2),
                'InterestRate': round(random.uniform(1.0, 5.0), 2),
                'LastUpdated': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
            }
            icici_data.append(icici_account)
        elif bank == 'HDFC':
            hdfc_acc_no = fake.unique.bothify(text='HDFC-####-####')
            hdfc_account = {
                'HDFC_AccountID': len(hdfc_data) + 1,
                'ClientName': name,
                'AccNo': hdfc_acc_no,
                'AccountType': random.choice(['Fixed Deposit', 'Savings']),
                'GovtID': person['NationalID'],
                'PAN': person['PAN'],
                'CurrentBalance': round(random.uniform(5000, 200000), 2),
                'MonthlyInterest': round(random.uniform(0.5, 3.0), 2),
                'LastUpdate': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
            }
            hdfc_data.append(hdfc_account)
        elif bank == 'SBI':
            sbi_acc_no = fake.unique.bothify(text='SBI-####-####')
            sbi_account = {
                'SBI_AccountID': len(sbi_data) + 1,
                'AccountHolder': name,
                'Acc_Number': sbi_acc_no,
                'Service_Type': random.choice(['Current', 'Savings']),
                'National_ID': person['NationalID'],
                'PAN': person['PAN'],
                'AmountStored': round(random.uniform(2000, 150000), 2),
                'Interest_Rate': round(random.uniform(1.5, 4.5), 2),
                'Last_Updated': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
            }
            sbi_data.append(sbi_account)

# Introduce some distinct individuals with similar names
additional_persons = []
for _ in range(20):  # 20 additional similar names
    base_person = random.choice(unique_persons)
    base_name = base_person['FullName']
    first_name, middle_name, last_name = base_name.split()
    name_variations = generate_name_variations(first_name, middle_name, last_name)
    # Slight variation: add "Jr." to some name variations
    name_variations = [name + " Jr." if "Jr." not in name else name for name in name_variations]
    pan = fake.unique.bothify(text='??######?').upper()
    national_id = fake.unique.bothify(text='###########')
    email = fake.unique.email()
    phone = fake.unique.phone_number()
    address = fake.address().replace('\n', ', ')
    dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
    account_creation_date = fake.date_between(start_date='-10y', end_date='today')

    additional_persons.append({
        'FullName': base_name + " Jr.",
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

# Assign accounts to these additional similar individuals
for person in additional_persons:
    # Randomly decide which banks the person has accounts in (1 to 3)
    num_banks = random.choice([1, 2, 3])
    banks = random.sample(['ICICI', 'HDFC', 'SBI'], num_banks)

    # Dictionary to store name used in each bank (optional, not tracked here)
    for bank_idx, bank in enumerate(banks):
        # Assign a unique name variation to each bank
        variations = person['NameVariations']
        name = variations[bank_idx % len(variations)]

        if bank == 'ICICI':
            icici_acc_no = fake.unique.bothify(text='IC###-####-####')
            icici_account = {
                'ICICI_AccountID': len(icici_data) + 1,
                'CustomerName': name,
                'AccountNumber': icici_acc_no,
                'ServiceType': random.choice(['Savings', 'Current']),
                'NationalID': person['NationalID'],
                'PAN': person['PAN'],
                'Balance': round(random.uniform(1000, 100000), 2),
                'InterestRate': round(random.uniform(1.0, 5.0), 2),
                'LastUpdated': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
            }
            icici_data.append(icici_account)
        elif bank == 'HDFC':
            hdfc_acc_no = fake.unique.bothify(text='HDFC-####-####')
            hdfc_account = {
                'HDFC_AccountID': len(hdfc_data) + 1,
                'ClientName': name,
                'AccNo': hdfc_acc_no,
                'AccountType': random.choice(['Fixed Deposit', 'Savings']),
                'GovtID': person['NationalID'],
                'PAN': person['PAN'],
                'CurrentBalance': round(random.uniform(5000, 200000), 2),
                'MonthlyInterest': round(random.uniform(0.5, 3.0), 2),
                'LastUpdate': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
            }
            hdfc_data.append(hdfc_account)
        elif bank == 'SBI':
            sbi_acc_no = fake.unique.bothify(text='SBI-####-####')
            sbi_account = {
                'SBI_AccountID': len(sbi_data) + 1,
                'AccountHolder': name,
                'Acc_Number': sbi_acc_no,
                'Service_Type': random.choice(['Current', 'Savings']),
                'National_ID': person['NationalID'],
                'PAN': person['PAN'],
                'AmountStored': round(random.uniform(2000, 150000), 2),
                'Interest_Rate': round(random.uniform(1.5, 4.5), 2),
                'Last_Updated': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
            }
            sbi_data.append(sbi_account)

# Combine unique_persons and additional_persons for mutual funds data generation
all_persons = unique_persons + additional_persons

# Convert to DataFrames
icici_df = pd.DataFrame(icici_data)
hdfc_df = pd.DataFrame(hdfc_data)
sbi_df = pd.DataFrame(sbi_data)

# Save accounts data to CSV files
icici_df.to_csv('ICICI_Accounts.csv', index=False)
hdfc_df.to_csv('HDFC_Accounts.csv', index=False)
sbi_df.to_csv('SBI_Accounts.csv', index=False)

# Display sample data
print("ICICI_Accounts Sample Data:")
print(icici_df.head(), "\n")

print("HDFC_Accounts Sample Data:")
print(hdfc_df.head(), "\n")

print("SBI_Accounts Sample Data:")
print(sbi_df.head(), "\n")

# Print name variations for multi-bank individuals
print("\n--- Name Variations Across Banks for Multi-Bank Individuals ---\n")
for idx, person in enumerate(multi_bank_persons_names, 1):
    print(f"Individual {idx}:")
    print(f"  PAN: {person['PAN']}")
    print(f"  NationalID: {person['NationalID']}")
    for bank, name in person['NameBankMapping'].items():
        print(f"  {bank} Account Name: {name}")
    print("\n")

print("Synthetic accounts data generation completed and saved to CSV files.\n")

# -------------------- Mutual Funds Data Generation --------------------

# Define Mutual Funds Banks
mutual_funds_banks = ['SBI', 'Tata', 'Bajaj']

# Define number of mutual funds per bank (set to 1 as per requirement)
NUM_FUNDS_PER_BANK = 1

# Define number of clients per mutual funds bank
NUM_MF_CLIENTS_PER_BANK = 80

# Initialize data structures
sbi_mf_clients = []
tata_mf_investors = []
bajaj_mf_customers = []

sbi_mf_funds = []
tata_mf_mutual_funds = []
bajaj_mf_funds = []

sbi_mf_returns = []
tata_mf_investment_returns = []
bajaj_mf_client_returns = []

# Function to generate Mutual Funds with correct column names per bank
def generate_mutual_funds(bank_name, num_funds):
    """
    Generate a list of mutual funds for a given bank with correct column names.
    """
    funds = []
    for _ in range(num_funds):
        if bank_name == 'SBI':
            fund_name = "SBI Mutual Fund"
            fund_type = 'Equity'  # Fixed type for simplicity
            risk_category = 'Medium'
            launch_date = fake.date_between(start_date='-15y', end_date='today')
            fund_manager = fake.name()
            nav = round(random.uniform(10.0, 1000.0), 4)
            aum = round(random.uniform(1000000.0, 500000000.0), 2)  # Assets Under Management

            fund = {
                'SBI_FundID': 1,  # Only one fund per bank
                'FundName': fund_name,
                'FundType': fund_type,
                'RiskCategory': risk_category,
                'LaunchDate': launch_date,
                'FundManager': fund_manager,
                'NAV': nav,
                'AUM': aum
            }
        elif bank_name == 'Tata':
            fund_name = "Tata Mutual Fund"
            category = 'Debt'  # Fixed category for simplicity
            risk_level = 'Low'
            inception_date = fake.date_between(start_date='-15y', end_date='today')
            fund_manager_name = fake.name()
            current_nav = round(random.uniform(10.0, 1000.0), 4)
            total_aum = round(random.uniform(1000000.0, 500000000.0), 2)

            fund = {
                'Tata_FundID': 1,  # Only one fund per bank
                'NameOfFund': fund_name,
                'Category': category,
                'RiskLevel': risk_level,
                'InceptionDate': inception_date,
                'FundManagerName': fund_manager_name,
                'CurrentNAV': current_nav,
                'TotalAUM': total_aum
            }
        elif bank_name == 'Bajaj':
            fund_title = "Bajaj Mutual Fund"
            fund_category = 'Hybrid'  # Fixed category for simplicity
            risk_profile = 'High'
            start_date = fake.date_between(start_date='-15y', end_date='today')
            manager_name = fake.name()
            nav_value = round(random.uniform(10.0, 1000.0), 4)
            assets_under_mgmt = round(random.uniform(1000000.0, 500000000.0), 2)

            fund = {
                'Bajaj_FundID': 1,  # Only one fund per bank
                'FundTitle': fund_title,
                'FundCategory': fund_category,
                'RiskProfile': risk_profile,
                'StartDate': start_date,
                'ManagerName': manager_name,
                'NAV_Value': nav_value,
                'AssetsUnderMgmt': assets_under_mgmt
            }
        funds.append(fund)
    return funds

# Function to generate Mutual Funds clients
def generate_mf_clients(bank_name, num_clients):
    """
    Generate a list of mutual funds clients for a given bank.
    """
    clients = []
    # Select random unique persons without replacement
    selected_persons = random.sample(all_persons, num_clients)
    for idx, person in enumerate(selected_persons):
        # Assign a name variation based on the mutual funds bank
        # Ensure different name variations for different mutual funds banks
        if bank_name == 'SBI':
            name_variation = person['NameVariations'][0]  # Full Name
            client = {
                'SBI_ClientID': idx + 1,
                'FullName': name_variation,
                'ClientEmail': fake.unique.email(),
                'ContactNumber': person['Phone'],
                'PAN_Number': person['PAN'],
                'Address': person['Address'],
                'DateOfBirth': person['DateOfBirth'],
                'RegistrationDate': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
            }
            clients.append(client)
        elif bank_name == 'Tata':
            name_variation = person['NameVariations'][1]  # Initials
            client = {
                'Tata_ClientID': idx + 1,
                'InvestorName': name_variation,
                'EmailAddress': fake.unique.email(),
                'PhoneNumber': person['Phone'],
                'PAN': person['PAN'],
                'ResidentialAddress': person['Address'],
                'DOB': person['DateOfBirth'],
                'JoinDate': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
            }
            clients.append(client)
        elif bank_name == 'Bajaj':
            name_variation = person['NameVariations'][2]  # Middle initial
            client = {
                'Bajaj_CustomerID': idx + 1,
                'Name': name_variation,
                'Email': fake.unique.email(),
                'Mobile': person['Phone'],
                'PAN_Num': person['PAN'],
                'Addr': person['Address'],
                'DOB': person['DateOfBirth'],
                'DateJoined': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
            }
            clients.append(client)
    return clients

# Function to generate Investment Returns with correct column names per bank
def generate_investment_returns(bank_name, clients, funds):
    """
    Generate investment returns for a given mutual funds bank.
    """
    returns = []
    for client in clients:
        client_id = client[f'{bank_name}_ClientID'] if bank_name != 'Bajaj' else client['Bajaj_CustomerID']
        num_investments = random.randint(1, 3)  # Number of investments per client (max 3 for simplicity)
        for _ in range(num_investments):
            fund = funds[0]  # Only one fund per bank
            if bank_name == 'SBI':
                investment_date = fake.date_between(start_date=fund['LaunchDate'], end_date='today')
                units_purchased = round(random.uniform(10.0, 1000.0), 4)
                investment_amount = round(units_purchased * fund['NAV'], 2)
                current_nav = round(fund['NAV'] * random.uniform(0.95, 1.10), 4)  # +/-5-10%
                current_value = round(units_purchased * current_nav, 2)
                return_percentage = round(((current_value - investment_amount) / investment_amount) * 100, 2)
                last_updated = fake.date_between(start_date=investment_date, end_date='today')

                investment = {
                    'ReturnID': len(returns) + 1,
                    'SBI_FundID': fund['SBI_FundID'],
                    'SBI_ClientID': client_id,
                    'InvestmentDate': investment_date,
                    'UnitsPurchased': units_purchased,
                    'InvestmentAmount': investment_amount,
                    'CurrentNAV': current_nav,
                    'CurrentValue': current_value,
                    'ReturnPercentage': return_percentage,
                    'LastUpdated': last_updated
                }
                returns.append(investment)
            elif bank_name == 'Tata':
                investment_date = fake.date_between(start_date=fund['InceptionDate'], end_date='today')
                units_bought = round(random.uniform(10.0, 1000.0), 4)
                investment_inr = round(units_bought * fund['CurrentNAV'], 2)
                nav_at_purchase = fund['CurrentNAV']
                current_nav = round(nav_at_purchase * random.uniform(0.95, 1.10), 4)
                investment_value = round(units_bought * current_nav, 2)
                gain_loss_percentage = round(((investment_value - investment_inr) / investment_inr) * 100, 2)
                last_updated = fake.date_between(start_date=investment_date, end_date='today')

                investment = {
                    'InvestmentReturnID': len(returns) + 1,
                    'Tata_FundID': fund['Tata_FundID'],
                    'Tata_ClientID': client_id,
                    'DateOfInvestment': investment_date,
                    'UnitsBought': units_bought,
                    'InvestmentINR': investment_inr,
                    'NAVAtPurchase': nav_at_purchase,
                    'CurrentNAVValue': current_nav,
                    'InvestmentValue': investment_value,
                    'GainLossPercentage': gain_loss_percentage,
                    'LastUpdated': last_updated
                }
                returns.append(investment)
            elif bank_name == 'Bajaj':
                investment_date = fake.date_between(start_date=fund['StartDate'], end_date='today')
                units_purchased = round(random.uniform(10.0, 1000.0), 4)
                amount_invested = round(units_purchased * fund['NAV_Value'], 2)
                purchase_nav = fund['NAV_Value']
                current_nav = round(purchase_nav * random.uniform(0.95, 1.10), 4)
                current_value = round(units_purchased * current_nav, 2)
                profit_loss_perc = round(((current_value - amount_invested) / amount_invested) * 100, 2)
                update_date = fake.date_between(start_date=investment_date, end_date='today')

                investment = {
                    'ClientReturnID': len(returns) + 1,
                    'Bajaj_FundID': fund['Bajaj_FundID'],
                    'Bajaj_CustomerID': client_id,
                    'InvestmentDate': investment_date,
                    'UnitsPurchased': units_purchased,
                    'AmountInvested': amount_invested,
                    'PurchaseNAV': purchase_nav,
                    'CurrentNAV': current_nav,
                    'CurrentValue': current_value,
                    'ProfitLossPerc': profit_loss_perc,
                    'UpdateDate': update_date
                }
                returns.append(investment)
    return returns

# Function to print investment details for a mutual funds bank
def print_investment_details(bank_name, clients_df, returns_df, funds_df, client_id_col, fund_id_col, name_col, fund_name_col):
    for idx, client in clients_df.iterrows():
        try:
            client_id = client[client_id_col]
        except KeyError:
            print(f"Error: Column '{client_id_col}' not found in clients DataFrame for {bank_name}.")
            continue

        try:
            client_name = client[name_col]
        except KeyError:
            print(f"Error: Column '{name_col}' not found in clients DataFrame for {bank_name}.")
            continue

        # Determine PAN column based on bank
        if bank_name == 'SBI':
            pan_col = 'PAN_Number'
        elif bank_name == 'Tata':
            pan_col = 'PAN'
        elif bank_name == 'Bajaj':
            pan_col = 'PAN_Num'
        else:
            pan_col = None

        if pan_col and pan_col in client:
            client_pan = client[pan_col]
        else:
            client_pan = 'N/A'

        # Filter investments for this client
        client_returns = returns_df[returns_df[client_id_col] == client_id]

        num_investments = len(client_returns)
        if num_investments > 0:
            print(f"Client: {client_name} (PAN: {client_pan}) has {num_investments} investment(s) in {bank_name} Mutual Fund:")
            for _, investment in client_returns.iterrows():
                fund_id = investment[fund_id_col]
                # Corrected fund retrieval
                fund = funds_df[funds_df[fund_id_col] == fund_id]
                if len(fund) == 0:
                    print(f"  - Fund ID {fund_id} not found in funds DataFrame.")
                    continue
                fund = fund.iloc[0]
                fund_name = fund[fund_name_col]
                # Additional investment details based on bank
                if bank_name == 'SBI':
                    amount = investment['InvestmentAmount']
                    current_value = investment['CurrentValue']
                    return_pct = investment['ReturnPercentage']
                    print(f"  - Fund: {fund_name}, Amount Invested: INR {amount}, Current Value: INR {current_value}, Return: {return_pct}%")
                elif bank_name == 'Tata':
                    amount = investment['InvestmentINR']
                    current_value = investment['InvestmentValue']
                    gain_loss_pct = investment['GainLossPercentage']
                    print(f"  - Fund: {fund_name}, Amount Invested: INR {amount}, Current Value: INR {current_value}, Gain/Loss: {gain_loss_pct}%")
                elif bank_name == 'Bajaj':
                    amount = investment['AmountInvested']
                    current_value = investment['CurrentValue']
                    profit_loss_pct = investment['ProfitLossPerc']
                    print(f"  - Fund: {fund_name}, Amount Invested: INR {amount}, Current Value: INR {current_value}, Profit/Loss: {profit_loss_pct}%")
            print("\n")

# Function to generate Mutual Funds with correct column names per bank
def generate_mutual_funds(bank_name, num_funds):
    """
    Generate a list of mutual funds for a given bank with correct column names.
    """
    funds = []
    for _ in range(num_funds):
        if bank_name == 'SBI':
            fund_name = "SBI Mutual Fund"
            fund_type = 'Equity'  # Fixed type for simplicity
            risk_category = 'Medium'
            launch_date = fake.date_between(start_date='-15y', end_date='today')
            fund_manager = fake.name()
            nav = round(random.uniform(10.0, 1000.0), 4)
            aum = round(random.uniform(1000000.0, 500000000.0), 2)  # Assets Under Management

            fund = {
                'SBI_FundID': 1,  # Only one fund per bank
                'FundName': fund_name,
                'FundType': fund_type,
                'RiskCategory': risk_category,
                'LaunchDate': launch_date,
                'FundManager': fund_manager,
                'NAV': nav,
                'AUM': aum
            }
        elif bank_name == 'Tata':
            fund_name = "Tata Mutual Fund"
            category = 'Debt'  # Fixed category for simplicity
            risk_level = 'Low'
            inception_date = fake.date_between(start_date='-15y', end_date='today')
            fund_manager_name = fake.name()
            current_nav = round(random.uniform(10.0, 1000.0), 4)
            total_aum = round(random.uniform(1000000.0, 500000000.0), 2)

            fund = {
                'Tata_FundID': 1,  # Only one fund per bank
                'NameOfFund': fund_name,
                'Category': category,
                'RiskLevel': risk_level,
                'InceptionDate': inception_date,
                'FundManagerName': fund_manager_name,
                'CurrentNAV': current_nav,
                'TotalAUM': total_aum
            }
        elif bank_name == 'Bajaj':
            fund_title = "Bajaj Mutual Fund"
            fund_category = 'Hybrid'  # Fixed category for simplicity
            risk_profile = 'High'
            start_date = fake.date_between(start_date='-15y', end_date='today')
            manager_name = fake.name()
            nav_value = round(random.uniform(10.0, 1000.0), 4)
            assets_under_mgmt = round(random.uniform(1000000.0, 500000000.0), 2)

            fund = {
                'Bajaj_FundID': 1,  # Only one fund per bank
                'FundTitle': fund_title,
                'FundCategory': fund_category,
                'RiskProfile': risk_profile,
                'StartDate': start_date,
                'ManagerName': manager_name,
                'NAV_Value': nav_value,
                'AssetsUnderMgmt': assets_under_mgmt
            }
        funds.append(fund)
    return funds

# Function to generate Mutual Funds clients
def generate_mf_clients(bank_name, num_clients):
    """
    Generate a list of mutual funds clients for a given bank.
    """
    clients = []
    # Select random unique persons without replacement
    selected_persons = random.sample(all_persons, num_clients)
    for idx, person in enumerate(selected_persons):
        # Assign a name variation based on the mutual funds bank
        # Ensure different name variations for different mutual funds banks
        if bank_name == 'SBI':
            name_variation = person['NameVariations'][0]  # Full Name
            client = {
                'SBI_ClientID': idx + 1,
                'FullName': name_variation,
                'ClientEmail': fake.unique.email(),
                'ContactNumber': person['Phone'],
                'PAN_Number': person['PAN'],
                'Address': person['Address'],
                'DateOfBirth': person['DateOfBirth'],
                'RegistrationDate': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
            }
            clients.append(client)
        elif bank_name == 'Tata':
            name_variation = person['NameVariations'][1]  # Initials
            client = {
                'Tata_ClientID': idx + 1,
                'InvestorName': name_variation,
                'EmailAddress': fake.unique.email(),
                'PhoneNumber': person['Phone'],
                'PAN': person['PAN'],
                'ResidentialAddress': person['Address'],
                'DOB': person['DateOfBirth'],
                'JoinDate': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
            }
            clients.append(client)
        elif bank_name == 'Bajaj':
            name_variation = person['NameVariations'][2]  # Middle initial
            client = {
                'Bajaj_CustomerID': idx + 1,
                'Name': name_variation,
                'Email': fake.unique.email(),
                'Mobile': person['Phone'],
                'PAN_Num': person['PAN'],
                'Addr': person['Address'],
                'DOB': person['DateOfBirth'],
                'DateJoined': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
            }
            clients.append(client)
    return clients

# Function to generate Investment Returns with correct column names per bank
def generate_investment_returns(bank_name, clients, funds):
    """
    Generate investment returns for a given mutual funds bank.
    """
    returns = []
    for client in clients:
        client_id = client[f'{bank_name}_ClientID'] if bank_name != 'Bajaj' else client['Bajaj_CustomerID']
        num_investments = random.randint(1, 3)  # Number of investments per client (max 3 for simplicity)
        for _ in range(num_investments):
            fund = funds[0]  # Only one fund per bank
            if bank_name == 'SBI':
                investment_date = fake.date_between(start_date=fund['LaunchDate'], end_date='today')
                units_purchased = round(random.uniform(10.0, 1000.0), 4)
                investment_amount = round(units_purchased * fund['NAV'], 2)
                current_nav = round(fund['NAV'] * random.uniform(0.95, 1.10), 4)  # +/-5-10%
                current_value = round(units_purchased * current_nav, 2)
                return_percentage = round(((current_value - investment_amount) / investment_amount) * 100, 2)
                last_updated = fake.date_between(start_date=investment_date, end_date='today')

                investment = {
                    'ReturnID': len(returns) + 1,
                    'SBI_FundID': fund['SBI_FundID'],
                    'SBI_ClientID': client_id,
                    'InvestmentDate': investment_date,
                    'UnitsPurchased': units_purchased,
                    'InvestmentAmount': investment_amount,
                    'CurrentNAV': current_nav,
                    'CurrentValue': current_value,
                    'ReturnPercentage': return_percentage,
                    'LastUpdated': last_updated
                }
                returns.append(investment)
            elif bank_name == 'Tata':
                investment_date = fake.date_between(start_date=fund['InceptionDate'], end_date='today')
                units_bought = round(random.uniform(10.0, 1000.0), 4)
                investment_inr = round(units_bought * fund['CurrentNAV'], 2)
                nav_at_purchase = fund['CurrentNAV']
                current_nav = round(nav_at_purchase * random.uniform(0.95, 1.10), 4)
                investment_value = round(units_bought * current_nav, 2)
                gain_loss_percentage = round(((investment_value - investment_inr) / investment_inr) * 100, 2)
                last_updated = fake.date_between(start_date=investment_date, end_date='today')

                investment = {
                    'InvestmentReturnID': len(returns) + 1,
                    'Tata_FundID': fund['Tata_FundID'],
                    'Tata_ClientID': client_id,
                    'DateOfInvestment': investment_date,
                    'UnitsBought': units_bought,
                    'InvestmentINR': investment_inr,
                    'NAVAtPurchase': nav_at_purchase,
                    'CurrentNAVValue': current_nav,
                    'InvestmentValue': investment_value,
                    'GainLossPercentage': gain_loss_percentage,
                    'LastUpdated': last_updated
                }
                returns.append(investment)
            elif bank_name == 'Bajaj':
                investment_date = fake.date_between(start_date=fund['StartDate'], end_date='today')
                units_purchased = round(random.uniform(10.0, 1000.0), 4)
                amount_invested = round(units_purchased * fund['NAV_Value'], 2)
                purchase_nav = fund['NAV_Value']
                current_nav = round(purchase_nav * random.uniform(0.95, 1.10), 4)
                current_value = round(units_purchased * current_nav, 2)
                profit_loss_perc = round(((current_value - amount_invested) / amount_invested) * 100, 2)
                update_date = fake.date_between(start_date=investment_date, end_date='today')

                investment = {
                    'ClientReturnID': len(returns) + 1,
                    'Bajaj_FundID': fund['Bajaj_FundID'],
                    'Bajaj_CustomerID': client_id,
                    'InvestmentDate': investment_date,
                    'UnitsPurchased': units_purchased,
                    'AmountInvested': amount_invested,
                    'PurchaseNAV': purchase_nav,
                    'CurrentNAV': current_nav,
                    'CurrentValue': current_value,
                    'ProfitLossPerc': profit_loss_perc,
                    'UpdateDate': update_date
                }
                returns.append(investment)
    return returns

# Function to print investment details for a mutual funds bank
def print_investment_details(bank_name, clients_df, returns_df, funds_df, client_id_col, fund_id_col, name_col, fund_name_col):
    for idx, client in clients_df.iterrows():
        try:
            client_id = client[client_id_col]
        except KeyError:
            print(f"Error: Column '{client_id_col}' not found in clients DataFrame for {bank_name}.")
            continue

        try:
            client_name = client[name_col]
        except KeyError:
            print(f"Error: Column '{name_col}' not found in clients DataFrame for {bank_name}.")
            continue

        # Determine PAN column based on bank
        if bank_name == 'SBI':
            pan_col = 'PAN_Number'
        elif bank_name == 'Tata':
            pan_col = 'PAN'
        elif bank_name == 'Bajaj':
            pan_col = 'PAN_Num'
        else:
            pan_col = None

        if pan_col and pan_col in client:
            client_pan = client[pan_col]
        else:
            client_pan = 'N/A'

        # Filter investments for this client
        client_returns = returns_df[returns_df[client_id_col] == client_id]

        num_investments = len(client_returns)
        if num_investments > 0:
            print(f"Client: {client_name} (PAN: {client_pan}) has {num_investments} investment(s) in {bank_name} Mutual Fund:")
            for _, investment in client_returns.iterrows():
                fund_id = investment[fund_id_col]
                # Corrected fund retrieval
                fund = funds_df[funds_df[fund_id_col] == fund_id]
                if len(fund) == 0:
                    print(f"  - Fund ID {fund_id} not found in funds DataFrame.")
                    continue
                fund = fund.iloc[0]
                fund_name = fund[fund_name_col]
                # Additional investment details based on bank
                if bank_name == 'SBI':
                    amount = investment['InvestmentAmount']
                    current_value = investment['CurrentValue']
                    return_pct = investment['ReturnPercentage']
                    print(f"  - Fund: {fund_name}, Amount Invested: INR {amount}, Current Value: INR {current_value}, Return: {return_pct}%")
                elif bank_name == 'Tata':
                    amount = investment['InvestmentINR']
                    current_value = investment['InvestmentValue']
                    gain_loss_pct = investment['GainLossPercentage']
                    print(f"  - Fund: {fund_name}, Amount Invested: INR {amount}, Current Value: INR {current_value}, Gain/Loss: {gain_loss_pct}%")
                elif bank_name == 'Bajaj':
                    amount = investment['AmountInvested']
                    current_value = investment['CurrentValue']
                    profit_loss_pct = investment['ProfitLossPerc']
                    print(f"  - Fund: {fund_name}, Amount Invested: INR {amount}, Current Value: INR {current_value}, Profit/Loss: {profit_loss_pct}%")
            print("\n")

# Generate Mutual Funds Clients, Funds, and Returns
for bank in mutual_funds_banks:
    print(f"Generating Mutual Funds data for {bank}...")
    # Generate Funds (only one mutual fund per bank)
    funds = generate_mutual_funds(bank, NUM_FUNDS_PER_BANK)
    # Assign generated funds to respective mutual funds lists
    if bank == 'SBI':
        sbi_mf_funds.extend(funds)
    elif bank == 'Tata':
        tata_mf_mutual_funds.extend(funds)
    elif bank == 'Bajaj':
        bajaj_mf_funds.extend(funds)
    # Generate Clients
    clients = generate_mf_clients(bank, NUM_MF_CLIENTS_PER_BANK)
    # Assign clients to respective lists
    if bank == 'SBI':
        sbi_mf_clients.extend(clients)
    elif bank == 'Tata':
        tata_mf_investors.extend(clients)
    elif bank == 'Bajaj':
        bajaj_mf_customers.extend(clients)
    # Generate Investment Returns
    if bank == 'SBI':
        returns = generate_investment_returns(bank, sbi_mf_clients, sbi_mf_funds)
        sbi_mf_returns.extend(returns)
    elif bank == 'Tata':
        returns = generate_investment_returns(bank, tata_mf_investors, tata_mf_mutual_funds)
        tata_mf_investment_returns.extend(returns)
    elif bank == 'Bajaj':
        returns = generate_investment_returns(bank, bajaj_mf_customers, bajaj_mf_funds)
        bajaj_mf_client_returns.extend(returns)

# Convert Mutual Funds data to DataFrames
sbi_mf_clients_df = pd.DataFrame(sbi_mf_clients)
tata_mf_investors_df = pd.DataFrame(tata_mf_investors)
bajaj_mf_customers_df = pd.DataFrame(bajaj_mf_customers)

sbi_mf_funds_df = pd.DataFrame(sbi_mf_funds)
tata_mf_mutual_funds_df = pd.DataFrame(tata_mf_mutual_funds)
bajaj_mf_funds_df = pd.DataFrame(bajaj_mf_funds)

sbi_mf_returns_df = pd.DataFrame(sbi_mf_returns)
tata_mf_investment_returns_df = pd.DataFrame(tata_mf_investment_returns)
bajaj_mf_client_returns_df = pd.DataFrame(bajaj_mf_client_returns)

# Save Mutual Funds data to CSV files
sbi_mf_clients_df.to_csv('SBI_MF_Clients.csv', index=False)
sbi_mf_funds_df.to_csv('SBI_MF_Funds.csv', index=False)
sbi_mf_returns_df.to_csv('SBI_MF_Returns.csv', index=False)

tata_mf_investors_df.to_csv('TataMF_Investors.csv', index=False)
tata_mf_mutual_funds_df.to_csv('TataMF_MutualFunds.csv', index=False)
tata_mf_investment_returns_df.to_csv('TataMF_InvestmentReturns.csv', index=False)

bajaj_mf_customers_df.to_csv('BajajMF_Customers.csv', index=False)
bajaj_mf_funds_df.to_csv('BajajMF_Funds.csv', index=False)
bajaj_mf_client_returns_df.to_csv('BajajMF_ClientReturns.csv', index=False)

# Display sample Mutual Funds data
print("SBI_MF_Clients Sample Data:")
print(sbi_mf_clients_df.head(), "\n")

print("TataMF_Investors Sample Data:")
print(tata_mf_investors_df.head(), "\n")

print("BajajMF_Customers Sample Data:")
print(bajaj_mf_customers_df.head(), "\n")

print("SBI_MF_Funds Sample Data:")
print(sbi_mf_funds_df.head(), "\n")

print("TataMF_MutualFunds Sample Data:")
print(tata_mf_mutual_funds_df.head(), "\n")

print("BajajMF_Funds Sample Data:")
print(bajaj_mf_funds_df.head(), "\n")

print("SBI_MF_Returns Sample Data:")
print(sbi_mf_returns_df.head(), "\n")

print("TataMF_InvestmentReturns Sample Data:")
print(tata_mf_investment_returns_df.head(), "\n")

print("BajajMF_ClientReturns Sample Data:")
print(bajaj_mf_client_returns_df.head(), "\n")

# -------------------- Print Detailed Mutual Funds Investment Details --------------------

print("\n--- Detailed Mutual Funds Investment Details ---\n")

# Create a mapping of PAN to persons for easy lookup
pan_to_person = {person['PAN']: person for person in all_persons}

for bank in mutual_funds_banks:
    print(f"--- {bank} Mutual Funds Investments ---\n")
    if bank == 'SBI':
        clients_df = sbi_mf_clients_df
        returns_df = sbi_mf_returns_df
        funds_df = sbi_mf_funds_df
        client_id_col = 'SBI_ClientID'
        fund_id_col = 'SBI_FundID'
        name_col = 'FullName'
        fund_name_col = 'FundName'
    elif bank == 'Tata':
        clients_df = tata_mf_investors_df
        returns_df = tata_mf_investment_returns_df
        funds_df = tata_mf_mutual_funds_df
        client_id_col = 'Tata_ClientID'
        fund_id_col = 'Tata_FundID'
        name_col = 'InvestorName'
        fund_name_col = 'NameOfFund'
    elif bank == 'Bajaj':
        clients_df = bajaj_mf_customers_df
        returns_df = bajaj_mf_client_returns_df
        funds_df = bajaj_mf_funds_df
        client_id_col = 'Bajaj_CustomerID'
        fund_id_col = 'Bajaj_FundID'
        name_col = 'Name'
        fund_name_col = 'FundTitle'

    print_investment_details(
        bank_name=bank,
        clients_df=clients_df,
        returns_df=returns_df,
        funds_df=funds_df,
        client_id_col=client_id_col,
        fund_id_col=fund_id_col,
        name_col=name_col,
        fund_name_col=fund_name_col
    )

print("Synthetic mutual funds data generation completed and saved to CSV files.")
