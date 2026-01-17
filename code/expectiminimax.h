#ifndef _EXPECTIMINIMAX_
#define _EXPECTIMINIMAX_

#define MAX_NUM_TILES 16
#define MAX_BOARD_DIMENSION 4
#define BLANK_TILE 0
#define TILE_2_CHANCE 0.9
#define TILE_4_CHANCE 0.1

long long get_heuristic_score(int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION]);

int *merge(int original_list[MAX_BOARD_DIMENSION], int new_list[MAX_BOARD_DIMENSION]);

bool shift(int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION], int original_board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION], int direction);

bool potential_merges(int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION]);

int **get_open_cells(int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION], int *num_open_cells);

long long get_best_score(int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION], int current_depth, bool players_turn);

int get_next_direction(int depth, int board[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION]) {

#endif
