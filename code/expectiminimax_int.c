/**
 * This file contains the code to run Expectiminimax through C as opposed to Python.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>
#include <assert.h>

#include "expectiminimax.h"

typedef enum {
    UP, // 0 -> 1
    DOWN, // 1 -> 2
    LEFT, // 2 -> 3
    RIGHT // 3 -> 4
} Direction;

const int SNAKE_HEURISTIC_1[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION] = {
    {32768, 16384, 8192, 4096},
    {256, 512, 1024, 2048},
    {128, 64, 32, 16},
    {1, 2, 4, 8}
};
const int SNAKE_HEURISTIC_2[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION] = {
    {1073741824, 268435456, 67108864, 16777216},
    {65536, 262144, 1048576, 4194304},
    {16384, 4096, 1024, 256},
    {1, 4, 16, 64}
};
const int SNAKE_HEURISTIC_3[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION] = {
    {4096, 2048, 1024, 512},
    {64, 128, 256, 512},
    {64, 32, 16, 8},
    {1, 2, 4, 8}
};
const int SNAKE_HEURISTIC_4[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION] = {
    {16777216, 4194304, 1048576, 262144},
    {4096, 16384, 65536, 262144},
    {4096, 1024, 256, 64},
    {1, 4, 16, 64}
};
const int SNAKE_HEURISTIC_5[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION] = {
    {4096, 2048, 1024, 256},
    {32, 128, 256, 512},
    {64, 32, 16, 4},
    {1, 2, 4, 8}
};
const int SNAKE_HEURISTIC_6[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION] = {
    {512, 256, 128, 64},
    {16, 32, 64, 64},
    {16, 16, 8, 8},
    {1, 2, 4, 8}
};

int DEPTH = 8; // The defalt depth for Expectiminimax
int HEURISTIC_NUM = 3; // The default number indicating which heuristic to use

/**
 * This gets the board snake heuristic score.
 * 
 * @param board The given 4x4 2048 board.
 * @param snake_heuristic The snake heuristic to use when calculating the board's score.
 * 
 * @return The board's snake heuristic score.
 */
uint64_t get_heuristic_snake_score(const int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION], const int snake_heuristic[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION]) {
    uint64_t board_heuristic = 0;
    // int open_cells = 0;
    for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
        for (int col = 0; col < MAX_BOARD_DIMENSION; col++) {
            // if (board[row][col] == BLANK_TILE) open_cells++;
            board_heuristic += (uint64_t) board[row][col] * snake_heuristic[row][col];
        }
    }
    // return floor(board_heuristic + board_heuristic * open_cells / 16 * 0.1);
    return board_heuristic;
}

/**
 * This gets the board heuristic score.
 * 
 * @param board The given 4x4 2048 board.
 * 
 * @return The board's heuristic score.
 */
uint64_t get_heuristic_score(const int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION]) {
    switch (HEURISTIC_NUM) {
        case 1:
            return get_heuristic_snake_score(board, SNAKE_HEURISTIC_1);
        case 2:
            return get_heuristic_snake_score(board, SNAKE_HEURISTIC_2);
        case 3:
            return get_heuristic_snake_score(board, SNAKE_HEURISTIC_3);
        case 4:
            return get_heuristic_snake_score(board, SNAKE_HEURISTIC_4);
        case 5:
            return get_heuristic_snake_score(board, SNAKE_HEURISTIC_5);
        case 6:
            return get_heuristic_snake_score(board, SNAKE_HEURISTIC_6);
        default:
            return get_heuristic_snake_score(board, SNAKE_HEURISTIC_3);
    }
}

/**
 * This merges and combines numbers from right to right for a single row/column.
 * \n
 * It start are the right and merges values in the right direction.\n
 * 
 * @param list The row/column list of values to combine.
 * 
 * @return The updated row/column list of values after the being merged.
 */
void merge(int original_list[MAX_BOARD_DIMENSION], int new_list[MAX_BOARD_DIMENSION]) {
    if (original_list[0] == BLANK_TILE && original_list[1] == BLANK_TILE && 
        original_list[2] == BLANK_TILE && original_list[3] == BLANK_TILE) {
        for (int i = 0; i < MAX_BOARD_DIMENSION; i++) new_list[i] = BLANK_TILE;
        return;
    }

    int original_list_values[MAX_BOARD_DIMENSION] = {0, 0, 0, 0};
    int original_list_values_length = MAX_BOARD_DIMENSION;
    int j = 0;
    for (int i = 0; i < MAX_BOARD_DIMENSION; i++) {
        if (original_list[i] == BLANK_TILE) {
            original_list_values_length--;
        } else {
            original_list_values[j] = original_list[i];
            j++;
        }
    }

    int index = MAX_BOARD_DIMENSION - 1;
    int i = original_list_values_length - 1;
    while (i >= 0) {
        if (i - 1 >= 0 && original_list_values[i] == original_list_values[i-1]) {
            new_list[index] = original_list_values[i] * 2;
            i -= 2;
        } else {
            new_list[index] = original_list_values[i];
            i--;
        }
        index--;
    }
}

