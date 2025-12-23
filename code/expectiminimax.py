from model import Model2048, Direction

class Expectiminimax2048():
    """
    This class uses the Expectiminimax algorithm to determine the "best" next move in 2048.
    """

    MAX_BOARD_DIMENSION = 4
    BLANK_TILE = 0
    TILE_2_CHANCE = 0.9
    TILE_4_CHANCE = 0.1
    SNAKE_HEURISTIC = [
        [2**15, 2**14, 2**13, 2**12],
        [2**11, 2**10, 2**9, 2**8],
        [2**7, 2**6, 2**5, 2**4],
        [2**3, 2**2, 2**1, 2**0]
    ]

    def __init__(self, depth):
        self.depth = depth  # How deep are algorithm will search

    def getHeuristicScore(self, board: list) -> int:
        """
        This gets the board snake heuristic score.
        
        :param board: The given 4x4 2048 board.
        :type board: list
        :return: The heuristic score.
        :rtype: int
        """
        heuristic_score = 0
        for y in range(self.MAX_BOARD_DIMENSION):
            for x in range(self.MAX_BOARD_DIMENSION):
                heuristic_score += board[y][x] * self.SNAKE_HEURISTIC[y][x]
        return heuristic_score

    def getNextDirection(self, board: list) -> int:
        """
        Docstring for getNextDirection
        
        :param board: Description
        :type board: list
        :return: Description
        :rtype: int
        """
        return self.getBestBoard(board, self.depth)

    def getBestBoard(self, board: list, current_depth) -> int:
        """
        Docstring for getBestBoard
        
        :param board: Description
        :type board: list
        :param current_depth: Description
        :return: Description
        :rtype: int
        """
        if current_depth == 0:
            return self.getHeuristicScore(board)
        elif current_depth % 2 != 0: # Odd: Player move, tiles shift
            return 0
        else: # Even: Game move, random tile spawn
            return 0
