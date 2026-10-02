from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from datetime import datetime

client = MongoClient("mongodb+srv://sabari:seetharamanpoongodi@cluster0.4higtot.mongodb.net/?appName=Cluster0")

db = client["ocean_project"]
users = db["users"]
products = db["products"]
orders = db["orders"]


# Unique email
users.create_index("email", unique=True)


# 1. Add User

def add_user():
    print("add user")
    name = input("Enter name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    mobile = input("Enter mobile: ")
    address = input("Enter address: ")

    user_data = {
        "name": name,
        "email": email,
        "password": password,
        "createdAt": datetime.now(),
        "mobile": mobile,
        "address": address
        }

    try:
        result = users.insert_one(user_data)
        print("✅User added successfully.")
        print("User ID:", result.inserted_id)

    except DuplicateKeyError:
        print("🙁 Error: Email already exists.")


# 2. Check Email and Password

def check_login():
    email = input("🆔 Enter email: ")
    password = input("🔑 Enter password: ")
    user = users.find_one({
        "email": email,
        "password": password
    })
    if user:
        print("🎉 Login successful.")
        print("Welcome", user["name"])
    else:
        print("❌ Invalid email or password.")


# 3. Get All Users

def get_all_users():
    data = users.find()
    for user in data:
        print("-------------------------")
        print("ID:", user["_id"])
        print("Name:", user["name"])
        print("Email:", user["email"])
        print("Password:", user["password"])
        print("Mobile:", user["mobile"])
        print("Address:", user["address"])
        print("Created At:", user["createdAt"])


# 4. Get Specific User

def get_specific_user():
    email = input("Enter email: ")
    user = users.find_one({"email": email})

    if user:
        print("-------------------------")
        print("ID:", user["_id"])
        print("Name:", user["name"])
        print("Email:", user["email"])
        print("Mobile:", user["mobile"])
        print("Address:", user["address"])
    else:
        print("🙁 User not found.")

# 5. Update User

def update_user():
    email = input("Enter email: ")
    user = users.find_one({"email": email})

    if user:
        name = input("Enter new name: ")
        mobile = input("Enter new mobile: ")
        address = input("Enter new address: ")
        update_data = {}
        if name.strip():
            update_data["name"] = name
        if mobile.strip():
            update_data["mobile"] = mobile
        if address.strip():
            update_data["address"] = address
        if update_data:
            users.update_one(
                {"email": email},
                {"$set": update_data}
            )
            print("✅ User updated successfully.")
        else:
            print("⚠️ No changes made.")
    else:
        print("❌ User not found.")

# 6. Delete User

def delete_user():
    email = input("Enter email: ")
    result = users.delete_one({"email": email})
    if result.deleted_count > 0:
        print("✅ User deleted successfully.")
    else:
        print("🙁 User not found.")


# 7. Add Product

def add_product():
    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    model = input("Enter model: ")
    color = input("Enter color: ")
    stock = int(input("Enter stock: "))
    discount = float(input("Enter discount (%): "))
    product_data = {
        "name": name,
        "price": price,
        "model": model,
        "color": color,
        "stock": stock,
        "discount": discount
    }
    result = products.insert_one(product_data)
    print("📦 Product added successfully.")
    print("Product ID:", result.inserted_id)


# 8. Get All Products

def get_all_products():
    data = products.find()
    for product in data:
        print("-------------------------")
        print("ID:", product["_id"])
        print("Name:", product["name"])
        print("Price:", product["price"])
        print("Model:", product["model"])
        print("Color:", product["color"])
        print("Stock:", product["stock"])
        print("Discount:", product["discount"], "%")


# 9. Get Specific Product

def get_specific_product():
    product_id = input("Enter product ID: ")
    try:
        product = products.find_one({
            "_id": ObjectId(product_id)
        })
        if product:
            print("-------------------------")
            print("ID:", product["_id"])
            print("Name:", product["name"])
            print("Price:", product["price"])
            print("Model:", product["model"])
            print("Color:", product["color"])
            print("Stock:", product["stock"])
            print("Discount:", product["discount"], "%")
        else:
            print("🙁 Product not found.")
    except:
        print("❌ Invalid product ID.")


# 10. Update Product

def update_product():
    product_id = input("Enter product ID: ")

    try:
        product = products.find_one({"_id": ObjectId(product_id)})
        if product:
            price = input("Enter new price: ")
            name = input("Enter new name: ")
            color = input("Enter new color: ")
            stock = input("Enter new stock: ")
            discount = input("Enter new discount: ")
            update_data = {}
            if price.strip():
                update_data["price"] = float(price)
            if name.strip():
                update_data["name"] = name
            if color.strip():
                update_data["color"] = color
            if stock.strip():
                update_data["stock"] = int(stock)
            if discount.strip():
                update_data["discount"] = float(discount)
            if update_data:
                products.update_one(
                    {"_id": ObjectId(product_id)},{"$set": update_data})
                print("✅ Product updated successfully.")
            else:
                print("⚠️ No changes made.")
        else:
            print("❌ Product not found.")
    except:
        print("❌ Invalid product ID.")


# 11. Delete Product

def delete_product():
    product_id = input("Enter product ID: ")
    try:
        result = products.delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count > 0:
            print("✅ Product deleted successfully.")
        else:
            print("🙁 Product not found.")
    except:
        print("❌ Invalid product ID.")


# 12. Order Product

def order_product():
    user_id = input("Enter user ID: ")
    product_id = input("Enter product ID: ")
    quantity = int(input("Enter quantity: "))
    try:
        user = users.find_one({"_id": ObjectId(user_id)})
        product = products.find_one({"_id": ObjectId(product_id)})
        if not user:
            print("🙁 User not found.")
            return
        if not product:
            print("🙁 Product not found.")
            return
        if product["stock"] < quantity:
            print("Not enough stock.")
            return

        
        # Calculate amount after discount
        price = product["price"]
        discount = product["discount"]
        discounted_price = price - (price * discount / 100)
        amount = discounted_price * quantity


        # Decrease stock
        products.update_one(
            {"_id": ObjectId(product_id)},{"$inc": {"stock": -quantity}}
        )

        # Create order
        order_data = {
            "userId": ObjectId(user_id),
            "productId": ObjectId(product_id),
            "amount": amount,
            "isPaid": False,
            "quantity": quantity,
            "orderedDate": datetime.now(),
            "isDelivered": False
        }

        result = orders.insert_one(order_data)
        print("🛒 Order placed successfully.")
        print("Order ID:", result.inserted_id)
        print("Amount:", amount)
        updated_product = products.find_one({"_id": ObjectId(product_id)})
        print("Remaining stock:", updated_product["stock"])
    except:
        print("Invalid User ID or Product ID.")


# 13. Get All Ordered Product + User Details

def get_all_orders():
    result = orders.aggregate([
                {
            "$lookup": {
                "from": "users",
                "localField": "userId",
                "foreignField": "_id",
                "as": "user"
            }
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "productId",
                "foreignField": "_id",
                "as": "product"
            }
        }
    ])
    for order in result:
        print("-------------------------")
        print("Order ID:", order["_id"])
        print("Quantity:", order["quantity"])
        print("Amount:", order["amount"])
        print("Paid:", order["isPaid"])
        print("Delivered:", order["isDelivered"])
        print("Ordered Date:", order["orderedDate"])

        if len(order["user"]) > 0:
            print("User Name:", order["user"][0]["name"])
            print("User Email:", order["user"][0]["email"])

        if len(order["product"]) > 0:
            print("Product Name:", order["product"][0]["name"])
            print("Product Price:", order["product"][0]["price"])


