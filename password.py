import json, hashlib, getpass, os, sys, string, random
from cryptography.fernet import Fernet

# Function to generate strong passwords for the user
def generate_password():

    # Generate at least 1 upper case, lower case, number, and symbol character.
    lowercase = random.choice(string.ascii_lowercase)
    uppercase = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    symbol = random.choice(string.punctuation)

    # Generate 12 random characters for the rest of the password
    all_chars = string.ascii_letters + string.digits + string.punctuation
    first_part = "123456789abc"
    for char in first_part:
        char = random.choice(all_chars)

    # Combine each character to create a strong 16 character password
    password_list = list(lowercase + uppercase + digit + symbol + ''.join(first_part))
    random.shuffle(password_list)
    return ''.join(password_list)
    

# Function to check the strength of an entered password
def check_password_strength(password):
    length = len(password)
    has_upper = False
    has_lower = False
    has_digit = False
    has_symbol = False

    # Go through the password and check for upper case, lower case
    # numbers, and symbols.
    for char in password:
        if char in string.ascii_uppercase:
            has_upper = True
        elif char in string.ascii_lowercase:
            has_lower = True
        elif char in string.digits:
            has_digit = True
        elif char in string.punctuation:
            has_symbol = True
            
    score = 0
    if has_upper:
        score += 1
    if has_lower:
        score += 1
    if has_digit:
        score += 1
    if has_symbol:
        score += 1
        
    # Short passwords are the weakest
    if length < 6:
        strength = "Very Weak"
    # Passwords that meet only 1 criteria are weak
    elif score < 2:
        strength = "Weak"
    # Passwords that meet 2 criteria and have 8 characters are decent
    elif score == 2 and length >= 8:
        strength = "Moderate"
    # Passwords that meet 3 criteria and 8 characters are strong
    elif score >= 3 and length >= 8:
        strength = "Strong"
    # The strongest passwords meet all 4 criteria and are 12 characters long at least.
    elif score == 4 and length >= 12:
        strength = "Very Strong"
    # Edge case, it's moderate
    else:
        strength = "Moderate"


    print("Password Strength: " + strength + "\n")

    # Give the user a choice to re enter their password
    choice = input("Do you want to re-enter a stronger password? (y/n): ").strip().lower()
    if choice == 'y':
        password = getpass.getpass("Enter a new password: ")
        # Go through the process recursively until the user is satisfied.
        return check_password_strength(password)
    elif choice == 'n':
        # Keep the entered password
        return password
    else:
        # Invalid input edge case, simply re enter the method.
        print("Invalid input. Please enter 'y' or 'n'.\n")
        return check_password_strength(password)


# Function for Hashing the Master Password.
def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode())
    return sha256.hexdigest()


# Generate a secret key.
def generate_key():
    return Fernet.generate_key()


# Initialize Fernet cipher with the provided key.
def initialize_cipher(key):
    return Fernet(key)


# Function to encrypt a password.
def encrypt_password(cipher, password):
    return cipher.encrypt(password.encode()).decode()


# Function to decrypt a password.
def decrypt_password(cipher, encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()


# Function to assign a master password to the user
def register(master_password):
    # Hash the master password and create a user_data.json file
    hashed_master_password = hash_password(master_password)
    user_data = {'master_password': hashed_master_password}
    file_name = 'user_data.json'

    # Add the password to the file
    with open(file_name, 'w') as file:
        json.dump(user_data, file)
    print("Master Password Set \n")


# Function to log the user in.
def login(entered_password):
    try:
        # Open the file with the hashed master password
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)

        # Get the master password's hash and hash the entered password to ensure they are the same. 
        stored_password_hash = user_data.get('master_password')
        entered_password_hash = hash_password(entered_password)

        # If the hashes are the same, the user logs in.
        if entered_password_hash == stored_password_hash:
            print("Login Successful\n")
        else:
            print("Incorrect Password \n")
            sys.exit()
    # User must make set a master password beforing being able to log in
    except Exception:
        print("Master password has not been set\n")
        sys.exit()

