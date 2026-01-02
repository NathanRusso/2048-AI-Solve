from model import Direction
import math as m
import random as r

class MCTSNode:
    """
    This class represents the games nodes used by MonteCarlo2048 to simulate a state of 2048.
    """

    MAX_BOARD_DIMENSION = 4
    BLANK_TILE = 0
    TILE_2_CHANCE = 0.9
    TILE_4_CHANCE = 0.1
    SNAKE_HEURISTIC_2 = [
        [4**15, 4**14, 4**13, 4**12],
        [4**8, 4**9, 4**10, 4**11],
        [4**7, 4**6, 4**5, 4**4],
        [4**0, 4**1, 4**2, 4**3]
    ]

    def __init__(self, board: list, parent: "MCTSNode", direction: int, players_turn: bool):
        """
        This creates the MCTS 2048 Node with all of the relevant information. 
        All and available action are set and the state is checked if the game is over.  
        
        :param board: The given current 4x4 2048 board.
        :type board: list
        :param parent: The parent node of the current MCTS2048Node.
        :type parent: "MCTSNode"
        :param direction: The shift direction made to reach this state: 1: UP, 2: DOWN, 3: LEFT, 4: RIGHT, None: Random tile.
        :type direction: int
        :param players_turn: This dictates if it is the player turn to shift tiles in the current node state.
        :type players_turn: bool
        """
        self.board = board
        self.parent = parent
        self.direction = direction
        self.players_turn = players_turn
        self.children = []
        self.all_actions = []
        self.available_actions = []
        self.game_over = True
        self.visits = 0
        self.reward = 0.0

        open_cells = []
        for y in range(self.MAX_BOARD_DIMENSION):
            for x in range(self.MAX_BOARD_DIMENSION):
                if board[y][x] == self.BLANK_TILE: open_cells.append((y, x))

        if len(open_cells) > 0:
            self.game_over = False
            if players_turn:
                for direction in Direction:
                    board_copy = [row[:] for row in board]
                    board_changed = self.__shift(board_copy, board, direction.value)
                    if board_changed: self.all_actions.append(direction.value)
                """
                br0, br1, br2, br3 = board # Board rows
                if self.BLANK_TILE in (br1[1], br1[2], br2[1], br2[2]):
                    self.all_actions = [Direction.DOWN.value, Direction.RIGHT.value, Direction.LEFT.value, Direction.UP.value]
                else:
                    if br0[0] == self.BLANK_TILE:
                        self.all_actions.append(Direction.UP.value)
                        self.all_actions.append(Direction.LEFT.value)
                    if br0[3] == self.BLANK_TILE:
                        self.all_actions.append(Direction.UP.value)
                        self.all_actions.append(Direction.RIGHT.value)
                    if br3[0] == self.BLANK_TILE:
                        self.all_actions.append(Direction.DOWN.value)
                        self.all_actions.append(Direction.LEFT.value)
                    if br3[0] == self.BLANK_TILE:
                        self.all_actions.append(Direction.DOWN.value)
                        self.all_actions.append(Direction.RIGHT.value)

                self.all_actions = list(set(self.all_actions))
                """
            else:
                self.all_actions = open_cells
        elif players_turn:
            check1 = False
            check2 = False
            for i in range(self.MAX_BOARD_DIMENSION):
                for j in range(self.MAX_BOARD_DIMENSION - 1):
                    if board[i][j] == board[i][j+1] and not check1:
                        self.all_actions.append(Direction.RIGHT.value)
                        self.all_actions.append(Direction.LEFT.value)
                        self.game_over = False
                        check1 = True
                    
                    if board[j][i] == board[j+1][i] and not check2:
                        self.all_actions.append(Direction.DOWN.value)
                        self.all_actions.append(Direction.UP.value)
                        self.game_over = False
                        check2 = True

        self.available_actions = self.all_actions

    def selectBestChild(self) -> "MCTSNode":
        """
        Given the current node, the child with the best UCB1 score is returned.
        
        :return: The node child with the best UCB1 score.
        :rtype: MCTSNode
        """
        best_child = None
        best_child_ucb1 = float("-inf")
        for child in self.children:
            child_ucb1 = self.__UCB1(child.reward, self.visits, child.visits)
            if child_ucb1 > best_child_ucb1:
                best_child_ucb1 = child_ucb1
                best_child = child
        return best_child

    def expandNode(self) -> "MCTSNode":
        """
        Given the current node, this adds/creates a new child for it.
        
        :return: A new child node for the given parent node based on the parent's available moves.
        :rtype: MCTSNode
        """
        action = self.available_actions.pop()
        board_copy = [row[:] for row in self.board]
        child = None
        if self.players_turn:
            board_changed = self.__shift(board_copy, self.board, action)
            child = MCTSNode(board_copy, self, action, not self.players_turn)
        else:
            y, x  = action
            tile_probability_num = r.random()
            if tile_probability_num < self.TILE_2_CHANCE:
                board_copy[y][x] = 2
            else:
                board_copy[y][x] = 4
            child = MCTSNode(board_copy, self, None, not self.players_turn)
        self.children.append(child)
        return child

    def simulateNode(self, expansion_depth: int) -> int:
        """
        Given the current node, this simulates a game with a max number of turns and return the final board score.
        
        :param expansion_depth: How many turns to simulate in the 2048 game.
        :type expansion_depth: int
        :return: The heuristic score of the final board.
        :rtype: int
        """
        simulation_board = [row[:] for row in self.board]
        game_over = False
        i = 0
        players_turn = self.players_turn
        while i < expansion_depth and not game_over:
            if players_turn:
                directions = [Direction.DOWN.value, Direction.RIGHT.value, Direction.LEFT.value, Direction.UP.value]
                board_changed = False
                while not board_changed and not game_over:
                    if len(directions) == 0:
                        game_over = True
                        continue
                    direction = directions.pop(r.randrange(len(directions)))
                    board_changed = self.__shift(simulation_board, simulation_board, direction)
            else:
                open_cells = []
                for y in range(self.MAX_BOARD_DIMENSION):
                    for x in range(self.MAX_BOARD_DIMENSION):
                        if simulation_board[y][x] == self.BLANK_TILE: open_cells.append((y, x))

                if len(open_cells) > 0:
                    y, x  = r.choice(open_cells)
                    tile_probability_num = r.random()
                    if tile_probability_num < self.TILE_2_CHANCE:
                        simulation_board[y][x] = 2
                    else:
                        simulation_board[y][x] = 4
            players_turn = not players_turn
            i += 1

        return self.getHeuristicSnake2Score(simulation_board)

    def backPropagation(self, reward: int):
        """
        Given the current node, this update the score and visits of itself, its parent, its parent's parent, and so on.
        
        :param reward: The heuristic score to add the a nodes reward.
        :type reward: int
        """
        node = self
        while node:
            node.visits += 1
            node.reward += reward
            node = node.parent
    
    def __UCB1(self, reward: float, parent_visits: int, node_visits: int) -> float:
        """
        Given a current node, this returns its Upper Confidence Bound 1 score for trees.
        For the exploit, since the heuristic scores go from 0 to infinity, a simple average of reward / visits cannot be used.  
        An alternative is adjusting the score using functions to be the score between 0 and 1. 
        
        :param reward: The current total heurisitic score of the node state.
        :type reward: float
        :param parent_visits: Then number of times the node's parent has been visited.
        :type parent_visits: int
        :param node_visits: The number of times the node has been visited
        :type node_visits: int
        :return: The UCB1 score of the node.
        :rtype: float
        """
        C = 4                                 # The exploration constant used to adjust weighting
        adjusted_score = m.log(reward)          # The logarithmic heavily reduces large number down
        exploit = m.tanh(adjusted_score / 50)   # The tanh function bounds the exploit to [0, 1]
        explore = C * m.sqrt( m.log(parent_visits) / node_visits )
        return exploit + explore                # UCB1 typical

    def getHeuristicSnake2Score(self, board: list) -> int:
        """
        Given the current node, this gets its board snake heuristic score.
                
        :param b: The given 4x4 2048 board.
        :type b: list
        :return: The heuristic score.
        :rtype: int
        """
        br0, br1, br2, br3 = board                      # Board rows
        hr0, hr1, hr2, hr3 = self.SNAKE_HEURISTIC_2     # Snake heuristic rows
        return (
            br0[0]*hr0[0] + br0[1]*hr0[1] + br0[2]*hr0[2] + br0[3]*hr0[3] +
            br1[0]*hr1[0] + br1[1]*hr1[1] + br1[2]*hr1[2] + br1[3]*hr1[3] +
            br2[0]*hr2[0] + br2[1]*hr2[1] + br2[2]*hr2[2] + br2[3]*hr2[3] +
            br3[0]*hr3[0] + br3[1]*hr3[1] + br3[2]*hr3[2] + br3[3]*hr3[3]
        )

    def __shift(self, board: list, original_board: list, direction: int) -> list:
        """
        This shifts the tiles of the given board in one of the 4 cardinal directions.
        
        :param board: The given 4x4 2048 board to shift.
        :type board: list
        :param original_board: The original 4x4 2048 board before the shift.
        :type original_board: list
        :param direction: The direction to shift the board tiles. 
        :type direction: int
        :return: True if the tiles on the board have changed positions, False otherwise.
        :rtype: list
        """
        if direction == Direction.UP.value:
            for col in range(self.MAX_BOARD_DIMENSION):
                original_col_values = [row[col] for row in board][::-1] # Column in reverse order (going up)
                final_col_values = self.__merge(original_col_values)[::-1]
                for row in range(self.MAX_BOARD_DIMENSION):
                    board[row][col] = final_col_values[row]
        elif direction == Direction.DOWN.value:
            for col in range(self.MAX_BOARD_DIMENSION):
                original_col_values = [row[col] for row in board] # Column in normal order (going down)
                final_col_values = self.__merge(original_col_values)
                for row in range(self.MAX_BOARD_DIMENSION):
                    board[row][col] = final_col_values[row]
        elif direction == Direction.LEFT.value:
            for row in range(self.MAX_BOARD_DIMENSION):
                original_row_values = board[row][::-1] # Row in reverse order
                final_row_values = self.__merge(original_row_values)[::-1]
                board[row] = final_row_values
        elif direction == Direction.RIGHT.value:
            for row in range(self.MAX_BOARD_DIMENSION):
                original_row_values = board[row] # Row in normal order
                final_row_values = self.__merge(original_row_values)
                board[row] = final_row_values
        else:
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
                

