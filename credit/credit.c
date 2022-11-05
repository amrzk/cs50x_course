#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    const long credit = get_long("Number: ");
    // Credit card digit check
    const long digit_12 = pow(10,12);
    const long digit_13 = pow(10,13);
    const long digit_14 = pow(10,14);
    const long digit_15 = pow(10,15);
    const long digit_16 = pow(10,16);
    long digits = credit;
    long modulo, sum;

    if(credit / digit_13 == 0 && credit / digit_12 > 0)
    {
        // Check for VISA-1 ( 13-digits, starts with 4, satisfy Luhn's)
        // Separate the credit card's digits
        for(long i = 1; digits % 10 > 0 || digits / 10 > 0; i ++)
        {
            modulo = digits % 10;
            digits /= 10;
            //Luhn's algorithm
            if(i % 2 == 0) // Sum the evens' digits of (modulo * 2)
            {
                for(long j = modulo * 2; j % 10 > 0 || j / 10 > 0; j /= 10)
                {
                    sum = sum + (j % 10);
                }
            }
            else // Sum odds to evens
            {
                sum = sum + modulo;
            }
        }
        (sum % 10 == 0) && (credit / digit_12 == 4) ? printf("VISA\n") : printf("INVALID\n");
    }
    else if(credit / digit_15 == 0 && credit / digit_14 > 0)
    {
        // Check for AMEX ( 15-digits, starts with 34-37, satisfy Luhn's)
        // Separate the credit card's digits
        for(long i = 1; digits % 10 > 0 || digits / 10 > 0; i ++)
        {
            modulo = digits % 10;
            digits /= 10;
            //Luhn's algorithm
            if(i % 2 == 0) // Sum the evens' digits of (modulo * 2)
            {
                for(long j = modulo * 2; j % 10 > 0 || j / 10 > 0; j /= 10)
                {
                    sum = sum + (j % 10);
                }
            }
            else // Sum odds to evens
            {
                sum = sum + modulo;
            }
        }
        (sum % 10 == 0) && ((credit / digit_13 == 34) || (credit / digit_13 == 37)) ? printf("AMEX\n") : printf("INVALID\n");
    }
    else if(credit / digit_16 == 0 && credit / digit_15 > 0)
    {
        // Check for Master Card && VISA-2
        // Separate the credit card's digits
        for(long i = 1; digits % 10 > 0 || digits / 10 > 0; i ++)
        {
            modulo = digits % 10;
            digits /= 10;
            //Luhn's algorithm
            if(i % 2 == 0) // Sum the evens' digits of (modulo * 2)
            {
                for(long j = modulo * 2; j % 10 > 0 || j / 10 > 0; j /= 10)
                {
                    sum = sum + (j % 10);
                }
            }
            else // Sum odds to evens
            {
                sum = sum + modulo;
            }
        }
        if(sum % 10 == 0 && credit / digit_15 ==4)
        {
            printf("VISA\n");
        }
        else if(sum % 10 == 0 && credit / digit_14 >= 51 && credit / digit_14 <= 55)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}