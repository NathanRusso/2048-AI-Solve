"""
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

    with open("data/emm_py_test.txt", "w") as f:
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
"""
