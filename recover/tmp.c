#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

char output[9] = "000.jpeg";
int main (void)
{
    for (int i = 0; i < 10; i++)
    {
        sprintf(output, "%03i.jpeg", i);
        printf("%s\n", output);
    }
}