''' A Shop in procedural program style in python
    Difference: in procedeural the data is seperate from the functions
    in oop they exist in one construct; the class.
    
'''

from dataclasses import dataclass, field
from typing import List
import csv
import os # To clear screen.

# Class contains information about the product - product name and price.
@dataclass
class Product:
    name: str
    price: float = 0.0

# Class contains information about the product stock - product and quantity. 
@dataclass 
class ProductStock:
    product: Product
    quantity: int

# Class contains information about the shop - cash balance and product stock.
@dataclass 
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)

# Class contains information about the customer - name, budget and shopping list. 
@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductStock] = field(default_factory=list) # creates empty list

# Function to populate shop with data from csv file.
def create_and_stock_shop():
    
    # Instantiate an instance of Shop class.
    s = Shop()
    
    # Opens stock.csv file.
    with open('csv_files/stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        # Reads in shop value and stores the value of shop in variable s. 
        first_row = next(csv_reader)
        s.cash = float(first_row[0])
        
        # Loops through rows, extracting information to create class instances of Product and ProductStock
        for row in csv_reader:
            p = Product(row[0], float(row[1]))
            ps = ProductStock(p, float(row[2]))
            s.stock.append(ps)
            #print(ps)
    
    return s    # Instance of Shop class

# Function to read in customer csv. 
def read_customer(file_path):
    
    # Opens the csv file.
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        # Reads in first row (budget) and assigns it to variable c. 
        first_row = next(csv_reader)
        c = Customer(first_row[0], float(first_row[1]))
        
        # Loops through rows, extracting information to create a shopping list. 
        for row in csv_reader:
            name = row[0]
            quantity = float(row[1])
            p = Product(name)           # Creates product
            ps = ProductStock(p, quantity)
            c.shopping_list.append(ps)
        
        return c 
        
# Function to print out product information - product name and price.
def print_product(p):
    print(f'\nPRODUCT NAME: {p.name} \nPRODUCT PRICE: {p.price}')

# Function to print out customer information - customer name, budget and shopping list.
def print_customer(c, s):
    
    print(f'\nCUSTOMER NAME: {c.name} \nCUSTOMER BUDGET: {c.budget}')
    
    # Variable for storing the total cash price.
    total = 0
    
    # Loop over each item in shopping list. 
    for item in c.shopping_list:
        
        # Loop over products.
        for p in s.stock:

            # Check if items exist.
            if item.product.name == p.product.name:
                print_product(p.product) # Prints each product in customer shopping list
                print(f'{c.name} ORDERS {item.quantity} OF ABOVE PRODUCT')
                cost = item.quantity * p.product.price
                print(f'THE COST TO {c.name} WILL BE €{cost}')
        
        # Calculate total cost for items.
        total += cost
    
    # Prints total cost.
    print(f"\nTOTAL: {total}")

# Function to print out shop information - shop balance, products and stock information.        
def print_shop(s):
    print("\n--------------------")
    print("WELCOME TO OUR SHOP")
    print("--------------------\n")
    print(f'Shop balance: €{s.cash}\n')
    print("--------------------")
    print("SHOP ITEMS")
    print("--------------------")
    # Prints out each shop item and its quantity. 
    for item in s.stock:
        print_product(item.product)
        print(f'The Shop has {item.quantity} of the above\n')
    print("--------------------\n")

# Function to clear screen/console. Adapted from: https://www.delftstack.com/howto/python/python-clear-console/
def clearConsole():
    # For windows.
    os.system('cls')
    # For linux/mac
    os.system('clear')

# Main menu. 
def displayMenu():
    print()
    print("*******************")
    print("Shop Menu")
    print("*******************\n")
    print("Option 1: View Shop and Stock")
    print("Option 2: Place Order with Shopping List")
    print("Option 3: Live Mode")
    print("Option 4: Back to Menu")
    print("Option 0: Exit Shop\n")

#s = create_and_stock_shop()
#print_shop(s)
# Main program.
if __name__ == '__main__':
    
    # Store function in a variable to be accessed later.
    s = create_and_stock_shop()
    
    # Displays the main menu.
    displayMenu()

    # Initiates value for while loop. 
    choice = -1

    # While loop terminates when 0 is entered.
    while choice != 0:
        choice = int(input("Please choose one of the menu options: \n"))
    
        if choice == 1:
            print_shop(s)

        elif choice == 4:
            displayMenu()
    
    # print("-------------------")
    # print()
    # #c = read_customer("csv_files/customer1.csv")
    # #print_customer(c, s)
    # # print("----------------------------------")