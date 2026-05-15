import bcrypt
import random
import sys
import string 
import json
import getpass
from cryptography.fernet import Fernet

GREEN = '\033[92m'
CYAN = '\033[96m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

registered_users = {}
accounts = {}
user_id = 1


def register():
    global user_id
    username = input("Username: ").strip()
    status = check_username_validity(username, registered_users)
    
    if status == "Empty":
        print(f"{RED}Please Enter A Valid Username!{RESET}")
        return
    elif status == "Taken":
        print(f"{YELLOW}This username is already taken!{RESET}")
        return
    
    
    master_password = getpass.getpass("Master Password: (Hidden) ").strip()
    if master_password == "":
        print(f"{RED}Please Enter A Valid Password!{RESET}")
        return
    elif len(master_password) < 5:
        print(f"{YELLOW}Please Choose A Longer Master Password!{RESET}")
        return
    byte_master = master_password.encode("utf-8")
    hashed_master_bytes = bcrypt.hashpw(byte_master, bcrypt.gensalt())
    hashed_master_string = hashed_master_bytes.decode("utf-8")

    if bcrypt.checkpw((getpass.getpass("Enter Your Master Password Again For Verification: (Hidden) ").encode("utf-8")), hashed_master_bytes):
        registered_users[username] = {
            "user_id": user_id,
            "master_password": hashed_master_string
         
        }
        user_id += 1
        print(f"{GREEN}Account Created Successfully!{RESET}")
        return
        
    else:
        print(f"{RED}Incorrect!{RESET}")
        return
        

    
def login():

    if len(registered_users) == 0:
        print(f"{RED}No Users Found!{RESET}")
        return
    

    username_login = input("Enter Your Username: ")
    master_pass_login = getpass.getpass("Enter Your Master Password: (Hidden) ")

    
    if username_login in registered_users:
        
        stored_hash_string = registered_users[username_login]["master_password"]
        stored_hash_bytes = stored_hash_string.encode("utf-8")
        
        
        if bcrypt.checkpw(master_pass_login.encode("utf-8"), stored_hash_bytes):
            print(f"{GREEN}Login Successful!{RESET}")
            menu_screen(registered_users[username_login]["user_id"])
            return
            
    print(f"{YELLOW}Please Check Your Login Informations!{RESET}")
    return
    


def welcome_screen():
    while True:
        print("+--------[ Welcome to Password Manager Plus!]--------+")
        print("----(1) Login")
        print("----(2) Register")
        print("----(3) Exit")
        choice = input("Please Choose an Option: ")
        
        if choice == "1":
            login()
        elif choice == "2":
            register()
        elif choice == "3":
            save_data(accounts, registered_users)
            print(f"{GREEN}Exiting... Have A Nice Day!{RESET}")
            sys.exit()
        else:
            print(f"{YELLOW}Please Choose A Valid Option.{RESET}")
            continue


def menu_screen(current_user):
    while True:

        if current_user in accounts:
            account_count = len(accounts[current_user])
        else: account_count = 0

        print("+--------[Menu]--------+")
        print("----(1) Add An Account")
        print(f"----(2) View Your Accounts [{account_count}]")
        print("----(3) Strong Password Generator")
        print("----(4) Password Validator")
        print("----(5) Exit")
        choice = input("Please Choose an Option: ")

        if choice == "1":
            add_account(current_user)
        elif choice == "2":

            if current_user not in accounts or len(accounts[current_user]) == 0:
                print(f"{YELLOW}You don't have any saved accounts yet!{RESET}")
                continue

            
            accounts_list = accounts[current_user].keys()
            print(f"{CYAN}Saved Accounts:{RESET} {' | '.join(accounts_list)}")
            website_ = input("Website: ").title().strip()

            try:
                encrypted_password_str = accounts[current_user][website_]['password']
                encrypted_password_byte = encrypted_password_str.encode("utf-8")
                decrypted_password = f.decrypt(encrypted_password_byte)
                user_password = decrypted_password.decode("utf-8")

                encrypted_username_str = accounts[current_user][website_]['username']
                encrypted_username_byte = encrypted_username_str.encode("utf-8")
                decrypted_username = f.decrypt(encrypted_username_byte)
                user_username = decrypted_username.decode("utf-8")

                print(f"{GREEN}Account For {website_} Has Found!{RESET}")
                print(f"{CYAN}+---------------------------------+{RESET}")
                print(f"->  Website  : {website_}")
                print(f"->  Username : {user_username}")
                print(f"->  Password : {user_password}")
                print(f"{CYAN}+---------------------------------+{RESET}")
            except KeyError:
                print(f"{RED}Account For This Website Could Not Be Found!{RESET}")
                continue
            

        elif choice == "3":
            while True:
                try:
                    length = int(input("Length[16-64]: "))
                except ValueError:
                    print(f"{YELLOW}Please enter a valid number!{RESET}")
                    continue
                    
            
                if (length < 16) or (length > 64):
                    print(f"{YELLOW}Password Length Should Be Between [16-64]{RESET}")
                    continue
            
                result = password_generator(length)
                print(f"{GREEN}Generated Strong Password: {RESET}{result}")
                
                choice = input("Generate Again (g) | Open Menu (m): ")
                if choice == "g":
                    continue
                elif choice == "m":
                    break
                else: 
                    print(f"{YELLOW}Invalid Choice, Returning To Menu...{RESET}")
                    break


        elif choice == "4":
            while True:
                validator_password = input("Enter A Password To Validate: ")
                result, score = password_validator(validator_password)

                if result == "Invalid":
                    print(f"{YELLOW}Please Enter A Valid Password!{RESET}")
                elif result == "Very Strong":
                    print(f"{GREEN}Very Strong Password! [Score: {score}/100]{RESET}")
                elif result == "Strong":
                    print(f"{GREEN}Strong Password! [Score: {score}/100]{RESET}")
                elif result == "Medium":
                    print(f"{YELLOW}Medium Level! [Score: {score}/100]{RESET}")
                elif result == "Weak":
                    print(f"{RED}Weak Password! [Score: {score}/100]{RESET}")
                elif result == "Very Weak":
                    print(f"{RED}Very Weak Password! [Score: {score}/100]{RESET}")

                
                choice = input("Validate Again (v) | Open Menu (m): ")
                if choice == "v":
                    continue
                elif choice == "m":
                    break
                else: 
                    print(f"{YELLOW}Invalid Choice, Returning To Menu...{RESET}")
                    break

        elif choice == "5":
                save_data(accounts, registered_users)
                print(f"{YELLOW}Saving User Data...{RESET}")
                print(f"{GREEN}User Data Saved!{RESET}")
                print(f"{GREEN}Exiting... Have A Nice Day!{RESET}")
                sys.exit()
        else:
                print(f"{YELLOW}Please Choose A Valid Option.{RESET}")
                continue
        

