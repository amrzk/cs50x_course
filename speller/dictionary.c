// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Dictionary strea
FILE *dic;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

void insert(char *word);
void free_memory(node *list);

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int n = hash(word);
    // Hash table is empty
    if (table[n] == NULL)
    {
        return false;
    }

    // Clear L_word from garbage values
    char L_word[LENGTH + 1];
    for (int i = 0; i < LENGTH + 1; i++)
    {
        L_word[i] = '\0';
    }

    // Change word to lowercase
    for (int i = 0; i < strlen(word); i++)
    {
        L_word[i] = tolower(word[i]);
    }

    // Check word againest hash table
    for (node *word_check = table[n]; word_check != NULL; word_check = word_check->next)
    {
        if (strcmp(L_word, word_check->word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    return toupper(word[0]) - 'A';
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // Set all table values to null
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }

    dic = fopen(dictionary, "r");
    if (dic == NULL)
    {
        return false;
    }
    else
    {
        // Read words and insert them to a hash table
        char c;
        int index = 0;
        char dic_word[LENGTH + 1];
        while (fread(&c, sizeof(char), 1, dic))
        {
            // Read dictionary words into a string dic_word
            if (isalpha(c) || (c == '\'' && index > 0))
            {
                dic_word[index] = c;
                index++;
            }
            else if (index > 0)
            {
                dic_word[index] = '\0';
                insert(dic_word);
                index = 0;
            }
        }
        return true;
    }
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    char c;
    int new_word = 0;
    rewind(dic);
    while (fread(&c, sizeof(char), 1, dic))
    {
        // the end of a word
        if (c == '\n')
        {
            new_word++;
        }
    }
    // printf("no_words %i\n", new_word);
    return new_word;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        free_memory(table[i]);
    }
    fclose(dic);
    return true;
}


void insert(char *word)
{

    // Hash the dic_word and store it in a hash table
    int n = hash(word);
    node *new = malloc(sizeof(node));

    if (new == NULL)
    {
        unload();
        return;
    }

    strcpy(new->word, word);
    new->next = NULL;

    if (table[n] == NULL)
    {
        // First node in the table
        table[n] = new;
    }
    else
    {
        // Shift table for new node insert
        new->next = table[n];
        table[n] = new;
    }

    // remove
    // for (node *tmp = table[n]; tmp != NULL; tmp = tmp->next)
    // {
    //     printf("%s, ", tmp->word);
    // }
    //
}

void free_memory(node *list)
{
    // Free tabe[n] memory
    if (list != NULL)
    {
        free_memory(list->next);
    }
    free(list);
}

