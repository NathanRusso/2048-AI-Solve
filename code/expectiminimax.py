from model import Model2048, Direction
import math as m

class Expectiminimax2048():
    """
    This class uses the Expectiminimax algorithm to determine the "best" next move in 2048.
    """

    MAX_BOARD_DIMENSION = 4
    BLANK_TILE = 0
    TILE_2_CHANCE = 0.9
    TILE_4_CHANCE = 0.1
    SNAKE_HEURISTIC_1 = [
        [2**15, 2**14, 2**13, 2**12],
        [2**8, 2**9, 2**10, 2**11],
        [2**7, 2**6, 2**5, 2**4],
        [2**0, 2**1, 2**2, 2**3]
    ]
    SNAKE_HEURISTIC_2 = [
        [4**15, 4**14, 4**13, 4**12],
        [4**8, 4**9, 4**10, 4**11],
        [4**7, 4**6, 4**5, 4**4],
        [4**0, 4**1, 4**2, 4**3]
    ]
    SNAKE_HEURISTIC_3 = [
        [2**12, 2**11, 2**10, 2**9],
        [2**6, 2**7, 2**8, 2**9],
        [2**6, 2**5, 2**4, 2**3],
        [2**0, 2**1, 2**2, 2**3]
    ]
    SNAKE_HEURISTIC_4 = [
        [4**12, 4**11, 4**10, 4**9],
        [4**6, 4**7, 4**8, 4**9],
        [4**6, 4**5, 4**4, 4**3],
        [4**0, 4**1, 4**2, 4**3]
    ]

    def __init__(self, depth: int, snake: int):
        """
        This sets up the variables needed for Expectiminimax to function.
        
        :param depth: The search depth of the AI solver/search.
        :type depth: int
        :param snake: Which snake heuristic to use.
        :type snake: int
        
        """
        self.depth = depth # How deep are algorithm will search
        self.snake = snake # If the heuristic will be the snake 1

    def getHeuristicScore(self, board: list) -> int:
        """
        This gets the board's heuristic score.
        
        :param board: The given 4x4 2048 board.
        :type board: list
        :return: The heuristic score.
        :rtype: int
        """
        match self.snake:
            case 1:
                return self.__getHeuristicSnakeScore(board, self.SNAKE_HEURISTIC_1)
            case 2:
                return self.__getHeuristicSnakeScore(board, self.SNAKE_HEURISTIC_2)
            case 3:
                return self.__getHeuristicSnakeScore(board, self.SNAKE_HEURISTIC_3)
            case 4:
                return self.__getHeuristicSnakeScore(board, self.SNAKE_HEURISTIC_4)
            case _:
                return self.__getHeuristicSnakeScore(board, self.SNAKE_HEURISTIC_2)

    def __getHeuristicSnakeScore(self, board: list, snake_heuristic: list) -> int:
        """
        This gets the board snake heuristic score.
                
        :param b: The given 4x4 2048 board.
        :type b: list
        :param h: The snake heuristic to be used when getting the board's score.
        :type h: list
        :return: The heuristic score.
        :rtype: int
        """
        br0, br1, br2, br3 = board              # Board rows
        hr0, hr1, hr2, hr3 = snake_heuristic    # Snake heuristic rows
        return (
            br0[0]*hr0[0] + br0[1]*hr0[1] + br0[2]*hr0[2] + br0[3]*hr0[3] +
            br1[0]*hr1[0] + br1[1]*hr1[1] + br1[2]*hr1[2] + br1[3]*hr1[3] +
            br2[0]*hr2[0] + br2[1]*hr2[1] + br2[2]*hr2[2] + br2[3]*hr2[3] +
            br3[0]*hr3[0] + br3[1]*hr3[1] + br3[2]*hr3[2] + br3[3]*hr3[3]
        )

    def getNextDirection(self, board: list) -> int:
        """
        This returns the "best" direction to shift the tiles in the given board.
        
        :param board: The given 4x4 2048 board.
        :type board: list
        :return: The best direction to move: 1: UP, 2: DOWN, 3: LEFT, 4: RIGHT.
        :rtype: int
        """
        best_direction = Direction.UP
        highest_heuristic = 0
        for direction in Direction:
            copy_board = [row[:] for row in board]
            board_changed = self.__shift(copy_board, board, direction.value)
            if board_changed:
                heuristic = self.__getBestScore(copy_board, self.depth - 1, False)
                if heuristic > highest_heuristic:
                    highest_heuristic = heuristic
                    best_direction = direction
        return best_direction.value

    def __getBestScore(self, board: list, current_depth: int, players_turn: bool) -> int:
        """
        Returns the best heuristic score for the given board and depth.
        
        :param board: The current 4x4 2048 board.
        :type board: list
        :param current_depth: The current search depth.
        :type current_depth: int
        :param players_turn: If it is the player's turn, shifting tiles.
        :type players_turn: bool
        :return: The average/best heuristic score of the board overall.
        :rtype: int
        """
        if current_depth == 0: return self.getHeuristicScore(board)
 
        open_cells = self.__getAllOpenCells(board)
        num_open_cells = len(open_cells)
        if num_open_cells == 0 and not self.__potentialMerges(board):
            return self.getHeuristicScore(board) # Game over for the board

        if players_turn: # Player's Turn: Tiles shift
            highest_heuristic = 0
            for direction in Direction:
                copy_board = [row[:] for row in board]
                board_changed = self.__shift(copy_board, board, direction.value)
                if board_changed:
                    heuristic = self.__getBestScore(copy_board, current_depth - 1, False)
                    if heuristic > highest_heuristic: highest_heuristic = heuristic
            return highest_heuristic
        elif num_open_cells != 0: # Game's Turn: Random tile spawn, tiles are open
            sum_heuristic_2 = 0
            sum_heuristic_4 = 0
            for cell in open_cells:
                copy_board_2 = [row[:] for row in board]
                copy_board_4 = [row[:] for row in board]
                y, x = cell
                copy_board_2[y][x] = 2
                copy_board_4[y][x] = 4
                sum_heuristic_2 += self.__getBestScore(copy_board_2, current_depth - 1, True)
                sum_heuristic_4 += self.__getBestScore(copy_board_4, current_depth - 1, True)

            avg_heuristic_2 = sum_heuristic_2 / num_open_cells
            avg_heuristic_4 = sum_heuristic_4 / num_open_cells
            return m.floor(avg_heuristic_2 * self.TILE_2_CHANCE + avg_heuristic_4 * self.TILE_4_CHANCE)
        else: # Game's Turn: Random tile spawn, no tile are open ~ SHOULD NOT HAPPEN
            copy_board = [row[:] for row in board]
            return self.__getBestScore(board, current_depth - 1, True)

    def __getAllOpenCells(self, board: list) -> list:
        """
        This finds all cells that are empty in the given board.
        
        :param board: The given 4x4 2048 board.
        :type board: list
        :return: A list of all open cells.
        :rtype: list
        """
        open_cells = []
        for y in range(self.MAX_BOARD_DIMENSION):
            for x in range(self.MAX_BOARD_DIMENSION):
                if board[y][x] == self.BLANK_TILE:
                    open_cells.append((y, x))
        return open_cells

    def __potentialMerges(self, board: list) -> bool:
        """
        This checks if any cells can be merged together.

        :param board: The current 4x4 2048 board to check.
        :type board: list
        :return: True if the board can merge cells, False otherwise.
        :rtype: bool
        """
        for i in range(self.MAX_BOARD_DIMENSION):
            for j in range(self.MAX_BOARD_DIMENSION - 1):
                if board[i][j] == board[i][j+1] or board[j][i] == board[j+1][i]: return True
        return False

    def __gameOver(self, board: list) -> bool:
        """
        This gets if the game is over, i.e, no tiles can merge into each other.
        
        :param board: The current 4x4 2048 board to check.
        :type board: list
        :return: True if the board can't progress any more, False otherwise.
        :rtype: bool
        """
        for y in range(self.MAX_BOARD_DIMENSION):
            for x in range(self.MAX_BOARD_DIMENSION):
                if board[y][x] == self.BLANK_TILE: return False

        return not self.__potentialMerges(board)

    def __shift(self, board: list, original_board: list, direction: int) -> bool:
        """
        This shifts the tiles of the given board in one of the 4 cardinal directions.
        
        :param board: The given 4x4 2048 board to shift.
        :type board: list
        :param original_board: The original 4x4 2048 board before the shift.
        :type original_board: list
        :param direction: The direction to shift the board tiles.
        :type direction: int
        :return: True if the tiles on the board have changed positions, False otherwise.
        :rtype: bool
        """
        match direction:
            case Direction.UP.value:
                for col in range(self.MAX_BOARD_DIMENSION):
                    original_col_values = [row[col] for row in board][::-1] # Column in reverse order (going up)
                    final_col_values = self.__merge(original_col_values)[::-1]
                    for row in range(self.MAX_BOARD_DIMENSION):
                        board[row][col] = final_col_values[row]
            case Direction.DOWN.value:
                for col in range(self.MAX_BOARD_DIMENSION):
                    original_col_values = [row[col] for row in board] # Column in normal order (going down)
                    final_col_values = self.__merge(original_col_values)
                    for row in range(self.MAX_BOARD_DIMENSION):
                        board[row][col] = final_col_values[row]
            case Direction.LEFT.value:
                for row in range(self.MAX_BOARD_DIMENSION):
                    original_row_values = board[row][::-1] # Row in reverse order
                    final_row_values = self.__merge(original_row_values)[::-1]
                    board[row] = final_row_values
            case Direction.RIGHT.value:
                for row in range(self.MAX_BOARD_DIMENSION):
                    original_row_values = board[row] # Row in normal order
                    final_row_values = self.__merge(original_row_values)
                    board[row] = final_row_values
            case _:
                return False # Invalid direction

        return original_board != board

    def __merge(self, list_values: list) -> list:
        """
        This merges and combines numbers from right to right for a single row/column.\n
        It start are the right and merges values in the right direction.\n
        
        :param list_values: The row/column list of values to combine.
        :type list_values: list
        :return: The updated row/column list of values after the being merged.
        :rtype: list
        """
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

        while len(final_values) < self.MAX_BOARD_DIMENSION:
            final_values.append(0)
        return final_values[::-1]

def main():
    model = Model2048()
    expectiminimax = Expectiminimax2048(5, False) # Search depth of 5 is a good balance
    while not model.gameOver():
        direction = expectiminimax.getNextDirection(model.getBoard())
        board_changed = model.shift(direction)
        if board_changed:
            model.addTile()
            model.updateGameOver()
    model.displayBoardScore()

if __name__ == '__main__':
    main()
