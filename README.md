# gameoflife
Python library for generating Conway's Game of Life. 

Example usage
-----------------------------------------------
```py
game = GameOfLife(40, 40, [(12, 10), (11, 11), (12, 12), (11, 10), (13, 10)])

while game.num_live_cells() > 0:
    print_grid(game)
    sleep(0.3)
    game.tick()
```
