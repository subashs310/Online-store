import mysql.connector
import pandas as pd

# Establish a database connection
con = mysql.connector.connect(host="localhost", user="root", password="root", database="onlinestore")

res = con.cursor()

def customer_sign_up():
    print("Sign Up")
    first_name = input("Enter your first name: ")
    city = input("Enter your city: ")
    state = input("Enter your state: ")

    qry = "INSERT INTO customers (customer_name, city, state) VALUES (%s, %s, %s)"
    val = (first_name, city, state)
    res.execute(qry, val)
    con.commit()

    qry = "SELECT customer_id FROM customers where customer_name = %s"
    val = (first_name,)
    res.execute(qry, val)
    result = res.fetchone()
    print(f"Welcome {first_name}! Your customer id is {result[0]}")
    print("Registered successfully!")

def customer_log_in():
    customer_id = int(input("Enter your customer ID: "))

    try:
        qry = "SELECT customer_name FROM customers where customer_id= %s"
        val = (customer_id,)
        res.execute(qry, val)
        result = res.fetchone()
        name = result[0]
    except:
        print("Customer id not found")
        return

    qry = "SELECT customer_id,customer_name FROM customers"
    res.execute(qry)
    result = res.fetchall()
    list_of_ids = [row[0] for row in result]
    list_of_names = [row[1] for row in result]

    if customer_id in list_of_ids:
        print(f"Welcome {name}")
        user = input("Where to (View Booking/New Booking/Cancel Booking): ")

        if user.lower() == "view booking":
            try:
                customerid = customer_id
                qry = "select * from orders where customer_id = %s"
                val = (customerid,)
                res.execute(qry, val)
                result = res.fetchall()
                data = result
                columns = ['order id', 'customerid', 'product name', 'product id', 'quantity', 'total spend ']
                df = pd.DataFrame(data, columns=columns)
                print(df)
            except:
                print("Order not found")

        elif user.lower() == "new booking":
            qry = "SELECT * FROM products"
            res.execute(qry)
            result = res.fetchall()
            df = pd.DataFrame(result, columns=["product_id", "customer_id", "product_name", "product_quantity"])
            print(df)
            list_of_pro_id = [row[0] for row in result]
            product = int(input("Choose product ID: "))

            if product:
                qry = "SELECT * FROM products WHERE product_id = %s"
                val = (product,)
                res.execute(qry, val)
                result = res.fetchone()
                quantity = int(input("Enter the quantity of the product: "))
                confirm = input("Confirm (yes/no): ")

                if confirm.lower() == "yes":
                    if result[3] >= quantity:
                        qry = "INSERT INTO orders (customer_id, product_name, product_id, quantity, total_spend) VALUES (%s, %s, %s, %s, %s)"

                        customer_id = customer_id
                        product_name = result[2]
                        product_id = product
                        total_spend = result[1] * quantity
                        val = (customer_id, product_name, product_id, quantity, total_spend)
                        res.execute(qry, val)
                        con.commit()
                        print("Added to cart")
                        qry = "select product_quantity from products where product_id = %s"
                        val = (product,)
                        res.execute(qry, val)
                        result = res.fetchone()
                        oldstock = result[0]
                        newstock = oldstock - quantity
                        qry = "update products set product_quantity= %s where product_id = %s"
                        val = (newstock, product)
                        res.execute(qry, val)
                        con.commit()
                        print("Stocks updated")
                        qry = "select order_id from orders where customer_id = %s"
                        val = (customer_id,)
                        res.execute(qry, val)
                        result = res.fetchall()
                        orderid1 = max(result)
                        order2 = orderid1[0]
                        print("Your order id is ", order2)
                    else:
                        print("Insufficient stock for the selected product")
                else:
                    print("Operation canceled")

        else:
            customerid = customer_id
            qry = "select * from orders where customer_id = %s"
            val = (customerid,)
            res.execute(qry, val)
            result = res.fetchall()
            data = result
            columns = ['order id', 'customerid', 'product name', 'product id', 'quantity', 'total spend ']
            df = pd.DataFrame(data, columns=columns)
            print(df)

            try:
                order = int(input("Enter the order id to delete: "))
                qry = "select quantity, product_id  from orders where order_id = %s"
                val = (order,)
                res.execute(qry, val)
                result = res.fetchone()
                productid = result[1]
                oldstock = result[0]
                qry = "select product_quantity from products where product_id = %s"
                val = (productid,)
                res.execute(qry, val)
                result = res.fetchone()
                stock = result[0]
                newstock = oldstock + stock
                qry = "update products set product_quantity = %s where product_id = %s"
                val = (newstock, productid)
                res.execute(qry, val)
                con.commit()
                qry = "delete from orders where order_id = %s"
                val = (order,)
                res.execute(qry, val)
                con.commit()
                print("Order canceled")
            except:
                print("No orders found")
    else:
        print("Sign up first")

