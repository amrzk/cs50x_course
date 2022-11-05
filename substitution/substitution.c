#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc == 2)
    {
        // In case one key provided
        string key = argv[1];
        int x = 0;
        int y = 0;
        for (int i = 0; i < strlen(key); i++)
        {
            for (int j = 0; j < i; j++)
            {
                if (toupper(key[i]) == toupper(key[j]))
                {
                    // Count for repeated letters
                    x += 1;
                }
            }
            if (toupper(key[i]) < 'A' || toupper(key[i]) > 'Z')
            {
                // Count for special characters
                y += 1;
            }
        }

        if (x != 0)
        {
            // Key has repeated letters
            printf("Key has %i repeated letter/s.\n", x);
            return 1;
        }
        else if (y != 0)
        {
            // Key has special characters
            printf("Key has %i special character/s.\n", y);
            return 1;
        }
        else if (strlen(key) != 26)
        {
            // Key isnot 26 characters
            printf("Key must contain 26 characters.\n");
            return 1;
        }
        else
        {
            // Check key for 26 characters
            string ptxt = get_string("plaintext: ");
            string ctxt = ptxt;
            for (int i = 0; i < strlen(ptxt); i++)
            {
                // Replace plaintxt char with char from key
                if (isupper(ptxt[i]))
                {
                    int n = ptxt[i] - 'A';
                    ctxt[i] = toupper(key[n]);
                }
                else if (islower(ptxt[i]))
                {
                    int n = ptxt[i] - 'a';
                    ctxt[i] = tolower(key[n]);
                }
                else
                {
                    ctxt[i] = ptxt[i];
                }
            }
            printf("ciphertext: %s\n", (string) ctxt);
            return 0;
        }
    }
    else
    {
        // In case too many keys are provided
        printf("Usage: ./substitution key\n");
        return 1;
    }
}