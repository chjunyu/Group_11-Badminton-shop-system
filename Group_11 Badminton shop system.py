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

def superadminMenu():
    global current_admin
    print("\n==============================================")
    print("============= Super Admin Menu ===============")
    print("==============================================\n")
    print(f"Hello! {current_admin} What would you like to do?\n")
    print("+------------------------------------+")
    print("| Sport Equipment                    |")
    print("+------------------------------------+")
    print("| 1. Add Equipment                   |")
    print("| 2. Edit Equipment                  |")
    print("| 3. Delete Equipment                |")
    print("| 4. View Equipment                  |")
    print("| 5. Product Recommendation          |")
    print("+------------------------------------+")
    print("| User                               |")
    print("+------------------------------------+")
    print("| 6. View Customer                   |")
    print("| 7. Add Customer                    |")
    print("+------------------------------------+")
    print("| Staff                              |")
    print("+------------------------------------+")
    print("| 8. Add Staff                       |")
    print("| 9. Delete Staff                    |")
    print("| 10. View Staff                     |")
    print("+------------------------------------+")
    print("| Another option                     |")
    print("+------------------------------------+")
    print("| 11. Sales Report                   |")
    print("| 12. Logout                         |")
    print("+------------------------------------+")
    
    choice = input("\nEnter your choice : ")
    if choice == "1":
        addEquipment()
    elif choice == "2":
        editEquipment()
    elif choice == "3":
        deleteEquipment()
    elif choice == "4":
        viewEquipment()
    elif choice == "5":
        viewAllRecommendations()
    elif choice == "6":
        viewCustomer()
    elif choice == "7":
        adminadduser()
    elif choice == "8":
        addStaff()
    elif choice == "9":
        deleteStaff()
    elif choice == "10":
        viewStaff()
    elif choice == "11":
        salesReport()
    elif choice == "12":
        current_admin = None
        print("\nLogging out...")
        time.sleep(1)
        main()
    else:
        print("Invalid choice")
        time.sleep(1)
        superadminMenu()
        
# Normal admin menu
def adminMenu():
    global current_admin
    print("\n==============================================")
    print("================== Admin Menu ===============")
    print("==============================================\n")
    print(f"Hello! {current_admin} What would you like to do?\n")
    print("+------------------------------------+")
    print("| Sport Equipment                    |")
    print("+------------------------------------+")
    print("| 1. Add Equipment                   |")
    print("| 2. Edit Equipment                  |")
    print("| 3. Delete Equipment                |")
    print("| 4. View Equipment                  |")
    print("| 5. Product Recommendation          |")
    print("+------------------------------------+")
    print("| Another option                     |")
    print("+------------------------------------+")
    print("| 6. Sales Report                    |")
    print("| 7. Logout                          |")
    print("+------------------------------------+")
    
    choice = input("\nEnter your choice : ")
    if choice == "1":
        addEquipment()
    elif choice == "2":
        editEquipment()
    elif choice == "3":
        deleteEquipment()
    elif choice == "4":
        viewEquipment()
    elif choice == "5":
        viewAllRecommendations()
    elif choice == "6":
        salesReport()
    elif choice == "7":
        current_admin = None
        print("\nLogging out...")
        time.sleep(1)
        main()
    else:
        print("Invalid choice")
        time.sleep(1)
        adminMenu()

# Helper function to get next ID
def get_next_id(filename):
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
            if not lines:
                return 1
            last_id = int(lines[-1].split(",")[0].strip())
            return last_id + 1
    except FileNotFoundError:
        return 1

# Admin Functions
def addEquipment():
    global current_admin
    print("\n=== Add New Equipment ===")
    equipment = []

    # Generate ID
    new_id = get_next_id("products.txt")

    name = input("Enter equipment name: ").replace(" ", "_")
    color = input("Enter color: ")

    print("1. Racket")
    print("2. Shuttlecocks")
    print("3. Badminton_Bag")
    print("4. Racket_Grips")

    category_map = {
        "1": "Racket",
        "2": "Shuttlecocks",
        "3": "Badminton_Bag",
        "4": "Racket_Grips"
    }

    while True:
        choice = input("Enter category number (1-4): ")
        if choice in category_map:
            category = category_map[choice]
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

    # Price validation
    while True:
        try:
            price = float(input("Enter price: RM "))
            if price <= 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid price! Must be a positive number.")

    # Stock validation
    while True:
        try:
            stock = int(input("Enter stock quantity: "))
            if stock < 0:
                raise ValueError
            break
        except ValueError:
            print("Invalid stock! Must be a non-negative integer.")

    # Check if file is empty or ends with newline
    need_newline = False
    try:
        with open("products.txt", "rb") as f:
            f.seek(-1, 2)  # Move to last byte
            last_char = f.read(1)
            if last_char != b"\n":
                need_newline = True
    except OSError:
        pass

    with open("products.txt", "a") as f:
        if need_newline:
            f.write("\n")
        f.write(f"{new_id},{name},{color},{category},{price:.2f},{stock}")
    
    print("Equipment added successfully!")
    time.sleep(2)
    
    if current_admin == "super_admin":
        superadminMenu()
    else:
        adminMenu()