def employee_sign_up():
    print("Employee Sign Up")
    employee_name = input("Enter your name: ")
    employee_password = input("Enter your password: ")
    reenter_password = input("Re-enter your password: ")

    while employee_password != reenter_password:
        print("Passwords don't match.")
        reenter_password = input("Re-enter your password: ")

    employee_city = input("Enter your city: ")
    check = input("I agree (yes/no): ")

    if check.lower() == "yes":
        qry = "INSERT INTO employee (employee_name, employee_password, employee_city) VALUES (%s, %s, %s)"
        val = (employee_name, employee_password, employee_city)
        res.execute(qry, val)
        con.commit()

        qry = "SELECT employee_id FROM employee where employee_name = %s"
        val = (employee_name,)
        res.execute(qry, val)
        result = res.fetchone()
        print(f"Welcome {employee_name}! Your employee id is {result[0]}")
        print("Registered successfully!")

    else:
        print("You must agree to sign up.")

def employee_log_in():
    employee_id = int(input("Enter your employee ID: "))
    password = input("Enter your password: ")

    try:
        qry = "select employee_id,employee_name,employee_password from employee where employee_id =%s"
        val = (employee_id,)
        res.execute(qry, val)
        result = res.fetchone()
        userdetails = {result[0]: result[2]}
        if employee_id in userdetails and password == userdetails[employee_id]:
            print("Welcome", result[1])
            employee_action()

        else:
            print("Password does not match.")
    except:
        print("Enter password.")

def employee_action():
    employee = input("What do you want to do? (View products/Stock update/Add new products/Delete products): ")

    if employee.lower() == "view products":
        qry = "select * from products"
        res.execute(qry)
        result = res.fetchall()
        columns = ['product_id', 'price', 'product_name', 'product_quantity']
        df = pd.DataFrame(result, columns=columns)
        print(df)

    elif employee.lower() == "stock update":
        qry = "select * from products"
        res.execute(qry)
        result = res.fetchall()
        columns = ['product_id', 'price', 'product_name', 'product_quantity']
        df = pd.DataFrame(result, columns=columns)
        print(df)
        productid = int(input("Enter product id to add stocks: "))
        quantity = int(input("Enter the quantity to update: "))
        qry = "select product_quantity from products where product_id = %s"
        val = (productid,)
        res.execute(qry, val)
        result = res.fetchone()
        oldstock = result[0]
        newstock = oldstock + quantity
        confirm = input("Confirm (yes/no): ")
        if confirm.lower() == "yes":
            qry = "update products set product_quantity = %s where product_id = %s"
            val = (newstock, productid)
            res.execute(qry, val)
            con.commit()
            print("Successfully added stocks.")
        else:
            print("Operation canceled.")

    elif employee.lower() == "add new products":
        qry = "select * from products"
        res.execute(qry)
        result = res.fetchall()
        columns = ['product_id', 'price', 'product_name', 'product_quantity']
        df = pd.DataFrame(result, columns=columns)
        print(df)
        productid = int(input("Enter product id: "))
        price = float(input("Enter the price: "))
        name = input("Enter product name: ")
        quantity = int(input("Enter the quantity: "))
        confirm = input("Confirm (yes/no): ")
        if confirm.lower() == "yes":
            try:
                qry = "insert into products (product_id,price,product_name,product_quantity) values (%s,%s,%s,%s)"
                val = (productid, price, name, quantity)
                res.execute(qry, val)
                con.commit()
                print("Product added.")
            except:
                print("Something went wrong. Try again.")
        else:
            print("Operation canceled.")

    elif employee.lower() == "delete products":
        qry = "select * from products"
        res.execute(qry)
        result = res.fetchall()
        columns = ['product_id', 'price', 'product_name', 'product_quantity']
        df = pd.DataFrame(result, columns=columns)
        print(df)
        product = int(input("Enter product id to delete: "))
        confirm = input("Confirm (yes/no): ")
        if confirm.lower() == "yes":
            qry = "delete from products where product_id = %s"
            val = (product,)
            res.execute(qry, val)
            con.commit()
            print("Product removed.")
        else:
            print("Operation canceled.")

# Main menu
print("Welcome to the Online Store")

# Sidebar navigation
rad = input("Navigator (Customer/Employee - 1/2): ")

if rad.lower() == "customer" or rad == "1":
    selected_option = input("Select an option (Sign Up/Log In - 1/2): ")

    if selected_option.lower() == "sign up" or selected_option == "1":
        customer_sign_up()

    elif selected_option.lower() == "log in" or selected_option == "2":
        customer_log_in()

    else:
        print("Invalid option.")

elif rad.lower() == "employee" or rad == "2":
    selected_option = input("Select an option (Sign Up/Log In - 1/2): ")

    if selected_option.lower() == "sign up" or selected_option == "1":
        employee_sign_up()

    elif selected_option.lower() == "log in" or selected_option == "2":
        employee_log_in()

    else:
        print("Invalid option.")

else:
    print("Invalid navigator.")
