#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Ask for the height
    int size;
    do
    {
        size = get_int("Pyramid size: ");
    }
    while (size < 1 || size > 8);

    //  draws the pyramid
    int i = size;
    while (i > 0)
    {
        // Rows
        for (int j = 1; j < i; j++) // Spaces befor blocks
        {
            printf(" ");
        }
        for (int j = size; j >= i; j--) // First half of blocks
        {
            printf("#");
        }
        printf("  "); // Space between blocks
        for (int j = size; j >= i; j--) // Second half of blocks
        {
            printf("#");
        }

        // move to next row
        printf("\n");
        i--;
    }
}