def editEquipment():
    global current_admin
    print("\n=== Edit Equipment ===")
    products = []

    try:
        with open("products.txt", "r") as f:
            products = [line.strip().split(",") for line in f.readlines()]
    except FileNotFoundError:
        print("No equipment found!")
        if current_admin == "super_admin":
            superadminMenu()
        else:
            adminMenu()
        return

    # Display products
    print("\nID  Name                                Category             Price    Stock")
    print("--------------------------------------------------------------------------")
    for p in products:
        print(f"{p[0]:<3} {p[1].replace('_',' '):<35} {p[3].replace('_',' '):<20} RM{p[4]:<6} {p[5]}")

    # Select product
    while True:
        try:
            pid = input("\nEnter equipment ID to edit (0 to cancel): ")
            if pid == "0":
                if current_admin == "super_admin":
                    superadminMenu()
                else:
                    adminMenu()
                return
            product = next(p for p in products if p[0] == pid)
            break
        except StopIteration:
            print("Invalid ID! Try again.")

    # Edit fields
    print("\nSelect field to edit:")
    print("1. Name")
    print("2. Color")
    print("3. Category")
    print("4. Price")
    print("5. Stock")
    choice = input("Enter choice: ")

    index_map = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
    if choice not in map(str, index_map.keys()):
        print("Invalid choice!")
        if current_admin == "super_admin":
            superadminMenu()
        else:
            adminMenu()
        return

    index = index_map[int(choice)]
    new_value = input(f"Enter new value (current: {product[index]}): ")

    # Validate numbers
    if index == 4:
        try:
            new_value = f"{float(new_value):.2f}"
        except ValueError:
            print("Invalid price format!")
            if current_admin == "super_admin":
                superadminMenu()
            else:
                adminMenu()
            return
    elif index == 5:
        try:
            new_value = str(int(new_value))
        except ValueError:
            print("Invalid stock format!")
            if current_admin == "super_admin":
                superadminMenu()
            else:
                adminMenu()
            return

    product[index] = new_value

    # Save changes
    with open("products.txt", "w") as f:
        for p in products:
            f.write(",".join(p) + "\n")

    print("Equipment updated successfully!")
    time.sleep(2)
    if current_admin == "super_admin":
        superadminMenu()
    else:
        adminMenu()

def deleteEquipment():
    global current_admin
    print("\n=== Delete Equipment ===")
    try:
        with open("products.txt", "r") as f:
            products = [line.strip().split(",") for line in f]
    except FileNotFoundError:
        print("No equipment found!")
        if current_admin == "super_admin":
            superadminMenu()
        else:
            adminMenu()
        return

    print("\nID  Name                                Category             Price    Stock")
    print("--------------------------------------------------------------------------")
    for p in products:
        print(f"{p[0]:<4} {p[1].replace('_',' '):<35} {p[3].replace('_',' '):<20} RM{p[4]:<8} {p[5]}")

    while True:
        pid = input("\nEnter equipment ID to delete (0 to cancel): ").strip()
        if pid == "0":
            if current_admin == "super_admin":
                superadminMenu()
            else:
                adminMenu()
            return
        if any(p[0] == pid for p in products):
            break
        print("Invalid ID! Try again.")

    confirm = input("Are you sure you want to delete this equipment? (y/n): ").lower()
    if confirm != "y":
        print("Deletion cancelled.")
        time.sleep(2)
        if current_admin == "super_admin":
            superadminMenu()
        else:
            adminMenu()
        return

    with open("products.txt", "w") as f:
        for p in products:
            if p[0] != pid:
                f.write(",".join(p) + "\n")

    print("Equipment deleted successfully!")
    time.sleep(2)
    if current_admin == "super_admin":
        superadminMenu()
    else:
        adminMenu()

def viewEquipment():
    print("\n==============================================")
    print("============== ALL EQUIPMENT ================")
    print("==============================================\n")
    
    try:
        with open("products.txt", "r") as f:
            print("\nID  Name                                Category             Price    Stock")
            print("-" * 70)
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 6:
                    print(f"{parts[0]:<4}{parts[1].replace('_',' '):<35}{parts[3]:<20}RM {parts[4]:<8}{parts[5]:<10}")
    except FileNotFoundError:
        print("No equipment found in inventory!")
    
    input("\nPress Enter to return...")
    if current_admin == "super_admin":
        superadminMenu()
    else:
        adminMenu()

def viewAllRecommendations():
    print("\n===== All Product Recommendations =====\n")

    # Load user_id → username
    user_map = {}
    try:
        with open("users.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    user_map[parts[0]] = parts[1]
    except FileNotFoundError:
        print("users.txt not found!")
        return

    # Load product_id → product_name
    product_map = {}
    try:
        with open("products.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    product_map[parts[0]] = parts[1].replace("_", " ")
    except FileNotFoundError:
        print("products.txt not found!")
        return

    # Load recommendations and sort by product_id
    try:
        with open("recommendation.txt", "r") as f:
            recommendations = [line.strip().split(",", 3) for line in f]
    except FileNotFoundError:
        print("recommendation.txt not found!")
        return

    if not recommendations:
        print("No recommendations available.")
        return

    # Sort recommendations by product_id (as integer)
    recommendations.sort(key=lambda x: int(x[2]))

    # Display grouped by product_id
    current_product_id = None
    for rec_id, user_id, product_id, comment in recommendations:
        if product_id != current_product_id:
            current_product_id = product_id
            product_name = product_map.get(product_id, f"Unknown Product {product_id}")
            print(f"\n{product_id} {product_name}")

        username = user_map.get(user_id, f"User{user_id}")
        print(f"{username}: {comment}")

    print("\n=======================================")
    input("\nPress Enter to continue...")
    if current_admin == "super_admin":
        superadminMenu()
    else:
        adminMenu()
