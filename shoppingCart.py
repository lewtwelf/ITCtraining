from sqlalchemy import text, Table, Column, Integer, String, Float, MetaData, create_engine, insert, select, update, delete, select

class shoppingKart():
    def __init__(self):
        # establish container connection
        self.engine = create_engine("postgresql+psycopg2://admin:admin123@127.0.0.1:5432/testdb")
        self.metadata = MetaData()

        # create inventory table
        self.items = Table('items', self.metadata,
                    Column('serialno', Integer, primary_key=True),
                    Column('name', String),
                    Column('quantity', Integer),
                    Column('cost', Float))
        self.metadata.create_all(self.engine)

        # clear inventory table
        with self.engine.connect() as conn:
            conn.execute(delete(self.items))
            conn.commit()

        # create empty basket
        self.basket = []
    
     # add item to inventory
    def addItem(self, serialNo, itemName, quantity, cost):
        with self.engine.connect() as conn:
            conn.execute(insert(self.items), {"serialno": serialNo, "name": itemName, "quantity": quantity, "cost": cost})
            conn.commit()


    # remove quantity from inventory
    def remItem(self, serialNo, quantity):
        with self.engine.connect() as conn:
            # select item using serialno
            result = conn.execute(select(self.items.c.quantity).where(self.items.c.serialno == serialNo))
            row = result.fetchone()
            # if no item with serialno
            if row is None:
                print(f"item with serialno {serialNo} not found.")
                return
            # get item quantity in inventory
            current_qty = row[0]
            new_qty = current_qty - quantity
            # if quantity is 0 remove item from inventory
            if new_qty <= 0:
                conn.execute(delete(self.items).where(self.items.c.serialno == serialNo))
            # else lowers quantity by amount specified
            else:
                conn.execute(update(self.items).where(self.items.c.serialno == serialNo).values(quantity=new_qty))
            conn.commit()

    # add item to in-memory basket
    def addToBasket(self, serialNo, quantity):
        with self.engine.connect() as conn:
            result = conn.execute(select(self.items).where(self.items.c.serialno == serialNo))
            row = result.fetchone()
            # if no item with serialno
            if row is None:
                print(f"item with serialno {serialNo} not found in inventory.")
                return
            # get item quantity in inventory
            inv_qty = row[2]
            # if quantity request is larger than inventory quantity
            if quantity > inv_qty:
                print(f"only {inv_qty} available, adding {inv_qty} to basket.")
                quantity = inv_qty
            for item in self.basket:
                # if item already in basket increase quantity
                if item['serialno'] == serialNo:
                    item['quantity'] += quantity
                    break
                # else add new item to basket
                else:
                    self.basket.append({
                        'serialno': serialNo,
                        'name': row[1],
                        'quantity': quantity,
                        'cost': row[3]})
            print(f"added {quantity} x {row[1]} to basket.")

    # on checkout remove items from inventory and print bill
    def checkout(self):
        # check if empty
        if not self.basket:
            print("basket is empty")
            return
        total = 0
        print("\n--- bill ---")
        # calc subtotal & remove item
        for item in self.basket:
            subtotal = item['quantity'] * item['cost']
            total += subtotal
            print(f"{item['name']}: {item['quantity']} x £{item['cost']:.2f} = £{subtotal:.2f}")
            self.remItem(item['serialno'], item['quantity'])
        self.basket.clear()
        print(f"total: £{total:.2f}\nthank you for your purchase!")

    # print inventory
    def getInventory(self):
        with self.engine.connect() as conn:
            result = conn.execute(select(self.items)).fetchall()
        print("\ninventory:")
        for row in result:
            print(row)

    # print basket
    def getBasket(self):
        print("\nbasket:")
        for item in self.basket:
            print(item)

# /\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\

session1 = shoppingKart()

items_to_insert = [
    {'serialno': 1, 'name': 'Notebook', 'quantity': 50, 'cost': 2.50},
    {'serialno': 2, 'name': 'Pen', 'quantity': 200, 'cost': 0.99},
    {'serialno': 3, 'name': 'Backpack', 'quantity': 20, 'cost': 35.00},
    {'serialno': 4, 'name': 'Calculator', 'quantity': 25, 'cost': 12.75},
    {'serialno': 5, 'name': 'Mug', 'quantity': 60, 'cost': 6.50},
    {'serialno': 6, 'name': 'Lamp', 'quantity': 15, 'cost': 22.99},
    {'serialno': 7, 'name': 'Chair', 'quantity': 10, 'cost': 49.99}]

for item in items_to_insert:
    session1.addItem(item['serialno'], item['name'], item['quantity'], item['cost'])

session1.getInventory()

session1.remItem(1, 10)
session1.remItem(2, 5)

session1.getInventory()

# Add items to basket
session1.addToBasket(5, 2)
session1.addToBasket(6, 3)
session1.addToBasket(7, 10)

# Checkout
session1.checkout()

session1.getInventory()  # inventory updated after purchase