# 14. Get Orders By User ID

def get_orders_by_user():
    user_id = input("Enter user ID: ")
    try:
        result = orders.aggregate([
            {
                "$match": {"userId": ObjectId(user_id)}
            },
            {
                "$lookup": {
                    "from": "products",
                    "localField": "productId",
                    "foreignField": "_id",
                    "as": "product"
                }
            }
        ])
        found = False
        for order in result:
            found = True
            print("-------------------------")
            print("Order ID:", order["_id"])
            print("Quantity:", order["quantity"])
            print("Amount:", order["amount"])
            print("Paid:", order["isPaid"])
            print("Delivered:", order["isDelivered"])
            if len(order["product"]) > 0:
                print("Product:", order["product"][0]["name"])
        if not found:
            print("No orders found for this user.")
    except:
        print("Invalid user ID.")


# 15. Update isDelivered = True

def update_delivery():
    order_id = input("Enter order ID: ")
    try:
        result = orders.update_one(
            {"_id": ObjectId(order_id)},{"$set": {"isDelivered": True}}
        )
        if result.modified_count > 0:
            print("Delivery status updated successfully.")
            print("isDelivered: True")
        else:
            print("Order not found or already delivered.")
    except:
        print("Invalid order ID.")


# Main Menu

while True:

    print("                     WELCOME TO RAJI'S ELECTRONICS")

    print("1. Add User")
    print("2. Check Email and Password")
    print("3. Get All Users")
    print("4. Get Specific User")
    print("5. Update User")
    print("6. Delete User")
    print("7. Add Product")
    print("8. Get All Products")
    print("9. Get Specific Product")
    print("10. Update Product")
    print("11. Delete Product")
    print("12. Order Product")
    print("13. Get All Orders")
    print("14. Get Orders By User")
    print("15. Update Delivery Status")
    print("0. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_user()
    elif choice == "2":
        check_login()
    elif choice == "3":
        get_all_users()
    elif choice == "4":
        get_specific_user()
    elif choice == "5":
        update_user()
    elif choice == "6":
        delete_user()
    elif choice == "7":
        add_product()
    elif choice == "8":
        get_all_products()
    elif choice == "9":
        get_specific_product()
    elif choice == "10":
        update_product()
    elif choice == "11":
        delete_product()
    elif choice == "12":
        order_product()
    elif choice == "13":
        get_all_orders()
    elif choice == "14":
        get_orders_by_user()
    elif choice == "15":
        update_delivery()
    elif choice == "0":
        print("Thank You for using Our program 🫶🏻")
        break
    else:
        print("Invalid choice.")
