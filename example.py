#!/usr/bin/python

from gameoflife import GameOfLife
from time import sleep

def print_grid(game):
    grid = game.grid
    for r in range(game.rows):
        for c in range(game.cols):
            print(grid[r][c], end='')
        print()

if __name__ == '__main__':
    game = GameOfLife(30, 40, [(2,3),(2,4),(2,5),(2,6),(2,7),(3,7),(4,6),(5,5),(6,4),(7,3)])

    while game.num_live_cells() > 0:
        print_grid(game)
        sleep(0.3)
        game.tick()
