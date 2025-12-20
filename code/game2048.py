import random as r

class Game2048:
    """
    This holds the functions to setup, run, and play the game 2048.
    """

    MAX_BOARD_DIMENSION = 4
    TILE_2_CHANCE = 0.9
    TILE_4_CHANCE = 0.1

    def __init__(self):
        """
        This initializes the 2048 game with an zero scores and a board with two, random 2 or 4, tiles.
        """
        self.board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.score = 0
        self.game_over = 0
        self.addTile()
        self.addTile()

    def getAllOpenCells(self) -> list:
        """
        This finds all cells that are empty. They all have a value of 0.
        
        :return: A list of all open cells.
        :rtype: list
        """
        open_cells = []
        for y in range(self.MAX_BOARD_DIMENSION):
            for x in range(self.MAX_BOARD_DIMENSION):
                if self.board[y][x] == 0:
                    open_cells.append((y, x))
        return open_cells

    def addTile(self) -> bool:
        """
        This adds a new 2 or 4 tile in on of the open cells on the board.
        
        :return: True if a new cell was added, False otherwise.
        :rtype: bool
        """
        open_cells = self.getAllOpenCells()
        if open_cells:
            y, x = r.choice(open_cells)
            tile_probability_num = r.random()
            if tile_probability_num < self.TILE_2_CHANCE:
                self.board[y][x] = 2
            else:
                self.board[y][x] = 4
            return True
        return False
    
    def getBoard(self) -> list:
        """
        This gets the current 2048 game board.
        
        :return: The 4x4 game board.
        :rtype: list
        """
        return self.board

    def getScore(self) -> int:
        """
        This gets the current 2048 game score.
        
        :return: The total game score.
        :rtype: int
        """
        return self.score

    def gameOver(self) -> bool:
        """
        This gets whether the current 2048 game is over.
        
        :return: True if the game is over, False otherwise.
        :rtype: bool
        """
        return self.game_over
    
    def getHighestTile(self) -> int:
        """
        This gets the highest tile on the current 2048 game board.
        
        :return: The highest tile.
        :rtype: int
        """
        highest_tile = 2
        for y in range(self.MAX_BOARD_DIMENSION):
            for x in range(self.MAX_BOARD_DIMENSION):
                tile = self.board[y][x]
                if tile > highest_tile:
                    highest_tile = tile
        return highest_tile
