# Password Manager Plus
#### Video Demo:  https://youtu.be/PoUhWFqkXyY
#### Description: Final Project For CS50P

Welcome to Password Manager Plus! 

#### Features:
Password Manager Plus includes the following features:
- **Password Manager** : You can store and view your accounts for websites safely with encryption. Since all user data is encrypted, only you, not even the developer, can access your data.
- **Strong Password Generator** : You can generate strong passwords by only choosing the length.
- **Password Validator** : You can check your password's strength. As a result, you receive a score.
- **Continuous Usage** : All data gets encrypted and stored on device and gets loaded whenever you start the Password Manager Plus.
- **Privacy Matters** : Your master password is not shown when you register and log in and also stored in your device encrypted.

### Files In This Program:
- 'project.py': This is the main file containing the program's core logic, the UI menu, and all the loops.
- 'test_project.py': This file contains the test functions. It uses `pytest` to test three independent logic functions from my main code 
(`password_generator`, `password_validator`, and `check_username_validity`).
- 'requirements.txt': Contains the list of external libraries needed to run this program (`bcrypt`, `cryptography`, `pytest`).
- `user_database.json` & `account_database.json`: These are automatically created by the program to store user data.
- 'secret.key': An automatically generated key file used by Fernet to encrypt and decrypt the saved passwords.

