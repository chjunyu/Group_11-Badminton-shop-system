def userMenu():
    clear_screen()
    global current_user
    print("\n===============================================")
    print("================== 📋User Menu ================")
    print("===============================================")
    print("1. Search Equipment (All)")
    print("2. Search Equipment (by category)")
    print("3. Product Recommendation") #by recomandation from Product Recommender(system) no feedback
    print("4. Puchase History")
    print("5. Provide recomandation")
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
        print(f"{'ID':<5}{'Name':<30}{'Category':<15}{'Price':<10}Stock")
        for p in products:
            print(f"{p['id']:<5}{p['name']:<30}{p['category']:<15}RM{p['price']:<8.2f}{p['quantity']}")

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
    print("\n=== Product Recommendations ===")
    
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
        with open("recommendation.txt", "r") as f:
            recommendations = []
            for line in f:
                parts = line.strip().split(",", 3)  # Split into 4 parts, ensuring the comment is handled
                if len(parts) == 4:
                    rec_id, user_id, prod_id, comment = parts
                    recommendations.append((rec_id, user_id, prod_id, comment.strip('"')))  # Remove quotes around comments
    except FileNotFoundError:
        print("recommendation.txt not found.")
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
    print("\n=== Provide Product Recommendation ===")
    
    # Show purchase history
    print("\nYour Purchase History:")
    print("{:<5} {:<27} {:<12} {}".format("ID", "Product Name", "Purchase Date", "Quantity"))
    print("-" * 55)
    
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
            print("{:<5} {:<27} {:<12} {}".format(
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
        product_id = input("\nEnter product ID to recommend (0 to cancel): ").strip()
        if product_id == "0":
            userMenu()
            return
            
        # Verify purchase
        valid_ids = [p["product_id"] for p in purchases]
        if product_id in valid_ids:
            break
        print("Invalid ID! You can only recommend products you've purchased")

    # Get recommendation comment
    comment = input("Enter your recommendation (max 100 characters): ").strip()[:100]
    
    # Generate recommendation ID
    try:
        with open("recommendation.txt", "r") as f:
            recommendations = f.readlines()
            last_id = int(recommendations[-1].split(",")[0]) if recommendations else 0
    except FileNotFoundError:
        last_id = 0
        
    new_id = last_id + 1

    # Save recommendation
    with open("recommendation.txt", "a") as f:
        f.write(f"{new_id},{current_user_id},{product_id},\"{comment}\"\n")
    
    print("\nRecommendation submitted successfully!")
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
    print("1. Puchase Racket")
    print("2. Purchase Shuttlecocks")
    print("3. Purchase Badminton Bag")
    print("4. Purchase Racket Grips")
    print("5. Search Equipment by Racket Recommendation") #include see all racket Recommendation press 1 as want purchase press 0 back
    print("6. Search Equipment by Shuttlecocks Recommendation")
    print("7. Search Equipment by Badminton Bag Recommendation")
    print("8. Search Equipment by Racket GripsRecommendation")
    
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
        userMenu()

#sort category product by recommendation
def searchbyRacketRecommendation():
    searchByCategoryRecommendation("Racket")

def searchbyShuttlecocksRecommendation():
    searchByCategoryRecommendation("Shuttlecocks")

def searchbyBadmintonBagRecommendation():
    searchByCategoryRecommendation("BadmintonBag")

def searchbyRacketGripsRecommendation():
    searchByCategoryRecommendation("RacketGrips")

def searchByCategoryRecommendation(category):
    clear_screen()
    print(f"\n=== Recommendations for Category: {category.replace('_', ' ')} ===")

    try:
        # Load products
        with open("products.txt", "r") as f:
            products = [line.strip().split(",") for line in f]

        # Load recommendations
        with open("recommendation.txt", "r") as f:
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
    searchByCategoryEquipment("Shuttlecocks")

def searchbyBadmintonBag():
    searchByCategoryEquipment("BadmintonBag")

def searchbyRacketGrips():
    searchByCategoryEquipment("RacketGrips")

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
        print(f"{'ID':<5}{'Name':<30}{'Price':<10}Stock")
        for p in products:
            print(f"{p['id']:<5}{p['name']:<30}RM{p['price']:<8.2f}{p['quantity']}")

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