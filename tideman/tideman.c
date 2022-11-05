#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);
        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // TODO

    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i; // Correlate bet. the name's rank & their Candidates[index]
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // TODO
    // +1 to the candidate with index (ranks[i]) over candidate with index (ranks[j])
    for (int i = 0; i < candidate_count; i++)
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    int k = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            // assign the index (row) of the winner
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[k].winner = i;
                pairs[k].loser = j;
                k++;
            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[k].winner = j;
                pairs[k].loser = i;
                k++;
            }
        }
    }

    pair_count = k;
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // TODO
    void merge_sort(pair array[], int key[], int L, int H);
    int pair_strength[pair_count];
    for (int i = 0; i < pair_count; i++)
    {
        // Strength of the pair's winner
        pair_strength[i] = preferences[pairs[i].winner][pairs[i].loser];
    }
    merge_sort(pairs, pair_strength, 0, pair_count - 1);
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // TODO
    bool cycle(int winner, int loser);
    for (int i = 0; i < pair_count; i++)
    {
        if (cycle(pairs[i].winner, pairs[i].loser))
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    // TODO
    typedef struct
    {
        int index;
        int edge;
    }
    win;

    // Winner contains how many edges ar pointed at a candidate
    win winner[candidate_count];
    for (int i = 0; i < candidate_count; i++)
    {
        // Populate winner
        winner[i].index = i;
        winner[i].edge = 0;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        // Count edgeds pointed at each candidate
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] ? winner[j].edge++ : 0;
        }
    }

    // Sort the candidates by edges pointed at them
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = 0; j < candidate_count - 1 - i; j++)
        {
            if (winner[j].edge > winner[j + 1].edge)
            {
                win tmp = winner[j];
                winner[j] = winner[j + 1];
                winner[j + 1] = tmp;
            }
        }
    }

    printf("%s\n", candidates[winner[0].index]);
    return;
}

// ------------- Additional functions -------------
// Devide an array in halves using a key array
void merge_sort(pair array[], int key[], int L, int H)
{
    void merge(pair array[], int key[], int L, int M, int H);
    // Find the mid(index) point between Low(index) and High(index)
    if (L < H)
    {
        int M = (L + H) / 2;
        merge_sort(array, key, L, M);
        merge_sort(array, key, M + 1, H);
        merge(array, key, L, M, H);
    }
    return;
}
// Sort an array using a key array
void merge(pair array[], int key[], int L, int M, int H)
{
    // Merge sort an array using a key
    // length of left and right arrays
    int c1 = M - L + 1;
    int c2 = H - M;

    // tmp left and right arrays
    pair arr_L[c1], arr_R[c2];
    int key_L[c1], key_R[c2];

    // fill tmp arrays
    for (int i = 0; i < c1; i++)
    {
        arr_L[i] = array[L + i];
        key_L[i] = key[L + i];
    }
    for (int j = 0; j < c2; j++)
    {
        arr_R[j] = array[M + j + 1];
        key_R[j] = key[M + j + 1];
    }

    // merge left and right into main array
    int i = 0;
    int j = 0;
    int k = L;
    while (c1 > i && c2 > j)
    {
        if (key_L[i] >= key_R[j])
        {
            array[k] = arr_L[i];
            key[k] = key_L[i];
            i++;
        }
        else
        {
            array[k] = arr_R[j];
            key[k] = key_R[j];
            j++;
        }
        k++;
    }

    // Remaining array
    while (c1 > i)
    {
        array[k] = arr_L[i];
        key[k] = key_L[i];
        i++;
        k++;
    }
    while (c2 > j)
    {
        array[k] = arr_R[j];
        key[k] = key_R[j];
        j++;
        k++;
    }
}
// Check if pair would create a cycle!
bool cycle(int winner, int loser)
{
    // Check if the loser have won before
    // if the loser ever won in any cycle against the winner & return false
    int j = 0;
    while (j < candidate_count)
    {
        if (locked[loser][j] == true)
        {
            if (winner == j || !cycle(winner, j))
            {
                return false;
            }
        }
        j++;
    }
    return true;
}
