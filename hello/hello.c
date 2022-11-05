#include <stdio.h>
#include <cs50.h>
// hello, stranger :)
int main(void)
{
    string name = get_string("wha's your name? ");
    printf("hello, %s\n", name);
}