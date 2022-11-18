import sqlite3
connection = sqlite3.connect('mydb.db')
connection.execute("PRAGMA foreign_key = 1")
my_cursor = connection.cursor()

query = (""" CREATE TABLE IF NOT EXISTS user
        (UserId         INTEGER         PRIMARY KEY AUTOINCREMENT,
        Username        TEXT            NOT NULL,
        Password        TEXT            NOT NULL);""")

query2 = (""" CREATE TABLE IF NOT EXISTS product
            (ProductId       INTEGER      PRIMARY KEY AUTOINCREMENT,
            ProductName      TEXT         NOT NULL,
            ProductPrice     INTEGER      NOT NULL);""")

query3 = """ CREATE TABLE IF NOT EXISTS cart (
    Customer_id INTEGER REFERENCES user(UserId) ,
    CartProductId INTEGER REFERENCES product(ProductId) );"""


query4 = """ CREATE TABLE IF NOT EXISTS order (
            OrderCustomerId INTEGER REFERENCES user(UserId) ,
            OrderProductId INTEGER REFERENCES product(ProductId)
            """


my_cursor.execute(query)
my_cursor.execute(query2)
my_cursor.execute(query3)


class IdGenerator:
    def __init__(self):
        self.id_number = 0

    def generate_id(self):
        self.id_number += 1
        return self.id_number


user_id_generated_instance = IdGenerator()
product_id_generated_instance = IdGenerator()
cart_id_generator = IdGenerator()
order_id_generator = IdGenerator()


class ListOfThings:
    user_list = []
    product_list = []
    cart_list = []
    order_list = []


class User:
    def __init__(self,  username, password):
        self.username = username
        self.password = password

    @staticmethod
    def create_user_from_input():
        username_input = input("Create Username")
        password_input = input("Create Password")
        new_user = User(username_input, password_input)
        ListOfThings.user_list.append(new_user)
        query_add_to_db = "INSERT INTO user (username,password) VALUES (?,?)"
        my_cursor.execute(query_add_to_db, (new_user.username, new_user.password))
        connection.commit()

    @staticmethod
    def load():
        my_cursor.execute("""SELECT * FROM user""")
        for row in iter(my_cursor.fetchone, None):
            user = User(row[1], row[2])
            ListOfThings.user_list.append(user.__dict__)
        print("Data loaded from database")
        main()


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.id = product_id_generated_instance.generate_id()

    @staticmethod
    def create_product_from_input():
        product_name = input("PRODUCT NAME TEXT ONLY:")
        product_price = int(input("PRODUCT PRICE INT ONLY:"))
        new_product = Product(product_name, product_price)
        ListOfThings.product_list.append(new_product)
        query_add_to_db = "INSERT INTO product (ProductName,ProductPrice) VALUES (?,?)"
        my_cursor.execute(query_add_to_db, (new_product.name, new_product.price))
        connection.commit()


def main():
    # test = Product.create_product_from_input()
    user_input = input("1--show products\n"
                       "2-- show users")

    if user_input == '1':
        my_cursor.execute("SELECT * FROM user")
        print(my_cursor.fetchall())
        main()
    if user_input == '2':
        my_cursor.execute("SELECT * FROM product")
        print(my_cursor.fetchall())
        main()
    if user_input == '3':
        my_cursor.execute("SELECT * FROM user")
        list_of_tuples_user = my_cursor.fetchall()
        print(list_of_tuples_user)
        user_select_input = int(input("Select user_id to add to cart"))
        my_cursor.execute("SELECT UserId FROM user WHERE UserId = :id", {'id': user_select_input})
        user_id_data = my_cursor.fetchall()
        print(user_id_data)
        my_cursor.execute("SELECT * FROM product")
        list_of_tuples_product = my_cursor.fetchall()
        print(list_of_tuples_product)
        user_select_input_product = int(input("Select product_id to add to cart"))
        my_cursor.execute("SELECT * FROM product WHERE ProductId = :id", {'id': user_select_input_product})
        data = my_cursor.fetchall()
        # my_cursor.execute("UPDATE cart SET product_id = ? WHERE customer_id = ?", (data[0][0], list_of_tuples_user[0][0]))
        my_cursor.execute("INSERT INTO cart (Customer_id, CartProductId) VALUES (?, ?)", (user_id_data[0][0], data[0][0]))
        connection.commit()
        main()

    if user_input == 'create':
        User.create_user_from_input()
        main()

    if user_input == 'createproduct':
        Product.create_product_from_input()
        main()

    if user_input == 'viewcart':
        sql = """SELECT cart.Customer_id, cart.CartProductId, product.ProductName, product.ProductPrice, user.Username  
        FROM cart
        INNER JOIN product ON cart.CartProductId = product.ProductId
        INNER JOIN user ON cart.Customer_id = user.UserId """
        my_cursor.execute(sql)
        result = my_cursor.fetchall()
        for row in result:
            print(row)
        main()

    if user_input == 'viewspes':
        sql_select_user = """ SELECT * From user"""
        my_cursor.execute(sql_select_user)
        list_of_tuples_user = my_cursor.fetchall()
        for inx, user in enumerate(list_of_tuples_user, start=1):
            print(inx, user)
        user_selector_input = int(input("Select user to view specific cart"))
        my_cursor.execute("""SELECT cart.CartCustomer_id, cart.CartProductId, product.ProductName, product.ProductPrice
                            FROM cart
                            INNER JOIN product ON cart.CartProductId = product.ProductId
                            WHERE cart.Customer_id = ?""", (user_selector_input, ))

        list_of_specific_carts = my_cursor.fetchall()
        print(list_of_specific_carts)
        input_question = input(f"You have {len(list_of_specific_carts)} in your cart, check out? Commands: all, onebyone")
        total_cart_value = 0
        if input_question == 'all':
            for x in list_of_specific_carts:
                my_cursor.execute("""INSERT INTO (OrderProductId)""")

        append_to_order_input = int(input("SELECT AN ITEM TO CHECK OUT"))
        for i in list_of_specific_carts:
            if i[0] == append_to_order_input:
                total_cart_value += i[2]
        print(f"Total cart value is {total_cart_value}")

main()

