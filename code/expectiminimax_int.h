#ifndef _EXPECTIMINIMAX_
#define _EXPECTIMINIMAX_

#include <stdint.h>

#define MAX_NUM_TILES 16
#define MAX_BOARD_DIMENSION 4
#define BLANK_TILE 0
#define TILE_2_CHANCE 0.9
#define TILE_4_CHANCE 0.1

uint64_t get_heuristic_snake_score(const uint64_t board, const int snake_heuristic[MAX_BOARD_DIMENSION][MAX_BOARD_DIMENSION]);

uint64_t get_heuristic_score(const uint64_t board);

void merge(int original_list[MAX_BOARD_DIMENSION], int new_list[MAX_BOARD_DIMENSION]);

bool shift(uint64_t board, uint64_t original_board, int direction);

bool potential_merges(uint64_t board);

int **get_open_cells(uint64_t board, int open_cells[MAX_BOARD_DIMENSION][2], int *num_open_cells);

uint64_t get_best_score(uint64_t board, int current_depth, bool players_turn);

int get_next_direction(int depth, int heuristic_num, int *flat_board);

#endif