def add_account(user_id):
    
    website = input("Website: ").title().strip()
    if website == "":
        print(f"{YELLOW}Please Enter A Valid Website!{RESET}")
        return
    if (user_id in accounts) and (website in accounts[user_id]):
        print(f"{YELLOW}You Already Have An Account Saved For {website}!{RESET}")
        return
    username = input("Username: ").strip()
    if username == "":
        print(f"{YELLOW}Please Enter A Valid Username!{RESET}")
        return
    password = input("Password: ").strip()
    if password == "":
        print(f"{YELLOW}Please Enter A Valid Password!{RESET}")
        return
    
    encrypt_byte = password.encode("utf-8")
    encrypted_byte = f.encrypt(encrypt_byte)
    encrypted_password = encrypted_byte.decode("utf-8")

    encrypt_user_byte = username.encode("utf-8")
    encrypted_user_byte = f.encrypt(encrypt_user_byte)
    encrypted_user = encrypted_user_byte.decode("utf-8")

    if user_id not in accounts:
        accounts[user_id] = {}

    accounts[user_id][website] = {
        "username": encrypted_user,
        "password": encrypted_password
    }
    print(f"{GREEN}Your Account for {website} Has Been Saved!{RESET}")
    while True:
        choice = input("Add Again (a) | Open Menu (m): ")
        if choice == "a":
            return add_account(user_id)
        elif choice == "m":
            return
        else: 
            continue
    


def password_generator(length):
    
        all_characters = string.ascii_letters + string.digits + string.punctuation

        generated_password = "".join(random.choices(all_characters, k=length))
        return generated_password
        

    


def password_validator(password_for_validation):

    score = 0

    lower_letters = []
    upper_letters = []
    numbers = []
    special_characters = []
    length = len(password_for_validation)

    if length <= 0:
        return "Invalid", 0
        

    for character in password_for_validation:
        if character.isupper():
            upper_letters.append(character)
        if character.islower():
            lower_letters.append(character)
        if character.isdigit():
            numbers.append(character)
        if character in string.punctuation:
            special_characters.append(character)

    if 8 < length:
        score += 20
    elif 5 < length:
        score += 5

    if len(upper_letters) > 3:
        score += 20
    elif len(upper_letters) >= 1:
        score += 10

    if len(lower_letters) > 3:
        score += 20
    elif len(lower_letters) >= 1:
        score += 10

    if len(special_characters) > 3:
        score += 20
    elif len(special_characters) >= 1:
        score += 10

    if len(numbers) > 3:
        score += 20
    elif len(numbers) >= 1:
        score += 10

    if len(upper_letters) == 0 or len(lower_letters) == 0 or len(special_characters) == 0 or len(numbers)== 0:
        if score >= 25:
            score = 25
        else: score = 0
    

    if 80 <= score <= 100:
        return "Very Strong", score
    elif 60 <= score < 80:
        return "Strong", score
    elif 40 <= score < 60:
        return "Medium", score
    elif 20 <= score < 40:
        return "Weak", score
    elif 0 <= score < 20:
        return "Very Weak", score



def save_data(accounts, registered_users):
    with open("user_database.json", "w") as file1:
         json.dump(registered_users, file1, indent=4)
    with open("account_database.json", "w") as file2:
         json.dump(accounts, file2, indent=4)


def load_data():
    global registered_users, accounts, user_id
    try: 
        with open("user_database.json", "r") as file1:
            registered_users = json.load(file1)
            user_id = len(registered_users) + 1 
            print(f"{GREEN}----User Data Has Loaded!----{RESET}")
    except FileNotFoundError:
        pass

    try:
        with open("account_database.json", "r") as file2:
            account_datas = json.load(file2)
            for id, account_details in account_datas.items():
                accounts[int(id)] = account_details
                
            print(f"{GREEN}----Account Data Has Loaded!----{RESET}")
    except FileNotFoundError:
        pass

def get_or_create_key():
    try:
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        new_key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(new_key)
        return new_key
    
def check_username_validity(username, current_users):

    if username == "":
        return "Empty"
    
    if username in current_users:
        return "Taken"
    
    return "Valid"


def main():
    load_data()         
    welcome_screen()

key = get_or_create_key()
f = Fernet(key)

if __name__ == "__main__":
    
    main()


