from model import Model2048, Direction
import math as m

class MonteCarlo2048:
    """
    This classes uses the Monte Carlo Tree Search algorithm to determine the "best" next move in 2048.
    """

    def __init__(self):
        pass

    def UCB1(self, average_reward: float, parent_visits: int, node_visits: int) -> float:
        """
        Docstring for UCB1 Upper Confidence Bound 1 for Trees
        
        :param average_reward: Description
        :type average_reward: float
        :param parent_visits: Description
        :type parent_visits: int
        :param node_visits: Description
        :type node_visits: int
        :return: Description
        :rtype: float
        """
        return average_reward + m.sqrt( 2 * m.log(parent_visits) / node_visits )

    def getNextDirection(self, board: list) -> int:
        """
        This returns the "best" direction to shift the tiles in the given board.
        
        :param board: The given 4x4 2048 board.
        :type board: list
        :return: The best direction to move: 1: UP, 2: DOWN, 3: LEFT, 4: RIGHT.
        :rtype: int
        """

        """best_direction = Direction.UP
        highest_heuristic = 0
        original_board = [row[:] for row in board]
        for direction in Direction:
            board_copy = [row[:] for row in board]
            board_changed = self.__shift(board_copy, original_board, direction.value)
            if board_changed:
                heuristic = self.__getBestScore(board_copy, self.depth - 1, False)
                if heuristic > highest_heuristic:
                    highest_heuristic = heuristic
                    best_direction = direction
        return best_direction.value"""
        pass

        def selection(self):
            pass

        def expansion(self):
            pass
        
        def simulation(self):
            pass

        def backPropagation(self):
            pass
