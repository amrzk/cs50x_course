#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

double letter(string txt);
double sentence(string txt);
int main(void)

{
    string text =  get_string("Text: ");
    int index;

    // Coleman-Liau index formula
    index = round(0.0588 * letter(text) - 0.296 * sentence(text) - 15.8);
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

double letter(string txt)
{
    long L = 0;
    long w = 1;

    for (int i = 0; i < strlen(txt); i++)
    {
        // Get number of letters
        if ((txt[i] >= 'A' && txt[i] <= 'Z') || (txt[i] >= 'a' && txt[i] <= 'z'))
        {
            L++;
        }
        // Get number of words
        if (txt[i] == ' ')
        {
            w++;
        }
    }
    // Get the average letters in 100 words
    double avg = ((double) L / (double) w) * 100;
    return avg;
}

double sentence(string txt)
{
    long w = 1;
    long s = 0;

    for (int i = 0; i < strlen(txt); i++)
    {
        // Get number of words
        if (txt[i] == ' ')
        {
            w++;
        }
        // Get number of sentences
        if (txt[i] == '.' || txt[i] == '?' || txt[i] == '!')
        {
            s++;
        }
    }
    // Get the average sentences in 100 words
    double avg = ((double) s / (double) w) * 100;
    return avg;
}