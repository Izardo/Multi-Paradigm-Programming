from dataclasses import dataclass, field
from typing import List
import csv

@dataclass
class Product:
    name: str
    price: float = 0.0

@dataclass 
class ProductStock:
    product: Product
    quantity: int

@dataclass 
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list) # creates empty list

# Populate shop with data from csv file.
def create_and_stock_shop():
    s = Shop()
    with open('csv_files/stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        s.cash = float(first_row[0])
        for row in csv_reader:
            p = Product(row[0], float(row[1]))
            ps = ProductStock(p, float(row[2]))
            s.stock.append(ps)
            #print(ps)
    return s
   
def read_customer(file_path):
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        c = Customer(first_row[0], float(first_row[1]))
        for row in csv_reader:
            name = row[0]
            quantity = float(row[1])
            p = Product(name)           # Creates product
            ps = ProductStock(p, quantity)
            c.shopping_list.append(ps)
        return c 
        

def print_product(p):
    print(f'\nPRODUCT NAME: {p.name} \nPRODUCT PRICE: {p.price}')

def print_customer(c, s):
    print(f'CUSTOMER NAME: {c.name} \nCUSTOMER BUDGET: {c.budget}')
    total = 0
    for item in c.shopping_list:
        for p in s.stock:
            # Check if items exist.
            if item.product.name == p.product.name:
                print_product(p.product) # Prints each product in customer shopping list
                print(f'{c.name} ORDERS {item.quantity} OF ABOVE PRODUCT')
                cost = item.quantity * p.product.price
                print(f'THE COST TO {c.name} WILL BE €{cost}')
        total += cost
    print()
    print(f"TOTAL: {total}")
        
def print_shop(s):
    print(f'SHOP HAS {s.cash} IN CASH.')
    for item in s.stock:
        print_product(item.product)
        print(f'The Shop has {item.quantity} of the above')

def displayMenu():
    print()
    print("-------------------")
    print("Shop Menu")
    print("-------------------")
    print("Option 1")
    print("Option 2")
    print("Option 3")
    print("Press 0 to exit")

#s = create_and_stock_shop()
#print_shop(s)
if __name__ == '__main__':
    # displayMenu()
    # print("-------------------")
    # print()
    s = create_and_stock_shop()
    c = read_customer("csv_files/customer1.csv")
    print_customer(c, s)
    # print("----------------------------------")