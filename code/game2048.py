from enum import Enum
import random as r

class Direction(Enum):
    """
    A class that sets the 4 cardinal directions of movements as integers.
    """
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Game2048:
    """
    This holds the functions to setup, run, and play the game 2048.
    """


    MAX_BOARD_DIMENSION = 4
    BLANK_TILE = 0
    TILE_2_CHANCE = 0.9
    TILE_4_CHANCE = 0.1

    def __init__(self):
        """
        This initializes the 2048 game with a zero scores and a board with two, random 2 or 4, tiles.
        """
        self.board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.score = 0
        self.game_over = False
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
                if self.board[y][x] == self.BLANK_TILE:
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
    
    def updateGameOver(self):
        """
        This checks if the game is over, i.e, no tiles can merge into each other.
        """
        for y in range(self.MAX_BOARD_DIMENSION):
            for x in range(self.MAX_BOARD_DIMENSION):
                if (self.board[y][x] == self.BLANK_TILE):
                    self.game_over = False
                    return

        for i in range(self.MAX_BOARD_DIMENSION):
            for j in range(self.MAX_BOARD_DIMENSION - 1):
                if (self.board[i][j] == self.board[i][j+1] or self.board[j][i] == self.board[j+1][i]):
                    self.game_over = False
                    return

        self.game_over = True







    def merge(self, list_values: list):
        """
        This merges and combines numbers from right to right for a single row/column.\n
        It start are the right and merges values in the right direction.\n
        Row - [Left, Right], Col - [Bottom, Top]

        Args:
            list_values (list): The row/column list of values to combine

        Returns:
            list: The updated row/column list of values after the shift/merge.
        """
        list_values = [v for v in list_values if v != 0]
        final_values = []
        i = len(list_values) - 1
        while i >= 0:
            if i - 1 >= 0 and list_values[i] == list_values[i - 1]:
                final_values.append(list_values[i] * 2)
                self.score += list_values[i] * 2
                i -= 2
            else:
                final_values.append(list_values[i])
                i -= 1

        while len(final_values) < 4:
            final_values.append(0)
        final_values.reverse()
        return final_values

    def shift(self, direction: int) -> bool:
        """
        This shifts the tiles on the board in one of the 4 cardinal directions.
        
        :param direction: The direction to shift the board tiles.
        :type direction: int
        :return: True if the tiles on the board have changed positions, False otherwise.
        :rtype: bool
        """
        if self.game_over: return False

        original_board = [row[:] for row in self.board]

        if direction == Direction.UP.value:
            for col in range(self.MAX_BOARD_DIMENSION):
                initial_values = [self.board[row][col] for row in range(self.MAX_BOARD_DIMENSION - 1, -1, -1)]
                final_values = self.merge(initial_values)
                for row in range(self.MAX_BOARD_DIMENSION):
                    self.board[row][col] = final_values[3 - row]
        elif direction == Direction.DOWN.value:
            for col in range(self.MAX_BOARD_DIMENSION):
                initial_values = [self.board[row][col] for row in range(self.MAX_BOARD_DIMENSION)]
                final_values = self.merge(initial_values)
                for row in range(self.MAX_BOARD_DIMENSION):
                    self.board[row][col] = final_values[row]
        elif direction == Direction.LEFT.value:
            for row in range(self.MAX_BOARD_DIMENSION):
                initial_values = [self.board[row][col] for col in range(self.MAX_BOARD_DIMENSION - 1, -1, -1)]
                final_values = self.merge(initial_values)
                for col in range(self.MAX_BOARD_DIMENSION):
                    self.board[row][col] = final_values[3 - col]
        elif direction == Direction.RIGHT.value:
            for row in range(self.MAX_BOARD_DIMENSION):
                initial_values = [self.board[row][col] for col in range(self.MAX_BOARD_DIMENSION)]
                final_values = self.merge(initial_values)
                for col in range(self.MAX_BOARD_DIMENSION):
                    self.board[row][col] = final_values[col]
        else:
            return False # Invalid direction

        return original_board != self.board

    def playAction(self, direction: int):
        """
        This shifts the tiles in one of the 4 cardinal directions. Then it adds a 2 or 4 tiles to the board if possible.
        
        :param direction: The direction to shift the board tiles.
        :type direction: int
        """
        if self.game_over: return
        board_changed = self.shift(direction)
        if board_changed:
            self.addTile()
            self.updateGameOver()

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

    def displayBoardScore(self):
        """
        This displays the current CLI board and score.
        """
        print("----------------------------------------")
        print(f"Score: {self.score}")
        for y in range(self.MAX_BOARD_DIMENSION):
            for x in range(self.MAX_BOARD_DIMENSION):
                print(f"{self.board[y][x]}  ", end='')
            print(" ")
        
    def playActionCLI(self, direction: int):
        """
        This shifts the tiles in one of the 4 cardinal directions. Then it adds a 2 or 4 tiles to the board if possible.\\
        Then it displays the current board.
        
        :param direction: The direction to shift the board tiles.
        :type direction: int
        """
        self.playAction(direction)
        self.displayBoardScore()

    def playCLI(self):
        """
        This runs 1 game using the current 2048 game board.
        
        :param self: Description
        """
        print("Welcome to 2048!")
        print("Here is your starting board")
        self.displayBoardScore()
        print("Use WASD to shift the tiles: 'W' is Up, 'A' is Left, 'S' is Down, & 'D' is Right. To quit, press 'X'.")

        while not self.game_over:
            direction = input("Direction: ").lower()
            match direction:
                case "w":
                    self.playActionCLI(Direction.UP.value)
                case "s":
                    self.playActionCLI(Direction.DOWN.value)
                case "a":
                    self.playActionCLI(Direction.LEFT.value)
                case "d":
                    self.playActionCLI(Direction.RIGHT.value)
                case "x":
                    print("You quit the game.")
                    return
                case _:
                    print("Invalid input try again.")

        print("----------------------------------------")
        print("GAME OVER!")
        print(f"Your score was {self.score}")
        print(f"Your highest tile was {self.getHighestTile()}")
        print("Thanks for playing.")

    def restart(self):
        """
        This restarts the 2048 game with a zero scores and a board with two, random 2 or 4, tiles.
        """
        self.board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
        self.score = 0
        self.game_over = False
        self.addTile()
        self.addTile()

def main():
    print("Welcome!")
    game = Game2048()
    while True:
        print("To play a game of 2048, press 'Y'. To end the program, press any other key.")
        action = input("Action: ").lower()
        match action:
            case "y":
                game.playCLI()
                game.restart()
            case _:
                print("Goodbye!")
                return

if __name__ == '__main__':
    main()
