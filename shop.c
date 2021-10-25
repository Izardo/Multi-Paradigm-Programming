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

struct Shop createAndStockShop() 
{
    struct Shop shop = { 200 };
    
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

    fp = fopen("stock.csv", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

    while ((read = getline(&line, &len, fp)) != -1) {
        // printf("Retrieved line of length %zu:\n", read);
        char *n = strtok(line, ",");
        char *p = strtok(NULL, ",");
        char *q = strtok(NULL, ",");
        double price = atof(p); // converts to floating point data type
        int quantity = atoi(q); // converts to integer data type
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

void printShop(struct Shop s)
{
    printf("SHOP CASH FLOAT: €%.2f\n", s.cash);
    for (int i = 0; i < s.index; i++)
    {   
        printf("------------------------------\n");
        printProduct(s.stock[i].product);
        printf("QUANTITY AVAILABLE: %d\n", s.stock[i].quantity);
    }
}

int main(void)
{
    // struct Customer isabella = {"Isabella", 100.0};
    // // printf("Customer's name: %s\n", Isabella.name);
    
    // struct Product coke = {"CAN COKE", 1.10};
    // // printProduct(coke);
    // // printf("Product: %s\nPrice: %.2f\n", coke.name, coke.price);
    
    // struct Product bread = { "Bread", 0.7 };
    
    // struct ProductStock cokeStock = { coke, 20 };
    // struct ProductStock breadStock = { bread, 2 };
    
    // isabella.shoppingList[isabella.index++] = cokeStock;
    // isabella.shoppingList[isabella.index++] = breadStock;
    // printCustomer(isabella);
    // // printf("%s QUANTITY: %d\n", cokeStock.product.name, cokeStock.quantity);
    
    struct Shop shop = createAndStockShop();
    printShop(shop);

};
