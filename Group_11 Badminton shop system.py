import os
import time

import os

def clear_screen():
    os.system('cls') 

from datetime import datetime

current_user = None
current_user_id = None
current_admin = None

def userRegister():# User Register
    clear_screen()
    print("================================================")
    print("================= User Register ================")
    print("================================================")
    print("1. Register")
    print("2. Back")
    choice = input("Enter your choice : ")
    if choice == "1":
        add_user()
    elif choice == "2":
        main()
    else:
        print("Invalid choice")

def add_user():
    clear_screen()
    print("================================================")
    print("================= User Register ================")
    print("================================================")
    
    for attempt in range(3):
        username = input("\nEnter username: " if attempt == 0 else "Enter a new username: ").strip()
        if not checkRepeatingName(username):
            break
        remaining = 2 - attempt
        if remaining > 0:
            print(f"{remaining} attempt(s) left.")
    else:
        print("Too many failed attempts. Registration aborted.")
        time.sleep(2)
        main()
        return

    for attempt in range(3):
        password = input("Enter password (min 8 characters): ").strip()
        if len(password) < 8:
            print("Password must be at least 8 characters.")
            remaining = 2 - attempt
            if remaining > 0:
                print(f"{remaining} attempt(s) left.")
            continue
        confirm = input("Confirm password: ").strip()
        if password == confirm:
            register(username, password)
            return
        else:
            print("Passwords do not match.")
            remaining = 2 - attempt
            if remaining > 0:
                print(f"{remaining} attempt(s) left.")

    print("Too many failed attempts. Registration aborted.")
    time.sleep(2)
    main()

def checkRepeatingName(username):
    try:
        with open("users.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 2 and parts[1].strip() == username:
                    print("Username already exists")
                    return True
    except FileNotFoundError:
        return False
    return False

def getNextUserId():
    try:
        with open("users.txt", "r") as file:
            lines = [line.strip() for line in file if line.strip()]
            if not lines:
                return 1
            last_line = lines[-1]
            last_id = int(last_line.split(",")[0])
            return last_id + 1
    except FileNotFoundError:
        return 1

def register(username, password):
    user_id = getNextUserId()
    with open("users.txt", "a", newline="\n") as file:
        file.write(f"{user_id},{username},{password}\n")
    print("\nAccount created successfully")
    time.sleep(2)
    userMenu()


def userLogin(): #user Login
    clear_screen()
    print("\n================================================")
    print("================== User Login ==================")
    print("================================================")
    print("1. Login")
    print("2. Back")
    choice = input("Enter your choice : ")
    if choice == "1":
        userLoginPage()
    elif choice == "2":
        main()
    else:
        print("Invalid choice")

def userLoginPage():# Modified userLoginPage() to capture user ID
    global current_user, current_user_id
    clear_screen()
    print("\n================================================")
    print("================== User Login ==================")
    print("================================================")
    
    username = input("Enter username: ").strip()
    
    if not checkUsernameExists(username):
        print("Username does not exist.")
        time.sleep(2)
        main()
        return

    for attempt in range(3):
        password = input("Enter password: ").strip()
        
        if checkUserPassword(username, password):
            current_user = username
            current_user_id = get_user_id(username)
            print("Login successful.")
            time.sleep(2)
            userMenu()
            return
        else:
            remaining = 2 - attempt
            if remaining > 0:
                print(f"Incorrect password. {remaining} attempt(s) left.")
            else:
                print("Too many failed attempts. Returning to main menu.")
            time.sleep(2)

    main()

def get_user_id(username):
    try:
        with open("users.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 3 and parts[1].strip() == username:
                    return parts[0].strip()  # Return as string
    except FileNotFoundError:
        return None
    return None

def checkUsernameExists(username):
    try:
        with open("users.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 3 and parts[1].strip() == username:
                    return True
    except FileNotFoundError:
        pass
    return False

def checkUserPassword(username, password):
    try:
        with open("users.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    stored_username = parts[1].strip()
                    stored_password = parts[2].strip()
                    if stored_username == username:
                        return stored_password == password
    except FileNotFoundError:
        pass
    return False

def guestMode():
    clear_screen()
    print("\n==============================================")
    print("================= Guest Mode =================")
    print("==============================================")

    print("1. View By guest mode")
    print("2. Back")

    choice = input("Enter your choice : ")
    
    if choice == "1":
        userMenu()  # Prevent guest purchase
    elif choice == "2":
        main()
    else:
        print("Invalid choice")
    time.sleep(2)  # Pause 2 seconds

def adminLogin():
    clear_screen()
    print("\n================================================")
    print("======= Badminton Sport Equipment System =======")
    print("================================================")
    print("================= Admin Login ==================")
    print("================================================")
    print("1. Login")
    print("2. Back")
    choice = input("Enter your choice : ")
    if choice == "1":
        adminLoginPage()
    elif choice == "2":
        main()
    else:
        print("Invalid choice")

def adminLoginPage():
    global current_admin
    clear_screen()
    print("\n================================================")
    print("================= Admin Login ==================")
    print("================================================")

    adminname = input("Enter adminname: ").strip()

    # Check for super admin
    if adminname == "super_admin":
        for attempt in range(3):
            password = input("Enter password: ").strip()
            if password == "12345678":
                current_admin = adminname
                print("Super Admin Login successful")
                time.sleep(2)
                superadminMenu()
                return
            else:
                remaining = 2 - attempt
                if remaining > 0:
                    print(f"Incorrect password. {remaining} attempt(s) left.")
                else:
                    print("Too many failed attempts. Returning to main menu.")
                time.sleep(2)
        main()
        return

    # Check if admin name exists in file
    if not checkStaffNameExists(adminname):
        print("Adminname does not exist.")
        time.sleep(2)
        main()
        return

    # Check password for regular admin
    for attempt in range(3):
        password = input("Enter password: ").strip()
        if checkStaffPassword(adminname, password):
            current_admin = adminname
            print("Login successful")
            time.sleep(2)
            adminMenu()
            return
        else:
            remaining = 2 - attempt
            if remaining > 0:
                print(f"Incorrect password. {remaining} attempt(s) left.")
            else:
                print("Too many failed attempts. Returning to main menu.")
            time.sleep(2)
    
    main()


def checkStaffNameExists(adminname):
    try:
        with open("admins.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 2 and parts[1].strip() == adminname:
                    return True
    except FileNotFoundError:
        pass
    return False

def checkStaffPassword(adminname, password):
    try:
        with open("admins.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 3:
                    stored_name = parts[1].strip()
                    stored_password = parts[2].strip()
                    if stored_name == adminname:
                        return stored_password == password
    except FileNotFoundError:
        pass
    return False