# Function to delete passwords
def delete_password(website):
    # If there is no saved data at all, simply tell the user
    if not os.path.exists('passwords.json'):
        print("No saved passwords found\n")
        return

    try:
        # Try to find the password from the file
        with open('passwords.json', 'r') as file:
            data = json.load(file)
    # Any modifications to the file will cause an error
    # Its a sign the password data file was tampered with
    except json.JSONDecodeError:
        print("Could not read password data")
        return

    # Filter out the entry with the matching website.
    # i.e. get the passwords for only the specified website.
    updated_data = [entry for entry in data if entry['website'] != website]

    # If the website was inputted incorrectly or doesn't exist,
    # Tell the user as much
    if len(updated_data) == len(data):
        print("No password found for " + website + "\n")
    else:
        with open('passwords.json', 'w') as file:
            json.dump(updated_data, file, indent=4)
        print("Password for " + website + " has been deleted.\n")

# View saved websites
def view_websites():
    try:
        with open('passwords.json', 'r') as data:
            websites = json.load(data)
            print("Saved Passwords: \n")
            for website in websites:
                print(website['website'])
            print('\n')
    except FileNotFoundError:
        print("No passwords have been saved \n")

# Load or create encryption key
# The key is what will translate hashed passwords into readible text
# There can only be one key, so this little block will save or load said key. 
key_filename = 'encryption_key.key'
if os.path.exists(key_filename):
    with open(key_filename, 'rb') as key_file:
        key = key_file.read()
else:
    key = generate_key()
    with open(key_filename, 'wb') as key_file:
        key_file.write(key)
# The cipher is the tool that will actually encode and decode the passwords.
cipher = initialize_cipher(key)

# Save a new password
def add_password(website, password):
    if not os.path.exists('passwords.json'):
        data = []
    else:
        try:
            with open('passwords.json', 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []
    # Encrypt the password and store it with the corresponding website.
    encrypted_password = encrypt_password(cipher, password)
    password_entry = {'website': website, 'password': encrypted_password}
    data.append(password_entry)

    with open('passwords.json', 'w') as file:
        json.dump(data, file, indent=4)

# Retrieve a password
def get_password(website):
    if not os.path.exists('passwords.json'):
        return None

    try:
        with open('passwords.json', 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        data = []
    # Loop through the passwords file and search for the inputted website
    # Then, decrypt the password and return it
    for entry in data:
        if entry['website'] == website:
            return decrypt_password(cipher, entry['password'])
    return None

# Main loop

while True:
    print("1. Set master password")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        if os.path.exists('user_data.json') and os.path.getsize('user_data.json') != 0:
            print("Master password has been set")
            sys.exit()
        master_password = getpass.getpass("Enter your master password: ")
        master_password = check_password_strength(master_password)
        register(master_password)

    elif choice == '2':
        if not os.path.exists('user_data.json'):
            print("Master password has not been set")
            sys.exit()
        master_password = getpass.getpass("Enter your master password: ")
        login(master_password)

        while True:
            print("1. Add Password")
            print("2. Get Password")
            print("3. View Saved Websites")
            print("4. Delete Password")
            print("5. Log Out")

            password_choice = input("Enter your choice: ")

            if password_choice == '1':
                website = input("Enter website: ")
                password = ""
                make_password = input("Would you like a generated password? (y/n) ").strip().lower()
                if make_password == 'y':
                    password = generate_password()
                else:
                    # Receive input from the user to get a provided password.
                    password = getpass.getpass("Enter password: ")
                    # Check the strength of the password.
                    password = check_password_strength(password)
                
                add_password(website, password)
                print("Password Saved\n")

            elif password_choice == '2':
                website = input("Enter website: ")
                decrypted_password = get_password(website)
                if website and decrypted_password:
                    print("Password: " + decrypted_password + "\n")
                   
                else:
                    print("Password not found\n")

            elif password_choice == '3':
                view_websites()
            elif password_choice == '4':
                website = input("Enter website to delete: ")
                delete_password(website)

            elif password_choice == '5':
                break

    elif choice == '3':
        break