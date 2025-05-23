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
    print("| 5. Product Comment                 |")
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
    print("| 5. Product Comment                 |")
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
    print("2. Shuttlecock")
    print("3. Badminton_Bag")
    print("4. Racket_Grip")

    category_map = {
        "1": "Racket",
        "2": "Shuttlecock",
        "3": "Badminton_Bag",
        "4": "Racket_Grip"
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
    print("\n===== All Product Comments =====\n")

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
        with open("comment.txt", "r") as f:
            recommendations = [line.strip().split(",", 3) for line in f]
    except FileNotFoundError:
        print("comment.txt not found!")
        return

    if not recommendations:
        print("No comment available.")
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

def viewCustomer():
    print("\n=== View Customers ===")
    try:
        with open("users.txt", "r") as f:
            users = [line.strip().split(",") for line in f]
    except FileNotFoundError:
        print("No customers found!")
        time.sleep(2)
        superadminMenu()
        return

    print(f"\nTotal users: {len(users)}\n")
    print("ID  Username")
    print("------------")
    for u in users:
        print(f"{u[0]:<3} {u[1]}")

    input("\nPress Enter to continue...")
    time.sleep(2)
    superadminMenu()

def adminadduser():
    # Username validation (3 attempts)
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
        superadminMenu()
        return

    # Password validation (3 attempts)
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
            admin_register(username, password)
            return
        else:
            print("Passwords do not match.")
            remaining = 2 - attempt
            if remaining > 0:
                print(f"{remaining} attempt(s) left.")

    print("Too many failed attempts. Registration aborted.")
    time.sleep(2)
    superadminMenu()

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

def admin_register(username, password):
    user_id = getNextUserId()
    with open("users.txt", "a", newline="\n") as file:
        file.write(f"{user_id},{username},{password}\n")
    print("\nAccount created successfully")
    time.sleep(2)
    superadminMenu()


def addStaff():
    print("\n=== Add New Staff ===")

    # Generate new staff ID
    new_id = get_next_id("admins.txt")

    # Get existing usernames to avoid duplicates
    existing = []
    try:
        with open("admins.txt", "r") as f:
            existing = [line.strip().split(",")[1] for line in f]
    except FileNotFoundError:
        pass  # It's okay if the file doesn't exist yet

    while True:
        username = input("Enter staff username: ").strip()
        if username in existing:
            print("Username already exists!")
        else:
            break

    # Password entry with validation and retry logic
    for attempt in range(3):
        password = input("Enter password (min 8 characters): ").strip()
        if len(password) < 8:
            print("Password must be at least 8 characters.")
            remaining = 2 - attempt
            if remaining > 0:
                print(f"{remaining} attempt(s) left.")
            time.sleep(1)
            continue

        confirm = input("Confirm password: ").strip()
        if password == confirm:
            # Save to file if password is valid and confirmed
            with open("admins.txt", "a") as f:
                f.write(f"{new_id},{username},{password}\n")
            print("Staff added successfully!")
            time.sleep(2)
            superadminMenu()
            return
        else:
            print("Passwords do not match.")
            remaining = 2 - attempt
            if remaining > 0:
                print(f"{remaining} attempt(s) left.")
            time.sleep(1)

    print("Too many failed attempts. Registration aborted.")
    time.sleep(2)
    superadminMenu()

def deleteStaff():
    print("\n=== Delete Staff ===")
    try:
        with open("admins.txt", "r") as f:
            staffs = [line.strip().split(",") for line in f]
    except FileNotFoundError:
        print("No staff found!")
        time.sleep(2)
        superadminMenu()
        return

    print("\nID  Username")
    print("------------")
    for s in staffs:
        print(f"{s[0]:<3} {s[1]}")

    while True:
        sid = input("\nEnter staff ID to delete (0 to cancel): ").strip()
        if sid == "0":
            superadminMenu()
            return
        if any(s[0] == sid for s in staffs):
            break
        print("Invalid ID! Try again.")

    confirm = input("Are you sure you want to delete this staff? (y/n): ").lower()
    if confirm != "y":
        print("Deletion cancelled.")
        time.sleep(2)
        superadminMenu()
        return

    with open("admins.txt", "w") as f:
        for s in staffs:
            if s[0] != sid:
                f.write(",".join(s) + "\n")

    print("Staff deleted successfully!")
    time.sleep(2)
    superadminMenu()

def viewStaff():
    print("\n=== View Staff ===")
    try:
        with open("admins.txt", "r") as f:
            staffs = [line.strip().split(",") for line in f]
    except FileNotFoundError:
        print("No staff found!")
        time.sleep(2)
        superadminMenu()
        return

    print("\nID  Username")
    print("------------")
    for s in staffs:
        print(f"{s[0]:<3} {s[1]}")
    
    input("\nPress Enter to continue...")
    superadminMenu()


def salesReport():
    print("\n=== Sales Report ===")
    today_str = datetime.now().strftime("%d/%m/%Y")

    try:
        with open("purchases.txt", "r") as f:
            lines = f.readlines()
            if len(lines) <= 1:
                print("No sales records found!")
                time.sleep(2)
                return superadminMenu() if current_admin == "super_admin" else adminMenu()
            purchases = [line.strip().split(",") for line in lines[1:] if line.strip()]
    except FileNotFoundError:
        print("No sales records found!")
        time.sleep(2)
        return superadminMenu() if current_admin == "super_admin" else adminMenu()

    # Load user ID to name mapping
    user_map = {}
    try:
        with open("user.txt", "r") as f:
            user_lines = f.readlines()[1:]  # Skip header
            for line in user_lines:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    user_map[parts[0]] = parts[1]
    except FileNotFoundError:
        pass

    # Load product ID to name mapping
    product_map = {}
    try:
        with open("products.txt", "r") as f:
            product_lines = f.readlines()[1:]  # Skip header
            for line in product_lines:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    product_map[parts[0]] = parts[1].replace("_", " ")
    except FileNotFoundError:
        pass

    # Initialize totals
    total_revenue = 0
    today_sales_volume = 0
    today_sales_quantity = 0
    today_products = {}
    all_products = {}

    recent_transactions = purchases[-10:]

    # Process purchases
    for p in purchases:
        try:
            purchase_id = p[0]
            user_id = p[1]
            product_id = p[2]
            quantity = int(p[3])
            total_price = float(p[4])
            method = p[5]
            date = p[6]
        except (IndexError, ValueError):
            continue

        total_revenue += total_price

        # For today's sales
        if date == today_str:
            today_sales_volume += total_price
            today_sales_quantity += quantity
            if product_id in today_products:
                today_products[product_id]["qty"] += quantity
                today_products[product_id]["total"] += total_price
            else:
                today_products[product_id] = {
                    "name": product_map.get(product_id, "Unknown"),
                    "qty": quantity,
                    "total": total_price
                }

        # All-time product stats
        if product_id in all_products:
            all_products[product_id]["qty"] += quantity
            all_products[product_id]["total"] += total_price
        else:
            all_products[product_id] = {
                "name": product_map.get(product_id, "Unknown"),
                "qty": quantity,
                "total": total_price
            }

    # Show today's sales
    print(f"\nToday's Sales Quantity: {today_sales_quantity}")
    print(f"Today's Sales Volume:   RM{today_sales_volume:.2f}")

    if today_products:
        print("\nProducts Sold Today:")
        print("ID  Name                                Qty  Total")
        print("-----------------------------------------------------")
        for pid in sorted(today_products.keys()):
            info = today_products[pid]
            print(f"{pid:<4}{info['name']:<35}{info['qty']:<5}RM{info['total']:.2f}")
    else:
        print("\nNo products were sold today.")

    # Show total revenue and product sales
    print(f"\nTotal Revenue: RM{total_revenue:.2f}")
    print("\nAll-Time Product Sales:")
    print("ID  Name                                Qty  Total")
    print("-----------------------------------------------------")
    for pid in sorted(all_products.keys()):
        info = all_products[pid]
        print(f"{pid:<4}{info['name']:<35}{info['qty']:<5}RM{info['total']:.2f}")

    input("\nPress Enter to return...")
    return superadminMenu() if current_admin == "super_admin" else adminMenu()


#-----------------------------------------------------------------------------------
#About Us
def aboutUs():
    clear_screen()
    print("\n===============================================")
    print("===== Badminton Sport Equipment System =======")
    print("==============================================")
    print("================== About Us ==================")
    print("==============================================")
    print("Group 11 Badminton Sport Equipment System")
    print("1. Chan Jun Yu    (1221208634)")
    print("2. Hwang Yong Jin (1221207893)")
    print("3. Soh Yong Seng  (1221207836)")
    print("4. Tan Chun Hoong (1221207498)")
    input("\nPress Enter to continue...")
    main()

#about us finish
#-----------------------------------------------------------------------------------

def userMenu():
    clear_screen()
    global current_user
    print("\n===============================================")
    print("================== 📋User Menu ================")
    print("===============================================")
    print("1. Search Equipment (All)")
    print("2. Search Equipment (by category)")
    print("3. View Product Comment") #by recomandation from Product Recommender(system) no feedback
    print("4. Puchase History")
    print("5. Give Feeback to Equipment")
    print("6. Edit Profile")
    print("7. Delete Account")
    print("8. Logout")
    print(f"Welcome {current_user} to our Badminton Sport Equipment System!")
    choice = input("\nEnter your choice : ")
    if choice == "1":
        searchAllEquipment()
    elif choice == "2":
        searchbyCategoryMenu()
    elif choice == "3":
        productRecommendation()
    elif choice == "4":
        purchaseHistory()
    elif choice == "5":
        provideRecommendation()
    elif choice == "6":
        editProfile()
    elif choice == "7":
        deleteAccount()
    elif choice == "8":
        current_user = None
        print("\nLogging out...")
        time.sleep(1)
        main()
    else:
        print("Invalid choice")
        time.sleep(2)
        userMenu()

#1
def searchAllEquipment():
    clear_screen()
    print("\n==============================================")
    print("========== Search Equipment (All) ===========")
    print("==============================================")
    print("1. Search Equipment (All)")
    print("0. Back")
    choice = input("Enter your choice : ")
    if choice == "1":
        searchAllEquipmentMenu()
    elif choice == "0":
        userMenu()
    else:
        print("Invalid choice. Try again.")
        time.sleep(1)
        searchAllEquipment()

def searchAllEquipmentMenu():
    clear_screen()
    products = []
    cart = []
    total_price = 0.0

    try:
        with open("products.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 6:
                    products.append({
                        "id": parts[0],
                        "name": parts[1].replace('_', ' '),
                        "color": parts[2],
                        "category": parts[3],
                        "price": float(parts[4]),
                        "quantity": int(parts[5])
                    })

        if not products:
            print("\nNo products available.")
            if current_user_id is None:  # Use global variable
                userMenu()
            else:
                userMenu()
            return

        print("\nAll Available Products:")
        print(f"{'ID':<5}{'Name':<35}{'Category':<15}{'Price':<10}Stock")
        for p in products:
            print(f"{p['id']:<5}{p['name']:<35}{p['category']:<15}RM{p['price']:<8.2f}{p['quantity']}")

        # Restrict guest from purchasing
        if current_user_id is None:  # Use global variable
            print("\nNote: Guests cannot purchase items. Please log in to buy equipment.")
            input("Press Enter to return to Guest Menu...")
            userMenu()
            return

        # Purchase flow for logged-in users
        while True:
            pid = input("\nEnter product ID to purchase (0 to cancel): ").strip()
            if pid == "0":
                break

            product = next((p for p in products if p['id'] == pid), None)
            if not product:
                print("Invalid product ID!")
                continue

            try:
                qty = int(input(f"How many '{product['name']}'? (Stock: {product['quantity']}) : "))
                if qty <= 0:
                    print("Quantity must be positive!")
                    continue
                if qty > product['quantity']:
                    print("Insufficient stock!")
                    continue

                cart.append({"product": product, "qty": qty})
                total_price += product['price'] * qty
                print(f"Added {qty} x {product['name']} to cart. Subtotal: RM{total_price:.2f}")

                cont = input("Do you want to keep buying (y/n)? ").strip().lower()
                if cont != 'y':
                    break

            except ValueError:
                print("Invalid quantity!")

        if not cart:
            print("No items selected. Returning to menu.")
            time.sleep(2)
            userMenu()
            return

        print(f"\nTotal: RM{total_price:.2f}")
        confirm = input("Confirm purchase (y/n)? ").strip().lower()
        if confirm != 'y':
            print("Purchase cancelled.")
            time.sleep(2)
            userMenu()
            return

        # Payment method
        print("\nPayment Method")
        print("1. Credit")
        print("2. Debit")
        purchase_by = input("Enter payment method (1/2): ").strip()
        if purchase_by == "1":
            purchase_by = "Credit"
        elif purchase_by == "2":
            purchase_by = "Debit"
        else:
            print("Invalid payment method. Purchase cancelled.")
            time.sleep(2)
            userMenu()
            return

        # Update stock
        with open("products.txt", "r") as file:
            all_products = []
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 6:
                    all_products.append({
                        "id": parts[0],
                        "name": parts[1].replace('_', ' '),
                        "color": parts[2],
                        "category": parts[3],
                        "price": float(parts[4]),
                        "quantity": int(parts[5])
                    })

        for item in cart:
            for prod in all_products:
                if prod["id"] == item["product"]["id"]:
                    prod["quantity"] -= item["qty"]

        with open("products.txt", "w") as f:
            for p in all_products:
                f.write(f"{p['id']},{p['name'].replace(' ', '_')},{p['color']},{p['category']},{p['price']:.2f},{p['quantity']}\n")

        # Generate purchase ID
        try:
            with open("purchases.txt", "r") as f:
                lines = f.readlines()
                last_id = max(int(line.strip().split(",")[0]) for line in lines if line.strip())
        except (FileNotFoundError, ValueError):
            last_id = 0

        new_purchase_id = last_id + 1
        today = datetime.today().strftime('%d/%m/%Y')

        # Save purchases
        with open("purchases.txt", "a") as f:
            for item in cart:
                f.write(f"{new_purchase_id},{current_user_id},{item['product']['id']},{item['qty']},{item['product']['price'] * item['qty']:.2f},{purchase_by},{today}\n")

        print("\nPurchase successful!")
        userReceipt(new_purchase_id, purchase_by, total_price, cart)

    except FileNotFoundError:
        print("Product database not found!")
        time.sleep(2)
        if current_user_id is None:
            print("\nSorry cannot Returning to Guest Menu...")
            time.sleep(2)
            userMenu()
        else:
            userMenu()

def productRecommendation():
    clear_screen()
    print("\n=== Product Comments ===")
    
    # Load product data
    try:
        with open("products.txt", "r") as f:
            products = [line.strip().split(",") for line in f]
    except FileNotFoundError:
        print("products.txt not found.")
        input("\nPress Enter to return...")
        userMenu()
        return

    # Load recommendation data
    try:
        with open("comment.txt", "r") as f:
            recommendations = []
            for line in f:
                parts = line.strip().split(",", 3)  # Split into 4 parts, ensuring the comment is handled
                if len(parts) == 4:
                    rec_id, user_id, prod_id, comment = parts
                    recommendations.append((rec_id, user_id, prod_id, comment.strip('"')))  # Remove quotes around comments
    except FileNotFoundError:
        print("comment.txt not found.")
        input("\nPress Enter to return...")
        userMenu()
        return

    # Load user data
    try:
        with open("users.txt", "r") as f:
            users = {u[0]: u[1] for u in (line.strip().split(",") for line in f)}
    except FileNotFoundError:
        print("users.txt not found.")
        input("\nPress Enter to return...")
        userMenu()
        return

    # Organize comments by product_id
    rec_dict = {}
    for rec in recommendations:
        rec_id, user_id, prod_id, comment = rec
        if prod_id not in rec_dict:
            rec_dict[prod_id] = []
        username = users.get(user_id, "Unknown")
        rec_dict[prod_id].append(f"{username}: {comment}")

    # Display all recommendations sorted by product_id
    for product in sorted(products, key=lambda x: int(x[0])):
        prod_id, name = product[0], product[1].replace("_", " ")
        if prod_id in rec_dict:
            print(f"\n{prod_id} {name}")
            for comment in rec_dict[prod_id]:
                print(comment)

    # Ask user what to do next
    while True:
        choice = input("\nDo you want to purchase? (1 = Yes, 0 = Back): ").strip()
        if choice == "1":
            searchAllEquipmentMenu()
            return
        elif choice == "0":
            userMenu()
            return
        else:
            print("Invalid input. Please enter 1 or 0.")

def purchaseHistory(): 
    clear_screen()
    print("\n--- Purchase History ---")

    # Load product names
    product_names = {}
    try:
        with open("products.txt", "r") as prod_file:
            for line in prod_file:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    product_names[parts[0]] = parts[1].replace('_', ' ')
    except FileNotFoundError:
        print("products.txt not found.")
        time.sleep(2)
        return

    # Load and filter purchases
    purchases = []
    try:
        with open("purchases.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 7 and parts[1] == current_user_id:
                    purchases.append({
                        "purchase_id": parts[0],
                        "product_id": parts[2],
                        "quantity": int(parts[3]),
                        "price": float(parts[4]),
                        "method": parts[5],
                        "date": parts[6]
                    })
    except FileNotFoundError:
        print("purchases.txt not found.")
        time.sleep(2)
        return

    if not purchases:
        print("No purchases found.")
        time.sleep(2)
        userMenu()
        return

    # Sort by date
    purchases.sort(key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"))

    # Display purchases
    print(f"{'Date':<12}{'Product Name':<35}{'Qty':<5}{'Total(RM)':<12}{'Method':<10}")
    print("-" * 75)
    for p in purchases:
        product_name = product_names.get(p["product_id"], "Unknown Product")
        total = p["price"]  # Directly use stored total price
        print(f"{p['date']:<12}{product_name:<35}{p['quantity']:<5}{total:<12.2f}{p['method'].title():<10}")

    input("\nPress Enter to return to the menu...")  # Pause screen
    userMenu()

def provideRecommendation():
    clear_screen()
    print("\n=== Product Comment ===")
    
    # Show purchase history
    print("\nYour Purchase History:")
    print("{:<5} {:<35} {:<15} {}".format("ID", "Product Name", "Purchase Date", "Quantity"))
    print("-" * 65)
    
    purchases = []
    try:
        # Get product names
        products = {}
        with open("products.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 6:
                    products[parts[0]] = parts[1].replace("_", " ")

        # Get purchase history for current user
        with open("purchases.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 7 and parts[1] == current_user_id:
                    product_id = parts[2]
                    purchases.append({
                        "product_id": product_id,
                        "name": products.get(product_id, "Unknown Product"),
                        "date": parts[6],
                        "quantity": parts[3]
                    })

        if not purchases:
            print("No purchase history found!")
            time.sleep(2)
            userMenu()
            return

        # Display purchases
        for idx, purchase in enumerate(purchases, 1):
            print("{:<5} {:<35} {:<15} {}".format(
                purchase["product_id"],
                purchase["name"],
                purchase["date"],
                purchase["quantity"]
            ))

    except FileNotFoundError:
        print("Purchase records not found!")
        time.sleep(2)
        userMenu()
        return

    # Get product ID input
    while True:
        product_id = input("\nEnter product ID to comment (0 to cancel): ").strip()
        if product_id == "0":
            userMenu()
            return
            
        # Verify purchase
        valid_ids = [p["product_id"] for p in purchases]
        if product_id in valid_ids:
            break
        print("Invalid ID! You can only comment products you've purchased")

    # Get recommendation comment
    comment = input("Enter your comment (max 100 characters): ").strip()[:100]
    
    # Generate recommendation ID
    try:
        with open("comment.txt", "r") as f:
            recommendations = f.readlines()
            last_id = int(recommendations[-1].split(",")[0]) if recommendations else 0
    except FileNotFoundError:
        last_id = 0
        
    new_id = last_id + 1

    # Save recommendation
    with open("comment.txt", "a") as f:
        f.write(f"{new_id},{current_user_id},{product_id},\"{comment}\"\n")
    
    print("\nComment successfully!")
    time.sleep(2)
    userMenu()

def editProfile():
    clear_screen()
    global current_user, current_user_id

    print("\n--- Edit Profile ---")
    try:
        with open("users.txt", "r") as f:
            users = f.readlines()

        found = False
        updated_users = []

        for line in users:
            parts = line.strip().split(",")
            if len(parts) >= 3 and parts[0] == current_user_id:
                current_username = parts[1]
                current_password = parts[2]
                found = True

                # Ask for current password verification
                attempts = 3
                while attempts > 0:
                    entered_password = input("Enter your current password to continue: ").strip()
                    if entered_password == current_password:
                        break
                    else:
                        attempts -= 1
                        print(f"Incorrect password! {attempts} attempt(s) remaining.")

                if attempts == 0:
                    print("Too many failed attempts. Returning to menu.")
                    time.sleep(2)
                    userMenu()
                    return

                # Get new name with validation
                while True:
                    new_name = input(f"Enter new name [{current_username}] (leave blank to keep current): ").strip()
                    if new_name == "":
                        new_name = current_username
                        break
                    elif new_name != current_username and checkRepeatingName(new_name):
                        print("Try another name.")
                    else:
                        break

                # Get new password with validation
                while True:
                    new_password = input("Enter new password (leave blank to keep current): ").strip()
                    if new_password == "":
                        new_password = current_password  # Keep current password
                        break
                    elif len(new_password) < 8:
                        print("Password must be at least 8 characters long.")
                    else:
                        break

                # Update info
                parts[1] = new_name
                parts[2] = new_password

                current_user = new_name  # Update global username
                updated_line = ",".join(parts)
                updated_users.append(updated_line)
            else:
                updated_users.append(line.strip())

        if not found:
            print("User not found!")
            time.sleep(2)
            userMenu()
            return

        with open("users.txt", "w") as f:
            f.write("\n".join(updated_users) + "\n")  # Add newline at the end

        print("\nProfile updated successfully!")

    except FileNotFoundError:
        print("User database not found!")

    time.sleep(2)
    userMenu()

def deleteAccount():
    clear_screen()
    global current_user, current_user_id

    print("\n--- Delete Account ---")
    try:
        with open("users.txt", "r") as f:
            users = f.readlines()

        password_match = False
        updated_users = []

        for line in users:
            parts = line.strip().split(",")
            if len(parts) >= 3 and parts[0] == current_user_id:
                stored_password = parts[2]

                # Ask for password up to 3 times
                attempts = 3
                while attempts > 0:
                    password = input("Enter your password to confirm: ").strip()
                    if password == stored_password:
                        password_match = True
                        break
                    else:
                        attempts -= 1
                        print(f"Incorrect password! {attempts} attempt(s) remaining.")

                if not password_match:
                    updated_users.append(line.strip())  # Keep user since deletion failed
                continue  # Skip this line if password matched (deleting user)

            updated_users.append(line.strip())

        if not password_match:
            print("Failed to authenticate. Account not deleted.")
            time.sleep(2)
            userMenu()
            return

        # Write remaining users back to file
        with open("users.txt", "w") as f:
            f.write("\n".join(updated_users) + "\n")

        print("\nAccount deleted successfully!")

        # Clear session
        current_user = None
        current_user_id = None

        time.sleep(2)
        main()

    except FileNotFoundError:
        print("User database not found!")
        time.sleep(2)
        userMenu()

def searchbyCategoryMenu():
    clear_screen()
    print("\n=====================================================")
    print("========== Search Equipment (by category) ===========")
    print("=====================================================")
    print("1. Search by Racket")
    print("2. Search by Shuttlecocks")
    print("3. Search by Badminton Bag")
    print("4. Search by Racket Grips")
    print("5. Search Comment by Racket") #include see all racket Recommendation press 1 as want purchase press 0 back
    print("6. Search Comment by Shuttlecocks")
    print("7. Search Comment by Badminton Bag")
    print("8. Search Comment by Racket Grips")
    
    print("0. Back")
    choice = input("\nEnter your choice : ")
    if choice == "1":
        searchbyRacket()
    elif choice == "2":
        searchbyShuttlecocks()
    elif choice == "3":
        searchbyBadmintonBag()
    elif choice == "4":
        searchbyRacketGrips()
    elif choice == "5":
        searchbyRacketRecommendation()
    elif choice == "6":
        searchbyShuttlecocksRecommendation()
    elif choice == "7":
        searchbyBadmintonBagRecommendation()
    elif choice == "8":
        searchbyRacketGripsRecommendation()
    else:
        print("Invalid choice!")
        time.sleep(2)
        userMenu()

#sort category product by recommendation
def searchbyRacketRecommendation():
    searchByCategoryRecommendation("Racket")

def searchbyShuttlecocksRecommendation():
    searchByCategoryRecommendation("Shuttlecock")

def searchbyBadmintonBagRecommendation():
    searchByCategoryRecommendation("BadmintonBag")

def searchbyRacketGripsRecommendation():
    searchByCategoryRecommendation("RacketGrip")

def searchByCategoryRecommendation(category):
    clear_screen()
    print(f"\n=== Comment for Category: {category.replace('_', ' ')} ===")

    try:
        # Load products
        with open("products.txt", "r") as f:
            products = [line.strip().split(",") for line in f]

        # Load recommendations
        with open("comment.txt", "r") as f:
            recommendations = [line.strip().split(",") for line in f]

        # Load user data
        with open("users.txt", "r") as f:
            users = {u[0]: u[1] for u in (line.strip().split(",") for line in f)}

    except FileNotFoundError as e:
        print(f"Missing file: {e.filename}")
        input("\nPress Enter to return...")
        userMenu()
        return

    # Filter products by category
    filtered_products = [p for p in products if p[3] == category]

    # Organize recommendations by product_id
    rec_dict = {}
    for rec in recommendations:
        if len(rec) != 4:
            continue  # Skip malformed lines
        _, user_id, prod_id, comment = rec
        username = users.get(user_id, "Unknown")
        rec_dict.setdefault(prod_id, []).append(f"{username}: {comment}")

    # Display recommendations only for filtered products
    for p in filtered_products:
        prod_id, name = p[0], p[1].replace("_", " ")
        if prod_id in rec_dict:
            print(f"\n{prod_id} {name}")
            for comment in rec_dict[prod_id]:
                print(f"- {comment}")

    # Option to purchase
    while True:
        choice = input("\nDo you want to purchase? (1 = Yes, 0 = Back): ").strip()
        if choice == "1":
            searchByCategoryEquipment(category)
            return
        elif choice == "0":
            searchbyCategoryMenu()
            return
        else:
            print("Invalid input. Please enter 1 or 0.")

#sort by cateogry product
def searchbyRacket():
    searchByCategoryEquipment("Racket")

def searchbyShuttlecocks():
    searchByCategoryEquipment("Shuttlecock")

def searchbyBadmintonBag():
    searchByCategoryEquipment("BadmintonBag")

def searchbyRacketGrips():
    searchByCategoryEquipment("RacketGrip")

from datetime import datetime

def searchByCategoryEquipment(category_filter):
    clear_screen()
    global current_user_id  # Ensure current_user_id is accessible
    products = []
    cart = []
    total_price = 0.0

    try:
        with open("products.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 6:
                    product = {
                        "id": parts[0],
                        "name": parts[1].replace('_', ' '),
                        "color": parts[2],
                        "category": parts[3],
                        "price": float(parts[4]),
                        "quantity": int(parts[5])
                    }
                    if product["category"].lower() == category_filter.lower():
                        products.append(product)

        if not products:
            print(f"\nNo products found under category '{category_filter}'.")
            userMenu()
            return

        # ✅ Show products to everyone (including guests)
        print(f"\nAvailable {category_filter}s:")
        print(f"{'ID':<5}{'Name':<35}{'Price':<10}Stock")
        for p in products:
            print(f"{p['id']:<5}{p['name']:<35}RM{p['price']:<8.2f}{p['quantity']}")

        # ✅ Then block purchase only if guest
        if current_user_id is None:
            print("\nNote: Guests cannot purchase items. Please log in to buy equipment.")
            input("Press Enter to return to Guest Menu...")
            userMenu()
            return
        
        while True:
            pid = input("\nEnter product ID to purchase (0 to cancel): ").strip()
            if pid == "0":
                break

            product = next((p for p in products if p['id'] == pid), None)
            if not product:
                print("Invalid product ID!")
                continue

            try:
                qty = int(input(f"How many '{product['name']}'? (Stock: {product['quantity']}) : "))
                if qty <= 0:
                    print("Quantity must be positive!")
                    continue
                if qty > product['quantity']:
                    print("Insufficient stock!")
                    continue

                cart.append({"product": product, "qty": qty})
                total_price += product['price'] * qty
                print(f"Added {qty} x {product['name']} to cart. Subtotal: RM{total_price:.2f}")

                cont = input("Do you want to keep buying (y/n)? ").strip().lower()
                if cont != 'y':
                    break

            except ValueError:
                print("Invalid quantity!")

        if not cart:
            print("No items selected. Returning to menu.")
            userMenu()
            return

        print(f"\nTotal: RM{total_price:.2f}")
        confirm = input("Confirm purchase (y/n)? ").strip().lower()
        if confirm != 'y':
            print("Purchase cancelled.")
            userMenu()
            return

        # Payment method
        print("\nPayment Method")
        print("1. Credit")
        print("2. Debit")
        purchase_by = input("Enter payment method (1/2): ").strip()
        if purchase_by == "1":
            purchase_by = "Credit"
        elif purchase_by == "2":
            purchase_by = "Debit"
        else:
            print("Invalid payment method. Purchase cancelled.")
            userMenu()
            return

        # Update stock
        with open("products.txt", "r") as file:
            all_products = []
            for line in file:
                parts = line.strip().split(",")
                if len(parts) >= 6:
                    all_products.append({
                        "id": parts[0],
                        "name": parts[1].replace('_', ' '),
                        "color": parts[2],
                        "category": parts[3],
                        "price": float(parts[4]),
                        "quantity": int(parts[5])
                    })

        for item in cart:
            for prod in all_products:
                if prod["id"] == item["product"]["id"]:
                    prod["quantity"] -= item["qty"]

        with open("products.txt", "w") as f:
            for p in all_products:
                f.write(f"{p['id']},{p['name'].replace(' ', '_')},{p['color']},{p['category']},{p['price']:.2f},{p['quantity']}\n")

        # Generate purchase ID
        try:
            with open("purchases.txt", "r") as f:
                lines = f.readlines()
                last_id = max(int(line.strip().split(",")[0]) for line in lines if line.strip())
        except (FileNotFoundError, ValueError):
            last_id = 0

        new_purchase_id = last_id + 1
        today = datetime.today().strftime('%d/%m/%Y')

        # Save to purchases.txt
        with open("purchases.txt", "a") as f:
            for item in cart:
                f.write(f"{new_purchase_id},{current_user_id},{item['product']['id']},{item['qty']},{item['product']['price'] * item['qty']:.2f},{purchase_by},{today}\n")

        print("\nPurchase successful!")
        userReceipt(new_purchase_id, purchase_by, total_price, cart)

    except FileNotFoundError:
        print("Product database not found!")
        time.sleep(2)
        if current_user_id is None:
            print("\nSorry cannot Returning to Guest Menu...")
            time.sleep(2)
            userMenu()
        else:
            userMenu()


def userReceipt(purchase_id, purchase_by, total_price, cart):
    print("\n" + "=" * 40)
    print("\t\tRECEIPT")
    print("=" * 40)
    print(f"Username     : {current_user}")
    print(f"Pay by       : {purchase_by}")
    print(f"{'Product':<30}{'Qty':<5}")
    for item in cart:
        print(f"{item['product']['name']:<30}{item['qty']:<5}")
    print("-" * 40)
    print(f"Total        : RM{total_price:.2f}")
    print("=" * 40)
    input("\nPress Enter to return...")
    userMenu()

#--------------------------------------------------------------
#main menu first page
def main():
    while True:    
        clear_screen()
        print("\n")
        print("\n================================================")
        print("======= Badminton Sport Equipment System =======")
        print("================================================")
        
        print("Menu")
        
        print("< 1 > User Register")
        print("< 2 > User Login")
        print("< 3 > Guest Mode")
        print("< 4 > Admin Login")
        print("< 5 > About Us")
        print("< 0 > Exit")
        choice = input("Enter your choice : ")

        if choice == "1":
            userRegister()
        elif choice == "2":
            userLogin()
        elif choice == "3":
            guestMode()
        elif choice == "4":
            adminLogin()
        elif choice == "5":
            aboutUs()
        elif choice == "0":
            print("Thank you for using our system")
            break
        else:
            print("Invalid choice")
main()