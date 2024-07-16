# Description
There's a flag shop selling stuff, can you buy a flag? Source. Connect with nc jupiter.challenges.picoctf.org 4906.

# Provided
- [store.c](.prov/49-store.c)

# Progress
## First impression
First thing i do is connecting to the server and see what my options are:
```
Welcome to the flag exchange
We sell flags

1. Check Account Balance

2. Buy Flags

3. Exit

 Enter a menu selection
```
So....
- 1 provides the information about our account balance (1100) and throws us back in the menu
- 2 allows us to buy stuff
  - 1 Definitely not the Flag (900)
  - 2 1337 Flag (100000)
- 3 exits, duh

So the only thing i can interact with is the 2nd option:
- 1 asks for the amount of flags i want to buy
- 2 only allows 1 as an input to confirm the purchase

## Little bit of Testing
First of all i try to buy the 1337 Flag:
```
Not enough funds for transaction
```
who would have thought....

Next the other flag. I buy one:
```
The final cost is: 900

Your current balance after transaction: 200
```
I try to buy a 2nd:
```
The final cost is: 900
Not enough funds to complete purchase
```

I'm stuck now, unable to do anything. So time for a reconnect:
So as this is still the only thing i can interact with i try to buy more than one flag, like 100:
```
The final cost is: 90000
Not enough funds to complete purchase
```

What about a negative value: directly back to the main menu....

Time to look at the code, i guess:

## Analyse
```
int account_balance = 1100;
```
``` c
else if(menu == 2){
printf("Currently for sale\n");
printf("1. Defintely not the flag Flag\n");
printf("2. 1337 Flag\n");
int auction_choice;
fflush(stdin);
scanf("%d", &auction_choice);
if(auction_choice == 1){
    printf("These knockoff Flags cost 900 each, enter desired quantity\n");

    int number_flags = 0;
    fflush(stdin);
    scanf("%d", &number_flags);
    if(number_flags > 0){
        int total_cost = 0;
        total_cost = 900*number_flags;
        printf("\nThe final cost is: %d\n", total_cost);
        if(total_cost <= account_balance){
            account_balance = account_balance - total_cost;
            printf("\nYour current balance after transaction: %d\n\n", account_balance);
        }
        else{
            printf("Not enough funds to complete purchase\n");
        }


    }
```
This seem to be the relevant parts for now. As i definitely need to buy a quantity different than 1 and i can't buy negative amounts, it has to be more. So how does the check work....
``` c
        total_cost = 900*number_flags;
        if(total_cost <= account_balance){
```
Wait a second, is this an overflow issue? I see nothing that would prevent an overflow....

Checking the int limits: [Wikipedia](https://en.wikipedia.org/wiki/C_data_types) -32767 - +32767, I thought int was bigger... oh well

$$
x\cdot900>32767\\
x>\frac{32767}{900}\\
x>36.4
$$

So 37 flags should do it?
```
The final cost is: 33300
Not enough funds to complete purchase
```

WHAT?? HOW?? That'S bigger than the limit....<br>
[Google](https://www.google.com/search?q=max+int+c): 
```
2147483647
INT_MAX in C/C++
INT_MAX is a macro that specifies that an integer variable cannot store any value beyond this limit. It represents the maximum value of the upper limit of the integer data type in C/C++. The value of INT_MAX is: INT_MAX = 2147483647 (for 32-bit Integers)
```

for 32 bit hmm, while wikipedia says 16bit.... Whatever
$$
x\cdot900>2147483647\\
x>\frac{2147483647}{900}\\
x>2386092.94111
$$

That's a lot of flags but hey guess it's time to buy 2386093 flags...
```
The final cost is: -2147483596

Your current balance after transaction: -2147482600
```

Hah, time to buy the l33t flag:
```
Not enough funds for transaction
```

Wait a second.... Account Balance?
```
 Balance: -2147482600
```

Ah i see i first overflowed the cost and then i overflowed the balance. So more flags to get rid of the 1100 account balance? basically $x\cdot900>2147483647+1100$?

What am i doing $1100/900=1.\text{something}$, just add 2 on the flag count and it should be fine:

```
These knockoff Flags cost 900 each, enter desired quantity
2386095

The final cost is: -2147481796

Your current balance after transaction: 2147482896
```
Now i can buy the flag:
```
1337 flags cost 100000 dollars, and we only have 1 in stock
Enter 1 to buy one1
YOUR FLAG IS: picoCTF{m0n3y_bag5_9c5fac9b}
```
