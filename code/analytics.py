from model import Model2048
from expectiminimax import Expectiminimax2048
from montecarlo import MonteCarlo2048
import ctypes
import os

EMM_DEPTH_C = 8
EMM_DEPTH_PY = 5
HEURISTIC_NUM  = 3

expectiminimax_c = ctypes.CDLL(os.path.abspath("code/expectiminimax.dll")) # Shared library to connect Python and C
expectiminimax_c.get_next_direction.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
expectiminimax_c.get_next_direction.restype = ctypes.c_int
CBoardType = ctypes.c_int * (16)


def testExpectiminimaxPy():
    model = Model2048()
    e_scores_all = []
    e_highest_tiles_all = []

    for i in range(1, 5):
        print(f"Expectiminimax Py: {i}")
        expectiminimax = Expectiminimax2048(EMM_DEPTH_PY, i)
        e_scores = []
        e_highest_tiles = []
        for j in range(20):
            print(j)
            while not model.gameOver():
                direction = expectiminimax.getNextDirection(model.getBoard())
                board_changed = model.shift(direction)
                if board_changed:
                    model.addTile()
                    model.updateGameOver()
            e_scores.append(model.getScore())
            e_highest_tiles.append(model.getHighestTile())
            model.restart()
        e_scores_all.append(e_scores)
        e_highest_tiles_all.append(e_highest_tiles)

    with open("data/output_1.txt", "w") as f:
        for i in range(1, 5): 
            f.write(f"E{i} Scores: {e_scores_all[i-1]}" + "\n")
        f.write("\n")

        for i in range(1, 5):
            f.write(f"E{i} Highest Tiles: {e_highest_tiles_all[i-1]}" + "\n")
        f.write("\n")

        for i in range(1, 5):
            f.write(f"E{i} Score Sum: {sum(e_scores_all[i-1])}, Avg: {sum(e_scores_all[i-1]) / 20}" + "\n")
        f.write("\n")

        for i in range(1, 5):
            f.write(f"E{i} Highest Tile Sum: {sum(e_highest_tiles_all[i-1])}, Avg: {sum(e_highest_tiles_all[i-1]) / 20}" + "\n")
        f.write("\n")

def testMonteCarlo():
    model = Model2048()
    m_scores_all = []
    m_highest_tiles_all = []

    c = 0.25
    for i in range(16):
        print(f"MCTS: {i+1}, C: {c}")
        montecarlo = MonteCarlo2048(1000, 5, c, None, HEURISTIC_NUM)
        m_scores = []
        m_highest_tiles = []
        for j in range(20):
            print(j)
            while not model.gameOver():
                direction = montecarlo.getNextDirection(model.getBoard())
                board_changed = model.shift(direction)
                if board_changed:
                    model.addTile()
                    model.updateGameOver()
            m_scores.append(model.getScore())
            m_highest_tiles.append(model.getHighestTile())
            model.restart()
        m_scores_all.append(m_scores)
        m_highest_tiles_all.append(m_highest_tiles)
        c += 0.25

    with open("data/output_2.txt", "w") as f:
        for i in range(1, 17):
            f.write(f"E{i} | C: {i/4} | Scores: {m_scores_all[i-1]}" + "\n")
        f.write("\n")

        for i in range(1, 17):
            f.write(f"E{i} | C: {i/4} | Highest Tiles: {m_highest_tiles_all[i-1]}" + "\n")
        f.write("\n")

        for i in range(1, 17):
            f.write(f"E{i} | C: {i/4} | Score Sum: {sum(m_scores_all[i-1])}, Avg: {sum(m_scores_all[i-1]) / 20}" + "\n")
        f.write("\n")

        for i in range(1, 17):
            f.write(f"E{i} | C: {i/4} | Highest Tile Sum: {sum(m_highest_tiles_all[i-1])}, Avg: {sum(m_highest_tiles_all[i-1]) / 20}" + "\n")
        f.write("\n")

def testExpectiminimaxC():
    model = Model2048()
    e_scores_all = []
    e_highest_tiles_all = []

    for i in range(1, 5):
        print(f"Expectiminimax C: {i}")
        e_scores = []
        e_highest_tiles = []
        for j in range(20):
            print(j)
            while not model.gameOver():
                board = model.getBoard()
                board_flat = [tile for row in board for tile in row]
                board_flat_c = CBoardType(*board_flat)
                direction = expectiminimax_c.get_next_direction(EMM_DEPTH_C, i, board_flat_c)
                board_changed = model.shift(direction)
                if board_changed:
                    model.addTile()
                    model.updateGameOver()
            e_scores.append(model.getScore())
            e_highest_tiles.append(model.getHighestTile())
            model.restart()
        e_scores_all.append(e_scores)
        e_highest_tiles_all.append(e_highest_tiles)

    with open("data/output_3.txt", "w") as f:
        for i in range(1, 5): 
            f.write(f"E{i} Scores: {e_scores_all[i-1]}" + "\n")
        f.write("\n")

        for i in range(1, 5):
            f.write(f"E{i} Highest Tiles: {e_highest_tiles_all[i-1]}" + "\n")
        f.write("\n")

        for i in range(1, 5):
            f.write(f"E{i} Score Sum: {sum(e_scores_all[i-1])}, Avg: {sum(e_scores_all[i-1]) / 20}" + "\n")
        f.write("\n")

        for i in range(1, 5):
            f.write(f"E{i} Highest Tile Sum: {sum(e_highest_tiles_all[i-1])}, Avg: {sum(e_highest_tiles_all[i-1]) / 20}" + "\n")

def main():
    """
    This runs different test for the 2048 algorithms and places out in /data.
    """
    #testExpectiminimaxPy()
    #testMonteCarlo()
    testExpectiminimaxC()

if __name__ == '__main__':
    main()
