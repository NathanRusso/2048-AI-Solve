# 2048-AI-Solve
This project is a recreation of the game 2048 with additional functionality to be solved using AI search algorithms.

## About the Application

### What is 2048
...

### How Is AI Used to Solve 2048
...

## Preparing and Using the the Application

### 2048 Game Requirements
1. Python 3+ (64-bit recommended)
    * To check your Python version, run `python --version` or `python3 --version`.
    * To check your Python architecture, run `python -c "import platform; print(platform.architecture())"`.
    * Downloads can be found at https://www.python.org/downloads/.
2. PyGame
    * To install PyGame into your system's Python, run `pip install pygame`.
3. MinGW
    * If you opted for a 64-bit version of Python, you must have a 64-bit version of MinGW installed.
        * Downloads can be found at https://www.mingw-w64.org/downloads/.
    * If you opted for a 32-bit version of Python, you must have a 32-bit version of MinGW installed, but this has not been tested.
        * Downloads can be found at https://www.winlibs.com/.
4. You must be in either the top level or /code directory.

### How To Run (Options)
1. If you are in the top directory, run `python code/ui.py` or `python3 code/ui.py`.
2. If you are in the /code directory, run `python ui.py` or `python3 ui.py`.
3. If you are using an IDE that handles Python, click the play button to run the ui.py file.

## Resources
### Expectiminimax
- https://www.geeksforgeeks.org/dsa/expectimax-algorithm-in-game-theory/
- https://www.geeksforgeeks.org/artificial-intelligence/expectimax-search-algorithm-in-ai/
- https://youtu.be/0fOLkZJ-Q6I?si=IS6iU51pobOUEFQW
- https://github.com/mschrandt/2048
- https://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf
- https://www.baeldung.com/cs/2048-algorithm
- https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048
- https://github.com/nneonneo/2048-ai

### Monte Carlo Tree Search
- https://www.geeksforgeeks.org/machine-learning/monte-carlo-tree-search-mcts-in-machine-learning/
- https://www.geeksforgeeks.org/machine-learning/upper-confidence-bound-algorithm-in-reinforcement-learning/
- https://github.com/poomstas/2048_MCTS

### Both
- https://www.researchgate.net/publication/327912401_Comparison_of_Expectimax_and_Monte_Carlo_algorithms_in_Solving_the_online_2048_game/fulltext/5bacdd4092851ca9ed2a29ce/Comparison-of-Expectimax-and-Monte-Carlo-algorithms-in-Solving-the-online-2048-game.pdf?__cf_chl_tk=f1HpxtWwhXsYdST7Gesk_kO1wUsKYZGxYo3_KazfrT4-1767725944-1.0.1.1-ajWTr_ys5XUhCiI32mzLZx7HUzXJ4IavJg3qRU8u0kI

### Other (Not yet implemented or taken inspiration from)
- https://event.cwi.nl/uai2010/papers/UAI2010_0219.pdf
- https://www.cs.unh.edu/~sjw1000/2024-socs-extreme_value_mcts-ea.pdf   # References 3?
- https://arxiv.org/html/2405.18248v1#S3                                # References 2?
- https://arxiv.org/html/2512.09727v1
