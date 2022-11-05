#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;
const int BLOCK_SIZE = 512;
char output[8] = "000.jpg";
bool state = false;
int i = 0;

int main(int argc, char *argv[])
{
    // Check arguments
    if (argc != 2)
    {
        printf("Usage: ./recover card.raw");
        return 1;
    }

    // Open memory card
    FILE *mcard = fopen(argv[1], "r");
    if (mcard == NULL)
    {
        fprintf(mcard, "not a valid card\n");
        fclose(mcard);
        return 1;
    }

    BYTE *buffer = malloc(BLOCK_SIZE);
    FILE *img;
    // Repeat until end of card:
    r// Read 512 bytes into a abuffer
    while (fread(buffer, 1, BLOCK_SIZE, mcard) == BLOCK_SIZE)
    {
        // if start of new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // First JPEG
            if (i == 0)
            {
                img = fopen(output, "w");
                fwrite(buffer, 1, BLOCK_SIZE, img);
                i++;
            }
            // Not the first JPEG
            else
            {
                fclose(img);
                sprintf(output, "%03i.jpg", i);
                img = fopen(output, "w");
                fwrite(buffer, 1, BLOCK_SIZE, img);
                i++;
            }
            state = true;
        }
        // if already found JPEG
        else if (state)
        {
            fwrite(buffer, 1, BLOCK_SIZE, img);
        }
    }
    // Close any remaining files
    fclose(img);
    fclose(mcard);
    free(buffer);
}