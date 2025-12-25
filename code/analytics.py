from model import Model2048, Direction
from expectiminimax import Expectiminimax2048

def main():
    model = Model2048()
    expectiminimax1 = Expectiminimax2048(5, 1) # Search depth of 5 is a good balance
    expectiminimax2 = Expectiminimax2048(5, 2) # Search depth of 5 is a good balance

    e1_scores = []
    e2_scores = []
    e1_highest_tiles = []
    e2_highest_tiles = []

    for i in range(20):
        print(i)
        while not model.gameOver():
            direction = expectiminimax1.getNextDirection(model.getBoard())
            board_changed = model.shift(direction)
            if board_changed:
                model.addTile()
                model.updateGameOver()
        e1_scores.append(model.getScore())
        e1_highest_tiles.append(model.getHighestTile())
        model.restart()
    
    for i in range(20):
        print(i)
        while not model.gameOver():
            direction = expectiminimax2.getNextDirection(model.getBoard())
            board_changed = model.shift(direction)
            if board_changed:
                model.addTile()
                model.updateGameOver()
        e2_scores.append(model.getScore())
        e2_highest_tiles.append(model.getHighestTile())
        model.restart()
    
    e1_scores_sum = sum(e1_scores)
    e2_scores_sum = sum(e2_scores)
    e1_highest_tiles_sum = sum(e1_highest_tiles)
    e2_highest_tiles_sum = sum(e2_highest_tiles)
    e1_scores_avg = e1_scores_sum / 20
    e2_scores_avg = e2_scores_sum / 20
    e1_highest_tiles_avg = e1_highest_tiles_sum / 20
    e2_highest_tiles_avg = e2_highest_tiles_sum / 20

    print(f"E1 Scores: {e1_scores}")
    print(f"E2 Scores: {e2_scores}")
    print(f"E1 Highest Tiles: {e1_highest_tiles}")
    print(f"E2 Highest Tiles: {e2_highest_tiles}")
    print(f"E1 Score Sum: {e1_scores_sum}, Avg: {e1_scores_avg}")
    print(f"E2 Score Sum: {e2_scores_sum}, Avg: {e2_scores_avg}")
    print(f"E1 Highest Tile Sum: {e1_highest_tiles_sum}, Avg: {e1_highest_tiles_avg}")
    print(f"E2 Highest Tile Sum: {e2_highest_tiles_sum}, Avg: {e2_highest_tiles_avg}")

    with open("output.txt", "w") as f:
        f.write(f"E1 Scores: {e1_scores}" + "\\n")
        f.write(f"E2 Scores: {e2_scores}" + "\\n")
        f.write(f"E1 Highest Tiles: {e1_highest_tiles}" + "\\n")
        f.write(f"E2 Highest Tiles: {e2_highest_tiles}" + "\\n")
        f.write(f"E1 Score Sum: {e1_scores_sum}, Avg: {e1_scores_avg}" + "\\n")
        f.write(f"E2 Score Sum: {e2_scores_sum}, Avg: {e2_scores_avg}" + "\\n")
        f.write(f"E1 Highest Tile Sum: {e1_highest_tiles_sum}, Avg: {e1_highest_tiles_avg}" + "\\n")
        f.write(f"E2 Highest Tile Sum: {e2_highest_tiles_sum}, Avg: {e2_highest_tiles_avg}" + "\\n")

if __name__ == '__main__':
    main()
