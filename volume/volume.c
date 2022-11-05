// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]); // Converts string to float

    // TODO: Copy header from input file to output file

    uint8_t ch[HEADER_SIZE];
    fread(ch, sizeof(uint8_t), HEADER_SIZE, input);
    fwrite(ch, sizeof(uint8_t), HEADER_SIZE, output);

    // TODO: Read samples from input file and write updated data to output file

    // Get the size of the file
    fseek(input, 0, SEEK_END);
    int size = ftell(input);
    int SAMPLE_SIZE = (size - HEADER_SIZE) / 2; // Sample size is per 2 bytes

    fseek(input, HEADER_SIZE, SEEK_SET);

    int16_t smpl[SAMPLE_SIZE];
    fread(smpl, sizeof(int16_t), SAMPLE_SIZE, input);

    for (int i = 0; i < SAMPLE_SIZE; i++)
    {
        smpl[i] *= factor;
    }

    fwrite(smpl, sizeof(int16_t), SAMPLE_SIZE, output);

    // Close files
    fclose(input);
    fclose(output);
}
