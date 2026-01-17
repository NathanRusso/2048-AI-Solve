/**
 * expectiminimax.c - A C, as opposed to Python, version of expectiminimax
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

#include "expectiminimax.h"

#define MAX_NUM_TILES 16
#define MAX_BOARD_DIMENSION 4
#define BLANK_TILE 0
#define TILE_2_CHANCE 0.9
#define TILE_4_CHANCE 0.1

typedef enum {
    UP, // 0 -> 1
    DOWN, // 1 -> 2
    LEFT, // 2 -> 3
    RIGHT // 3 -> 4
} Direction;

const int SNAKE_HEURISTIC_3[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION] = {
    {4096, 2048, 1024, 512},
    {64, 128, 256, 512},
    {64, 32, 16, 8},
    {1, 2, 4, 8}
};

int DEPTH = 5; // The defalt depth for Expectiminimax

/**
 * This gets the board heuristic score.
 * 
 * @param board The given 4x4 2048 board.
 * 
 * @return The board's snake heuristic score.
 */
long long get_heuristic_score(int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION]) {
    long long board_heuristic = 0;
    for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
        for (int col = 0; col < MAX_BOARD_DIMENSION; col++) {
            board_heuristic += board[row][col] * SNAKE_HEURISTIC_3[row][col];
        }
    }
    return board_heuristic;
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
int *merge(int list[4]) {
/*
    list_values = [tile for tile in list_values if tile != self.BLANK_TILE]
    final_values = []
    i = len(list_values) - 1
    while i >= 0:
        if i - 1 >= 0 and list_values[i] == list_values[i-1]:
            new_tile = list_values[i] * 2
            final_values.append(new_tile)
            i -= 2
        else:
            final_values.append(list_values[i])
            i -= 1

    while len(final_values) < MAX_BOARD_DIMENSION:
        final_values.append(0)
    return final_values[::-1]
*/
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
                //original_col_values = [row[col] for row in board][::-1] # Column in reverse order (going up)
                //final_col_values = self.__merge(original_col_values)[::-1]
                //for row in range(MAX_BOARD_DIMENSION):
                    //board[row][col] = final_col_values[row]
                for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
                    //board[row][col] = final_col_values[row]
                }
            }
            return true;
            break;
        case DOWN:
            for (int col = 0; col < MAX_BOARD_DIMENSION; col++) {
                //original_col_values = [row[col] for row in board] # Column in normal order (going down)
                //final_col_values = self.__merge(original_col_values)
                //for row in range(MAX_BOARD_DIMENSION):
                    //board[row][col] = final_col_values[row]   
                for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
                    //board[row][col] = final_col_values[row]
                }
            }
            return true;
            break;
        case LEFT:
            for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
                //original_row_values = board[row][::-1] # Row in reverse order
                //final_row_values = self.__merge(original_row_values)[::-1]
                //board[row] = final_row_values
            }
            return true;
            break;
        case RIGHT:
            for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
                //original_row_values = board[row] # Row in normal order
                //final_row_values = self.__merge(original_row_values)
                //board[row] = final_row_values
            }
            return true;
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
 * @param num_open_cells A pointer to a variable holding the number of open cells.
 * 
 * @return A list of all open cells.
 */
int **get_open_cells(int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION], int *num_open_cells) {
    int **open_cells = (int **) malloc(sizeof(int*) * MAX_NUM_TILES);
    assert(open_cells);
    *num_open_cells = 0;
    for (int row = 0; row < MAX_BOARD_DIMENSION; row++) {
        for (int col = 0; col < MAX_BOARD_DIMENSION; col++) {
            if (board[row][col] == BLANK_TILE) {
                open_cells[*num_open_cells] = (int *) malloc(sizeof(int) * 2);
                assert(open_cells[*num_open_cells]);
                open_cells[*num_open_cells][0] = row;
                open_cells[*num_open_cells][1] = col;
                *num_open_cells++;
            }
        }
    }
    return open_cells;
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
long long get_best_score(int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION], int current_depth, bool players_turn) {
    if (current_depth == 0) return get_heuristic_score(board);
    int num_open_cells = 0;
    int **open_cells = get_open_cells(board, &num_open_cells);
    if (num_open_cells == 0 && !potential_merges(board)) return get_heuristic_score(board);

    long long final_heuristic = 0;
    if (players_turn) { // Player's Turn: Tiles shift
        int original_board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION];
        memcpy(board, original_board, sizeof(board));
        for (int direction = UP; direction <= RIGHT; direction++) {
            int copy_board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION];
            memcpy(original_board, copy_board, sizeof(original_board));
            bool board_changed = shift(copy_board, original_board, direction);
            if (board_changed) {
                long long heuristic = get_best_score(copy_board, current_depth - 1, false);
                if (heuristic > final_heuristic) final_heuristic = heuristic;
            }
        }
    } else if (num_open_cells != 0) { // Game's Turn: Random tile spawn, tiles are open
        long long avg_heuristic_2 = 0;
        long long avg_heuristic_4 = 0;
        for (int i = 0; i < num_open_cells; i++) {
            int copy_board_2[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION];
            int copy_board_4[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION];
            memcpy(board, copy_board_2, sizeof(board));
            memcpy(board, copy_board_4, sizeof(board));
            int row = open_cells[i][0];
            int col = open_cells[i][1];
            copy_board_2[row][col] = 2;
            copy_board_4[row][col] = 4;
            avg_heuristic_2 += get_best_score(copy_board_2, current_depth - 1, true) / num_open_cells;
            avg_heuristic_4 += get_best_score(copy_board_4, current_depth - 1, true) / num_open_cells;
        }
        final_heuristic = floor(avg_heuristic_2 * TILE_2_CHANCE + avg_heuristic_4 * TILE_4_CHANCE);
    } else { // Game's Turn: Random tile spawn, no tile are open
        int copy_board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION];
        memcpy(board, copy_board, sizeof(board));
        final_heuristic = get_best_score(copy_board, current_depth - 1, false);
    }

    for (int i = 0; i < num_open_cells; i++) free(open_cells[i]);
    free(open_cells);
    return final_heuristic;
}

/**
 * This returns the "best" direction to shift the tiles in the given board.
 * 
 * @param depth The search depth of the AI Expectiminimax solver/search.
 * @param board The given 4x4 2048 board.
 * 
 * @return The best direction to move: 1: UP, 2: DOWN, 3: LEFT, 4: RIGHT
 */
int get_next_direction(int depth, int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION]) {
    DEPTH = depth;
    Direction best_direction = UP;
    long long highest_heuristic = 0;
    int original_board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION];
    memcpy(board, original_board, sizeof(board));
    for (int direction = UP; direction <= RIGHT; direction++) {
        int copy_board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION];
        memcpy(board, original_board, sizeof(board));
        bool board_changed = shift(copy_board, original_board, direction);
        if (board_changed) {
            long long heuristic = get_best_score(copy_board, DEPTH - 1, false);
            if (heuristic > highest_heuristic) {
                highest_heuristic = heuristic;
                best_direction = direction;
            }
        }
    }
    return best_direction + 1;
}