class MonteCarlo2048:
    """
    This classes uses the Monte Carlo Tree Search algorithm to determine the "best" next move in 2048.
    """

    def __init__(self, selection_iterations: int, expansion_depth: int):
        """
        This sets up the variables needed for MCTS to function.
        
        :param selection_iterations: The number of iterations/times a new node will be run on.
        :type selection_iterations: int
        :param expansion_depth: The max number of moves simulated on a node.
        :type expansion_depth: int
        """
        self.selection_iterations = selection_iterations
        self.expansion_depth = expansion_depth

    def getNextDirection(self, original_board: list) -> int:
        """
        Docstring for getNextDirection
        
        :param original_board: Description
        :type original_board: list
        :return: Description
        :rtype: int
        """
        root = MCTSNode(original_board, None, None, True)
        original_heuristic = root.getHeuristicSnake2Score(original_board)
        
        for i in range(self.selection_iterations):
            node = root

            while not node.game_over and len(node.available_actions) == 0:
                node = node.selectBestChild()                       # Selection

            if not node.game_over and len(node.available_actions) > 0:
                node = node.expandNode()                            # Expansion

            heuristic = node.simulateNode(self.expansion_depth)     # Simulation

            node.backPropagation(heuristic)                    # Backpropagation

        best_direction = None
        best_visits = 0
        for child in root.children:
            print(child.reward)
            if best_direction is None:
                best_direction = child.direction
                best_visits = child.visits
            elif child.visits > best_visits:
                best_visits = child.visits
                best_direction = child.direction
        print(best_direction)
        return best_direction
