# gameoflife
Python library for generating Conway's Game of Life. 

Example usage
-----------------------------------------------
```py
from gameoflife import GameOfLife
from time import sleep

def print_grid(game):
    grid = game.grid
    for r in range(game.rows):
        for c in range(game.cols):
            print(grid[r][c], end='')
        print()

game = GameOfLife(40, 40, [(12, 10), (11, 11), (12, 12), (11, 10), (13, 10)])

while game.num_live_cells() > 0:
    print_grid(game)
    sleep(0.3)
    game.tick()
```
