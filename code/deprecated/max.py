def printMaxBoardHeuristicScore():
    SNAKE_HEURISTIC_3 = [
        [2**12, 2**11, 2**10, 2**9],
        [2**6, 2**7, 2**8, 2**9],
        [2**6, 2**5, 2**4, 2**3],
        [2**0, 2**1, 2**2, 2**3]
    ]
    MAX = [
        [2**17, 2**16, 2**15, 2**14],
        [2**10, 2**11, 2**12, 2**13],
        [2**9, 2**8, 2**7, 2**6],
        [2**2, 2**3, 2**4, 2**5]
    ]
    total = 0
    for i in range(0, 4):
        for j in range(0, 4):
            total += SNAKE_HEURISTIC_3[i][j] * MAX[i][j]
    print(total)

if __name__ == '__main__':
    printMaxBoardHeuristicScore()