/**
 * This shifts the tiles of the given board in one of the 4 cardinal directions.
 * 
 * @param board The given 4x4 2048 board to shift.
 * @param original_board The original 4x4 2048 board before the shift.
 * @param direction The direction to shift the board tiles.
 * 
 * @return True if the tiles on the board have changed positions, False otherwise.
 */
bool shift(int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION], int original_board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION], int direction) {  
    switch (direction) {
        case UP:
            for (int col = 0; col < MAX_BOARD_DIMENSION; col++) {
                int original_col_values[MAX_BOARD_DIMENSION];
                for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
                    original_col_values[row] = board[3 - row][col]; // Column in reverse order (going up)
                }
                int final_col_values[MAX_BOARD_DIMENSION] = {0, 0, 0, 0};
                merge(original_col_values, final_col_values);
                for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
                    board[row][col] = final_col_values[3 - row];
                }
            }
            break;
        case DOWN:
            for (int col = 0; col < MAX_BOARD_DIMENSION; col++) {
                int original_col_values[MAX_BOARD_DIMENSION];
                for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
                    original_col_values[row] = board[row][col]; // Column in normal order (going down)
                }
                int final_col_values[MAX_BOARD_DIMENSION] = {0, 0, 0, 0};
                merge(original_col_values, final_col_values);
                for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
                    board[row][col] = final_col_values[row];
                }
            }
            break;
        case LEFT:
            for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
                int original_row_values[MAX_BOARD_DIMENSION];
                for (int col = 0; col < MAX_BOARD_DIMENSION; col++) {
                    original_row_values[col] = board[row][3 - col]; // Row in reverse order
                }
                int final_row_values[MAX_BOARD_DIMENSION] = {0, 0, 0, 0};
                merge(original_row_values, final_row_values);
                for (int col = 0; col < MAX_BOARD_DIMENSION; col++) {
                    board[row][col] = final_row_values[3 - col];
                }
            }
            break;
        case RIGHT:
            for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
                int original_row_values[MAX_BOARD_DIMENSION];
                for (int col = 0; col < MAX_BOARD_DIMENSION; col++) {
                    original_row_values[col] = board[row][col]; // Row in normal order
                }
                int final_row_values[MAX_BOARD_DIMENSION] = {0, 0, 0, 0};
                merge(original_row_values, final_row_values);
                for (int col = 0; col < MAX_BOARD_DIMENSION; col++) {
                    board[row][col] = final_row_values[col];
                }
            }
            break;
        default:
            return false; // Invalid direction
    }

    for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
        for (int col = 0; col < MAX_BOARD_DIMENSION; col++) {
            if (board[row][col] != original_board[row][col]) {
                return true; // Board changed
            }
        }
    }
    return false; // Board didn't change 
}

/**
 * This checks if any cells can be merged together.
 * 
 * @param The current 4x4 2048 board to check.
 * 
 * @return True if the board can merge cells, False otherwise.
 */
bool potential_merges(int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION]) {
    for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
        for (int col = 0; col < MAX_BOARD_DIMENSION - 1; col++) {
            if (board[row][col] == board[row][col+1] || board[col][row] == board[col+1][row]) {
                return true;
            }
        }
    }
    return false;
}

/**
 * This finds all cells that are empty in the given board.
 * \n
 * The cells and board must be freed later.
 * 
 * @param board The given 4x4 2048 board.
 * @param open_cells The list to add all open cells.
 * @param num_open_cells A pointer to a variable holding the number of open cells.
 */
int **get_open_cells(int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION], int open_cells[MAX_BOARD_DIMENSION][2], int *num_open_cells) {
    for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
        for (int col = 0; col < MAX_BOARD_DIMENSION; col++) {
            if (board[row][col] == BLANK_TILE) {
                open_cells[*num_open_cells][0] = row;
                open_cells[*num_open_cells][1] = col;
                (*num_open_cells)++;
            }
        }
    }
}

/**
 * Returns the best heuristic score for the given board and depth.
 * 
 * @param board The current 4x4 2048 board to check.
 * @param current_depth The current search depth.
 * @param players_turn If it is the player's turn, shifting tiles.
 * 
 * @return The average/best heuristic score of the board overall.
 */
