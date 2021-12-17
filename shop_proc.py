''' 
Student: 
    Isabella Doyle
Module: 
    Multi-paradigm Programming 2021
Program:
    A Shop in procedural program style in python
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

def create_and_stock_shop():
    '''
        Function: 
            Populates the shop with data from csv file.
        Returns:
            s : an instance of the shop class
    '''

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


def read_customer(file_path):
    '''
        Function:
            Reads in customer csv. 
        Params: 
            file_path : csv file name - str
        Returns:
            c : customer budget - float
    '''
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
        
def print_product(p):
    '''
        Function:
            Prints out product information (product name and price).
        Params: 
            p : an instance of the Product class
    '''
    print(f'\nPRODUCT NAME: {p.name} \nPRODUCT PRICE: {p.price}')

def print_customer(c, s):
    '''
    Function: 
        Prints out customer information - customer name, budget and shopping list.
    Params:
        c : Customer - an instance of the Customer class
        s : Shop - an instance of the Shop class
    '''
    print(f'\nCUSTOMER NAME: {c.name} \nCUSTOMER BUDGET: {c.budget}')
    # Variable for storing the total of shopping list.
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
                print(f'The cost to {c.name} will be €{cost}') 
        # Add cost to total.
        total += cost
    # Prints total cost.
    print(f"\nTOTAL: €{total}")
    # Prints budget after purchase.
    print(f"{c.name} budget after purchase will be €{c.budget}\n")
    return total

def process_order(s, c):
    '''
        Function:
            Process the customer's order by checking the stock & the customer's budget. 
            If the transaction is successful, the shop's stock & budget is updated. 
        Params:
            s : an instance of Shop class
            c : an instance of Customer class
    '''
    print("\n------------------------")
    print("Processing your order...")
    print("------------------------\n")
    print("See overview below before proceeding with transaction: \n")
    
    # Initiate variable to hold total sum for shopping.
    total = 0
    
    # Loop over items in customer's shopping list
    for i in c.shopping_list:
        
        # Check if item exists in shop.
        prod = find_product(s, i.product.name)
        
        if prod == 1:
            # Counts order price.
            for p in s.stock:
                # Creates list for customer of products available & costs.
                if i.product.name == p.product.name:
                    print_product(p.product) # Prints each product in customer shopping list
                    print(f'{c.name} ORDERS {i.quantity} OF ABOVE PRODUCT')
                    
                    # Check availability of stock.
                    if i.quantity <= p.quantity:
                        cost = i.quantity * p.product.price
                        print(f'COST TO {c.name} IS €{cost}')
                        # Update shop balance. 
                        p.quantity -= i.quantity
                        
                        # Add cost to total.
                        total += cost
                    else:
                        print(f"Sorry, we do not have {i.quantity} units of this product available at this time.")
        else:
            print(f"\nSorry, we do not stock the following item: {i.product.name}")

    # Finalise order.
    print(f"\nTOTAL: €{total}")
    # Prints budget after purchase.
    prov_budget = c.budget - total
    print(f"BUDGET AFTER PURCHASE WILL BE: €{prov_budget}\n")
    # Takes input from user to proceed with order.
    proceed = input("Are you happy to complete transaction? (y/n)\n")
    if proceed == "y":
        # Checks if customer has sufficient funds. 
        if c.budget > total:
            # Updates customer's budget. 
            c.budget -= total
            print("\nTransaction successful.")
            print(f"Your new budget: €{c.budget}\n")
            # Update shop balance. 
            s.cash += total     
        else:
            print("\nDue to insufficient funds transaction CANNOT BE NOT COMPLETED.\n")

def find_product(s, item):
    '''
        Function:
            Checks if item exists in shop.
        Params:
            s : an instance of Shop class
            item : item in customer's shopping list
        Returns:
            Boolean
    '''
    for i in s.stock:
        if i.product.name == item:
            return 1
    return None

def print_shop(s):
    '''
    Function: 
        Prints out shop information - shop balance, products and stock information.
    Params:
        s : an instance of the Shop class
    '''

    # Welcome message & shop balance.
    print("\n--------------------")
    print("WELCOME TO OUR SHOP")
    print("--------------------\n")
    print(f'Shop balance: €{s.cash}\n')
    print("--------------------")
    print("SHOP ITEMS")
    print("--------------------")
    
    # Prints out each shop item and its quantity by calling print_product function.
    for item in s.stock:
        print_product(item.product)
        print(f'The Shop has {item.quantity} of the above\n')
    print("--------------------\n")

# Code adapted from: https://www.delftstack.com/howto/python/python-clear-console/
def clearConsole():
    '''
    Function: 
        Clears screen/console.
    '''
    # For windows.
    os.system('cls')
    # For linux/mac
    os.system('clear')
 
def displayMenu():
    ''' 
        Function:
            Prints menu.
    '''

    print()
    print("*******************")
    print("Shop Menu")
    print("*******************\n")
    print("Option 1: View Shop and Stock")
    print("Option 2: Place Order from CSV Shopping List")
    print("Option 3: Live Mode")
    print("Option 4: Back to Menu")
    print("Option 0: Exit Shop\n")

if __name__ == '__main__':
    '''
        The main program displays the menu. It takes an input from the user and 
        redirects the program accordingly.

        The while loop breaks when 0 is input by the user.
    '''
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
        elif choice == 2:
            # Takes input of customer name & creates a string with file path corresponding to customer list.
            cust_path = "csv_files/" + input("Please state your name associated with the CSV shopping list: ") + ".csv"
            cust = read_customer(cust_path)
            process_order(s, cust)
        elif choice == 4:
            displayMenu()
    
    # print("-------------------")
    # print()
    # #c = read_customer("csv_files/customer1.csv")
    # #print_customer(c, s)
    # # print("----------------------------------")