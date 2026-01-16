/**
 * expectiminimax.c - A C, as opposed to Python, version of expectiminimax
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

#include "expectiminimax.h"

#define MAX_BOARD_DIMENSION 4
#define BLANK_TILE 0
#define TILE_2_CHANCE 0.9
#define TILE_4_CHANCE 0.1

typedef enum {
    UP,
    DOWN,
    LEFT,
    RIGHT
} Direction; // NOTE: STARTS AT 0, NOT 1!!!!!!!!!!!!!

const int SNAKE_HEURISTIC_3[4][4] = {
    {4096, 2048, 1024, 512},
    {64, 128, 256, 512},
    {64, 32, 16, 8},
    {1, 2, 4, 8}
};

int DEPTH = 5; // The defalt depth for Expectiminimax

/**
 * This returns the "best" direction to shift the tiles in the given board.
 * 
 * @param depth The search depth of the AI solver/search.
 * @param board The given 4x4 2048 board.
 * 
 * @return The best direction to move: 1: UP, 2: DOWN, 3: LEFT, 4: RIGHT
 */
int getNextDirection(int depth, int board[4][4]) {
    DEPTH = depth;
    Direction best_direction = UP;
    return best_direction + 1;
}
