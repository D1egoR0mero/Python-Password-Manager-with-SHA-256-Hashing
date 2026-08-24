# Simple Password Manager

A simple, secure password manager built with Python. This application allows users to generate, store, retrieve, 
and delete encrypted passwords for websites, protected by a master password.

---

## Features

- Master password setup and login
- Password strength checker
- Secure password encryption using "cryptography.fernet"
- Password generator (includes uppercase, lowercase, numbers, and symbols)
- Store and manage passwords in a JSON file
- View saved website entries
- Delete individual saved passwords
- File-based key storage for persistent encryption

---

## Setup

### Requirements

- Python 3.8+
- Modules:
  - `cryptography`
  - `pyperclip` 

Install dependencies:

```bash`
pip install cryptography pyperclip


Usage:
Now, the terminal should look like this:
1. Set master password
2. Login
3. Exit
The user can only enter: 1, 2, or 3. 
The user must set a master password, enter 1, for the program before being able to actually store passwords.
Once a master password is set, enter 2 to login. Re-enter the set master password.
Exit, enter 3, just means to stop running.
After that, the terminal will look like this: 
1. Add Password
2. Get Password
3. View Saved Websites
4. Delete Password
5. Log Out

Again, only 1-5 are accepted as input from the user. 
Enter 1: Add a password
The terminal will prompt the user for the website they're storing the password for. 
Enter a website name, any name really. Then, "Would you like a generated password? (y/n)" will pop up.
Only y/n are allowed. Pressing anything else will just cause the program to proceed
Entering y will cause a random 16 character password to be made and saved. 
After that, the user will be able to store whatever password they type.

Enter 2: Get Password
The user will be prompted for a website. Entering the name will return the password 
associated with the name. The password will be displayed in the terminal. Originally,
it was supposed to copy onto the clipboard, but using sudo to install the needed capability didn't work.

Enter 3: View Saved Websites
The stored websites will be displayed on the terminal. 
The associated passwords will NOT be displayed.

Enter 4: Delete Password
The user will be prompted for a website. The program will delete both the website name
and password associated with it. 

Enter 5: Log Out
The user will be taken back to the start menu, where they can enter 3 to terminate the program.

Testing Notice:
password_test.py has a habit of causing the program to be run in the terminal.
When this happens, simply enter 3 to allow the test cases to run. Also, the passwords.json file 
will be deleted after each run. Moreover, a __pychace__ folder is created after each test run. This data
messes the main program, so it's best to simply delete it. Now, the encryption_key.key file is important. There 
can only be one of it. If you call the function generate_key() more than once, it will cause errors when encoding 
and decoding passwords. password.py will only generate one key on its own, this is mainly for if you decide to test generate key.
Also, there isn't a way to change the master password through password.py, so if you forget, delete the user_data.json file. Deleting
the file will allow you to set a new master password. 
