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
    alternate_first_name = first_name[:-1] + random.choice(string.ascii_lowercase)
    alternate_name = f"{alternate_first_name} {middle_name} {last_name}"
    variations.append(alternate_name)
    return variations

# Generate unique individuals
unique_persons = []

for _ in range(NUM_UNIQUE_PERSONS):
    full_name, first_name, middle_name, last_name = generate_full_name()
    name_variations = generate_name_variations(first_name, middle_name, last_name)
    pan = fake.unique.bothify(text='??######?')  # PAN format: 5 letters, 4 digits, 1 letter
    national_id = fake.unique.bothify(text='###########')  # Assuming an 11-digit ID
    email = fake.unique.email()
    phone = fake.unique.phone_number()
    address = fake.address().replace('\n', ', ')
    dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
    account_creation_date = fake.date_between(start_date='-10y', end_date='today')

    unique_persons.append({
        'FullName': full_name,
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
    pan = fake.unique.bothify(text='??######?')
    national_id = fake.unique.bothify(text='###########')
    email = fake.unique.email()
    phone = fake.unique.phone_number()
    address = fake.address().replace('\n', ', ')
    dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
    account_creation_date = fake.date_between(start_date='-10y', end_date='today')

    additional_persons.append({
        'FullName': base_name + " Jr.",
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

    # Assign different name variations to each bank
    for bank_idx, bank in enumerate(banks):
        # Assign a unique name variation if possible
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
                'AmountStored': round(random.uniform(2000, 150000), 2),
                'Interest_Rate': round(random.uniform(1.5, 4.5), 2),
                'Last_Updated': fake.date_between(start_date=person['AccountCreationDate'], end_date='today')
            }
            sbi_data.append(sbi_account)

# Convert to DataFrames
icici_df = pd.DataFrame(icici_data)
hdfc_df = pd.DataFrame(hdfc_data)
sbi_df = pd.DataFrame(sbi_data)

# Display sample data
print("ICICI_Accounts Sample Data:")
print(icici_df.head(), "\n")

print("HDFC_Accounts Sample Data:")
print(hdfc_df.head(), "\n")

print("SBI_Accounts Sample Data:")
print(sbi_df.head(), "\n")

# Save to CSV files
icici_df.to_csv('ICICI_Accounts.csv', index=False)
hdfc_df.to_csv('HDFC_Accounts.csv', index=False)
sbi_df.to_csv('SBI_Accounts.csv', index=False)

# Print name variations for multi-bank individuals
print("\n--- Name Variations Across Banks for Multi-Bank Individuals ---\n")
for idx, person in enumerate(multi_bank_persons_names, 1):
    print(f"Individual {idx}:")
    print(f"  PAN: {person['PAN']}")
    print(f"  NationalID: {person['NationalID']}")
    for bank, name in person['NameBankMapping'].items():
        print(f"  {bank} Account Name: {name}")
    print("\n")

print("Synthetic data generation completed and saved to CSV files.")
