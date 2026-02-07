from model import Model2048
from montecarlo import MonteCarlo2048
import ctypes as ct
import os
import time as t
import csv

try:
    expectiminimax_c = ct.CDLL(os.path.abspath("expectiminimax.dll")) # Shared library to connect Python and C
except FileNotFoundError:
    try:
        expectiminimax_c = ct.CDLL(os.path.abspath("code/expectiminimax.dll")) # Shared library to connect Python and C
    except FileNotFoundError as f:
        print(f"There was an error loading Expectiminimax: {f}\n")
except Exception as e:
    print(f"There was an error loading Expectiminimax: {e}\n")
expectiminimax_c.get_next_direction.argtypes = [ct.c_int, ct.c_int, ct.POINTER(ct.c_int)]
expectiminimax_c.get_next_direction.restype = ct.c_int
CBoardType = ct.c_int * 16

EMM_DEPTH_C = 8
EMM_DEPTH_PY = 5
HEURISTIC_NUM  = 3


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

    with open("data/mcts_test_1.txt", "w") as f:
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

    with open("data/emm_c_test.txt", "w") as f:
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

def testExpectiminimaxDepth():
    model = Model2048()
    emm_scores_all = []
    emm_highest_tiles_all = []
    emm_times_all = []

    for d in range(1, 8): # Depths 1-7
        emm_scores = []
        emm_highest_tiles = []
        emm_times = []
        for i in range(100):
            print(f"Depth: {d}, Expectiminimax: #{i+1}")
            start_time = t.perf_counter()
            while not model.gameOver():
                board = model.getBoard()
                board_flat = [tile for row in board for tile in row]
                board_flat_c = CBoardType(*board_flat)
                direction = expectiminimax_c.get_next_direction(d, HEURISTIC_NUM, board_flat_c)
                board_changed = model.shift(direction)
                if board_changed:
                    model.addTile()
                    model.updateGameOver()
            end_time = t.perf_counter()
            emm_scores.append(model.getScore())
            emm_highest_tiles.append(model.getHighestTile())
            emm_times.append(end_time - start_time)
            model.restart()
        emm_scores_all.append(emm_scores)
        emm_highest_tiles_all.append(emm_highest_tiles)
        emm_times_all.append(emm_times)

    emm_all_data = emm_scores_all + emm_highest_tiles_all + emm_times_all

    with open("data/emm_depth_test.csv", "w", newline="") as f:
        writer = csv.writer(f)
        emm_all_rows = zip(*emm_all_data)
        writer.writerow(["Depth",
            "1", "2", "3", "4", "5", "6", "7", "",
            "1", "2", "3", "4", "5", "6", "7", "",
            "1", "2", "3", "4", "5", "6", "7"
        ])
        for row in emm_all_rows:
            row_list = list(row)
            row_list.insert(0, "")
            row_list.insert(8, "")
            row_list.insert(16, "")
            writer.writerow(row_list)

def testExpectiminimaxDepth8():
    model = Model2048()
    emm_scores_all = []
    emm_highest_tiles_all = []
    emm_times_all = []

    for d in range(8, 9): # Depths 8
        emm_scores = []
        emm_highest_tiles = []
        emm_times = []
        for i in range(100):
            print(f"Depth: {d}, Expectiminimax: #{i+1}")
            start_time = t.perf_counter()
            while not model.gameOver():
                board = model.getBoard()
                board_flat = [tile for row in board for tile in row]
                board_flat_c = CBoardType(*board_flat)
                direction = expectiminimax_c.get_next_direction(d, HEURISTIC_NUM, board_flat_c)
                board_changed = model.shift(direction)
                if board_changed:
                    model.addTile()
                    model.updateGameOver()
            end_time = t.perf_counter()
            emm_scores.append(model.getScore())
            emm_highest_tiles.append(model.getHighestTile())
            emm_times.append(end_time - start_time)
            model.restart()
        emm_scores_all.append(emm_scores)
        emm_highest_tiles_all.append(emm_highest_tiles)
        emm_times_all.append(emm_times)

    emm_all_data = emm_scores_all + emm_highest_tiles_all + emm_times_all
    print(emm_all_data)
    emm_all_rows = list(zip(*emm_all_data))
    print(emm_all_data)
    rows = []

    with open("data/emm_depth_test.csv", "r", newline="") as f:
        reader = csv.reader(f)
        i = -1
        for row in reader:
            new_row = row
            if i == -1:
                new_row.insert(8, "8")
                new_row.insert(17, "8")
                new_row.insert(26, "8")
            else:
                new_row.insert(8, emm_all_rows[i][0])
                new_row.insert(17, emm_all_rows[i][1])
                new_row.insert(26, emm_all_rows[i][2])
            rows.append(new_row)       
            i += 1

    with open("data/emm_depth_test.csv", "w", newline="") as f:
        writer = csv.writer(f)
        for row in rows:
            print(row)
            writer.writerow(row)

def main():
    """
    This runs different test for the 2048 algorithms and places out in /data.
    """
    #testMonteCarlo()
    #testExpectiminimaxC()
    #testExpectiminimaxDepth()
    #testExpectiminimaxDepth8()

if __name__ == '__main__':
    main()
