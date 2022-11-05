#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int avg = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtRed = avg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE tmp = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE img[height][width];
    int B, G, R;
    float factor;

    for (int i = 0; i < height; i++)
    {
        // Copy
        for (int j = 0; j < width; j++)
        {
            img[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // by pixel
            B = 0;
            G = 0;
            R = 0;
            factor = 0; // Edge factor is 3, corner factor is 5

            for (int ii = i - 1; ii <= i + 1; ii++)
            {
                for (int jj = j - 1; jj <= j + 1; jj++)
                {
                    if (ii >= 0 && jj >= 0 && ii < height && jj < width)
                    {
                        B += img[ii][jj].rgbtBlue;
                        G += img[ii][jj].rgbtGreen;
                        R += img[ii][jj].rgbtRed;
                    }
                    else
                    {
                        factor++;
                    }
                }
            }

            image[i][j].rgbtBlue = round(B / (9 - factor));
            image[i][j].rgbtGreen = round(G / (9 - factor));
            image[i][j].rgbtRed = round(R / (9 - factor));
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE img[height][width];
    int Gxb, Gxg, Gxr;
    int Gyb, Gyg, Gyr;
    double Gb, Gg, Gr;

    // Sobel operators
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++)
    {
        // Copy
        for (int j = 0; j < width; j++)
        {
            img[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // by pixel
            // Reset Pixel value to 0
            Gxb = 0;
            Gxg = 0;
            Gxr = 0;

            Gyb = 0;
            Gyg = 0;
            Gyr = 0;

            for (int ii = i - 1; ii <= i + 1; ii++)
            {
                for (int jj = j - 1; jj <= j + 1; jj++)
                {
                    if (ii >= 0 && jj >= 0 && ii < height && jj < width)
                    {
                        // Sum of (pixel channel value x corresponding Sobel) operator in each direction
                        Gxb += (img[ii][jj].rgbtBlue * Gx[ii - i + 1][jj - j + 1]) ;
                        Gxg += (img[ii][jj].rgbtGreen * Gx[ii - i + 1][jj - j + 1]);
                        Gxr += (img[ii][jj].rgbtRed * Gx[ii - i + 1][jj - j + 1]);

                        Gyb += (img[ii][jj].rgbtBlue * Gy[ii - i + 1][jj - j + 1]) ;
                        Gyg += (img[ii][jj].rgbtGreen * Gy[ii - i + 1][jj - j + 1]);
                        Gyr += (img[ii][jj].rgbtRed * Gy[ii - i + 1][jj - j + 1]);
                    }
                }
            }

            // SRSS GX & GY for each channel
            Gb = round(sqrt(pow(Gxb, 2) + pow(Gyb, 2)));
            Gg = round(sqrt(pow(Gxg, 2) + pow(Gyg, 2)));
            Gr = round(sqrt(pow(Gxr, 2) + pow(Gyr, 2)));

            // GX & GY capped at 0, 255
            Gb > 255 ? Gb = 255 : (Gb < 0 ? Gb = 0 : 0);
            Gg > 255 ? Gg = 255 : (Gg < 0 ? Gg = 0 : 0);
            Gr > 255 ? Gr = 255 : (Gr < 0 ? Gr = 0 : 0);

            image[i][j].rgbtBlue = Gb;
            image[i][j].rgbtGreen = Gg;
            image[i][j].rgbtRed = Gr;
        }
    }
    return;
}
