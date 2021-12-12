//
//  shop.c
//  
//
//  Created by Isabella on 22/10/2021.
//

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct Product {
    char* name;
    double price;
};

struct ProductStock {
    struct Product product;
    int quantity;
};

struct Shop {
    double cash;
    struct ProductStock stock[20]; // Thats an array stock has 20 items
    int index;
};

struct Customer {
    char* name;
    double budget;
    struct ProductStock shoppingList[10];
    int index; // keeps track of value
};

void printProduct(struct Product p)
{
    printf("PRODUCT NAME: %s\nPRODUCT PRICE: €%.2f\n", p.name, p.price);
};

void printCustomer(struct Customer c)
{
    printf("--------------------------\n");
    printf("CUSTOMER NAME: %s\nCUSTOMER BUDGET: %.2f\n\n", c.name, c.budget);
    for (int i = 0; i< c.index; i++)
    {
        printf("--------------------------\n");
        printProduct(c.shoppingList[i].product);
        printf("QUANTITY: %d\n\n", c.shoppingList[i].quantity); // customer's shopping list, array item at index i, product quantity
        // cost = item quantity * price
        double cost = (c.shoppingList[i].quantity * c.shoppingList[i].product.price);
        printf("COST: €%.2f\n\n", cost);
    };
};

// Struct to create and stock shop
struct Shop createAndStockShop() 
{    
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    // Opens csv with stock & shop value
    fp = fopen("csv_files/stock.csv", "r");
    
    if (fp == NULL)
        exit(EXIT_FAILURE);

    // Gets cash balance from csv
    read = getline(&line, &len, fp);
    float cash = atof(line);
    printf("CASH IN SHOP IS %.2f\n", cash);
    
    struct Shop shop = { cash };

    // String tokeniser method
    while ((read = getline(&line, &len, fp)) != -1) {
        // printf("Retrieved line of length %zu:\n", read);
        char *n = strtok(line, ",");
        char *p = strtok(NULL, ",");
        char *q = strtok(NULL, ",");
        double price = atof(p); // converts to floating point
        int quantity = atoi(q); // converts to integer
        char *name = malloc(sizeof(char) * 50); // Dynamcally allocated new memory for holding product name
        strcpy(name, n); // makes copy of data stored in n

        // Put data from CSV file into struct
        struct Product product = { name, price };
        struct ProductStock stockItem = { product, quantity };
        // adding items to shop
        shop.stock[shop.index++] = stockItem;
        // printf("NAME OF PRODUCT: %s\n PRICE: %.2f\n QUANTITY: %d\n\n", name, price, quantity);
    }

    return shop;

}
struct Customer customerOrderCSV()
{
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen("customer1.csv", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    read = getline(&line, &len, fp);
    char *a = strtok(line, ",");
    char *b = strtok(NULL, ",");
    char *custName = malloc(sizeof(char) * 50);
    double custBudget = atof(b);
    strcpy(custName, a);
    struct Customer customer = { custName, custBudget }; 

    //struct ProductStock array[] = { StockA, StockB }
    while ((read = getline(&line, &len, fp)) != -1) {
        // code here
    }
    // return customer struct
    return customer;
}

void printShop(struct Shop *s) //added pointer
{
    printf("SHOP CASH FLOAT: €%.2f\n", s->cash);
    for (int i = 0; i < s->index; i++)
    {   
        printf("------------------------------\n");
        printProduct(s->stock[i].product);
        printf("QUANTITY AVAILABLE: %d\n", s->stock[i].quantity);
    }
}
// Display menu.
void displayMenu()
{
    // fflush(stdin); // might not need this
    printf("\n-------------------");
    printf("\nSHOP MENU\n");
    printf("-------------------");
    printf("\nView shop stock, press 1\n");
    printf("\nMake an order, press 2\n");
    printf("\nOption 3\n");
    printf("-------------------");
    printf("\nPress 0 to Exit\n");
    printf("-------------------\n");
}
// Return to menu.
void toMenu()
{   
    // Flush input.
    fflush(stdin); 
    char menu;
    printf("----------------------------\n");
    printf("To view menu press y.");
    scanf("%c", &menu);
    if (menu == 'y'){ // single quotes refers to value in a, while double refers to memory address
        displayMenu();
    }
};
double find(struct Shop s, char* name) 
{
    for (int i = 0; i < s.index; i++)
    {
        if (strcmp(name, s.stock[i].product.name) == 0){
            return s.stock[i].product.price;
        }
    }
    return -1;
}
// Main program.
int main(void)
{
    fflush(stdin);
    displayMenu();
    struct Shop shop = createAndStockShop();
    
    int choice = -1;
    while (choice != 0){
        printf("\nPlease select a menu option: ");
        scanf(" %d", &choice); // looks for input

        if (choice == 1){
            printf("Shop Stock & Status\n");
            // Prints stock items & shop balance
            printShop(&shop);
            toMenu();
        }
        else if (choice == 2){
            printf("Make an order\n");
            struct Customer customer = customerOrderCSV();
            // Check if customer has enough cash to purchase order
            
            if (customer.budget == 0) {
                printf("There is insufficient funds in your account.");
                toMenu();
            }
        }
    } //Put lengthy code in own method.
};
