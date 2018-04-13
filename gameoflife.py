#!/usr/bin/python

# Conway's Game of Life
# github.com/semyon-san

import sys
from time import sleep

class Cell(object):
    CELL_LIVE = '#'
    CELL_DEAD = ' '

    def __init__(self, row, col, is_live=True):
        self._live = is_live
        self._future_live = is_live
        self._last_processed_time = 0

        self._processed = False

        self._row = row
        self._col = col


    def __str__(self):
        return Cell.CELL_LIVE if self._live else Cell.CELL_DEAD

    def live(self):
        self._future_live = True

    def die(self):
        self._future_live = False

    def is_live(self):
        return self._live

    def is_dead(self):
        return self._live == False

    def is_processed(self):
        return self._processed

    def processed(self, clock):
        self._processed = True
        self._last_processed_time = clock

    def sync(self, clock):
        if (clock != self._last_processed_time):
            self._processed = False
            self._last_processed_time = clock

    def change_state(self):
        self._live = self._future_live

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

class GameOfLife(object):
    def __init__(self, rows, cols, live_cells_coords):
        self._grid_rows = rows
        self._grid_cols = cols

        self._live_cells = {}

        self._changed_cells = []

        self._clock = 0

        self._grid = self._make_grid(rows, cols, live_cells_coords)

    def num_live_cells(self):
        return len(self._live_cells)

    def tick(self):
        for live_cell in self._live_cells:
            cell_y = live_cell.row
            cell_x = live_cell.col

            # processing the live cell and adjacent cells
            for y in range(cell_y-1, cell_y+1+1):
                for x in range(cell_x-1, cell_x+1+1):
                    if ((y >= 0) and (y < self._grid_rows)) and ((x >= 0) and (x < self._grid_cols)):
                        cell = self._grid[y][x]
                        cell.sync(self._clock)
                        if not cell.is_processed():
                            self._process(cell)

        self._progress()

    @property
    def grid(self):
        return self._grid

    @property
    def rows(self):
        return self._grid_rows

    @property
    def cols(self):
        return self._grid_cols

    def _process(self, cell):
        num_live_neighbours = self._num_live_neighbours(cell)
        if cell.is_live():
            if num_live_neighbours < 2 or num_live_neighbours > 3:
                cell.die() # solitude or overpopulation
                self._changed_cells.append(cell)
        else:
            if num_live_neighbours == 3:
                cell.live() # 3 is good
                self._changed_cells.append(cell)
        cell.processed(self._clock)

    def _num_live_neighbours(self, cell):
        n = 0
        for r in range(cell.row-1, cell.row+1+1):
            for c in range(cell.col-1, cell.col+1+1):
                if not (r == cell.row and c == cell.col):
                    if ((r >= 0) and (r < self._grid_rows)) and ((c >= 0) and (c < self._grid_cols)):
                        if self._grid[r][c].is_live():
                            n += 1
        return n

    def _update_clock(self):
        self._clock += 1

    def _progress(self):
        for cell in self._changed_cells:
            cell.change_state()
            if cell.is_live():
                self._live_cells[cell] = cell
            else:
                self._live_cells.pop(cell)

        self._changed_cells = []

        self._update_clock()

    def _make_grid(self, grid_rows, grid_cols, live_cells_coords):
        grid = [[Cell(r, c, is_live=False) for c in range(grid_cols)] for r in range(grid_rows)]

        for row, col in live_cells_coords:
            cell = grid[row][col]
            cell.live()
            cell.change_state()
            self._live_cells[cell] = cell

        return grid

def print_grid(game):
    grid = game.grid
    for r in range(game.rows):
        for c in range(game.cols):
            print(grid[r][c], end='')
        print()

if __name__ == '__main__':
    game = GameOfLife(rows=30, cols=40, live_cells_coords=[(2,3),(2,4),(2,5),(2,6),(2,7),(3,7),(4,6),(5,5),(6,4),(7,3)])

    while game.num_live_cells() > 0:
        print_grid(game)
        sleep(0.3)
        game.tick()