uint64_t get_best_score(int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION], int current_depth, bool players_turn) {
    if (current_depth == 0) return get_heuristic_score(board);
    int num_open_cells = 0;
    int open_cells[MAX_BOARD_DIMENSION][2];
    get_open_cells(board, open_cells, &num_open_cells);

    if (num_open_cells == 0 && !potential_merges(board)) {  // Game over for the board
        return get_heuristic_score(board);
    } else if (players_turn) { // Player's Turn: Tiles shift
        uint64_t highest_heuristic = 0;
        for (int direction = UP; direction <= RIGHT; direction++) {
            int copy_board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION];
            memcpy(copy_board, board, sizeof(int) * MAX_NUM_TILES);
            bool board_changed = shift(copy_board, board, direction);
            if (board_changed) {
                uint64_t heuristic = get_best_score(copy_board, current_depth - 1, false);
                if (heuristic > highest_heuristic) highest_heuristic = heuristic;
            }
        }
        return highest_heuristic;
    } else if (num_open_cells != 0) { // Game's Turn: Random tile spawn, tiles are open
        uint64_t avg_heuristic_2 = 0;
        uint64_t avg_heuristic_4 = 0;
        for (int i = 0; i < num_open_cells; i++) {
            int copy_board_2[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION];
            int copy_board_4[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION];
            memcpy(copy_board_2, board, sizeof(int) * MAX_NUM_TILES);
            memcpy(copy_board_4, board, sizeof(int) * MAX_NUM_TILES);
            int row = open_cells[i][0];
            int col = open_cells[i][1];
            copy_board_2[row][col] = 2;
            copy_board_4[row][col] = 4;
            avg_heuristic_2 += get_best_score(copy_board_2, current_depth - 1, true) / num_open_cells;
            avg_heuristic_4 += get_best_score(copy_board_4, current_depth - 1, true) / num_open_cells;
        }
        return floor(avg_heuristic_2 * TILE_2_CHANCE + avg_heuristic_4 * TILE_4_CHANCE);
    } else { // Game's Turn: Random tile spawn, no tile are open ~ SHOULD NOT HAPPEN
        int copy_board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION];
        memcpy(copy_board, board, sizeof(int) * MAX_NUM_TILES);
        return get_best_score(copy_board, current_depth - 1, false);
    }
}

/**
 * This returns the "best" direction to shift the tiles in the given board.
 * 
 * @param depth The search depth of the AI Expectiminimax solver/search.
 * @param heuristic_num The number indicating which heuristic to use when calculating the board's score.
 * @param flat_board The given 1x16 2048 board.
 * 
 * @return The best direction to move: 1: UP, 2: DOWN, 3: LEFT, 4: RIGHT
 */
int get_next_direction(int depth, int heuristic_num, int *flat_board) {
    HEURISTIC_NUM = heuristic_num;
    Direction best_direction = UP;
    uint64_t highest_heuristic = 0;

    /*uint64_t original_board = 0; // A 64-bit number to store all tiles of the board!
    for (int tile_index = 0; tile_index < MAX_NUM_TILES; tile_index++) {
        int tile = flat_board[tile_index];
        if (tile != BLANK_TILE) {
            uint64_t adjusted_tile = __builtin_ctz(tile); // Faster than log2(). Counts the # of trailing 0s. Ex: 8 = 0b1000 -> 3 = log2(8).
            if (adjusted_tile > 15) adjusted_tile = 15;
            uint64_t shifted_tile = adjusted_tile << (60 - 4 * tile_index);
            original_board |= shifted_tile;
        }
    }*/

    int original_board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION];
    for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
        for (int col = 0; col < MAX_BOARD_DIMENSION; col++) {
            original_board[row][col] = flat_board[row * MAX_BOARD_DIMENSION + col];
        }
    }
    for (int direction = UP; direction <= RIGHT; direction++) {
        int copy_board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION];
        memcpy(copy_board, original_board, sizeof(int) * MAX_NUM_TILES);
        bool board_changed = shift(copy_board, original_board, direction);
        if (board_changed) {
            uint64_t heuristic = get_best_score(copy_board, depth - 1, false);
            if (heuristic > highest_heuristic) {
                highest_heuristic = heuristic;
                best_direction = direction;
            }
        }
    }
    return best_direction + 1;
}

int main() {
    int board[16] = {0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    printf("test5\n");
    printf("%d", get_next_direction(DEPTH, HEURISTIC_NUM, board));
}
