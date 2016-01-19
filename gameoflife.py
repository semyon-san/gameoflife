#!/usr/bin/python

# Conway's Game of Life
# github.com/semyon-san

import sys
from time import sleep

class Cell(object):
    CELL_LIVE = '#'
    CELL_DEAD = ' '

    def __init__(self, is_live, row, col):
        self._live = is_live
        self._processed = False
        self._row = row
        self._col = col

    def __str__(self):
        return Cell.CELL_LIVE if self._live else Cell.CELL_DEAD

    def live(self):
        self._live = True

    def die(self):
        self._live = False

    def is_live(self):
        return self._live

    def is_dead(self):
        return self._live == False

    def is_processed(self):
        return self._processed

    def processed(self):
        self._processed = True

    def unprocessed(self):
        self._processed = False

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

class GameOfLife(object):
    def __init__(self, grid_rows, grid_cols, live_cells_coords):
        self._grid_rows = grid_rows
        self._grid_cols = grid_cols

        self._current_live_cells = []
        self._future_live_cells = []

        self._processed_cells = []

        self._current_grid = self._make_grid(grid_rows, grid_cols, live_cells_coords)
        self._future_grid = self._make_grid(grid_rows, grid_cols, [])

    def num_live_cells(self):
        return len(self._current_live_cells)

    def tick(self):
        for live_cell in self._current_live_cells:
            row = live_cell.row
            col = live_cell.col

            # processing the live cell and adjacent cells
            for r in range(row-1, row+1+1):
                for c in range(col-1, col+1+1):
                    if ((r >= 0) and (r < self._grid_rows)) and ((c >= 0) and (c < self._grid_cols)):
                        cell = self._current_grid[r][c]
                        if not cell.is_processed():
                            self._process(cell)

        self._progress()

    @property
    def grid(self):
        return self._current_grid

    @property
    def rows(self):
        return self._grid_rows

    @property
    def cols(self):
        return self._grid_cols

    def _process(self, cell):
        current_cell = cell
        future_cell = self._future_grid[current_cell.row][current_cell.col]

        n = self._num_live_neighbours(current_cell)
        if current_cell.is_live():
            if n < 2:
                future_cell.die() # solitude
            elif n > 3:
                future_cell.die() # overpopulation
            else:
                future_cell.live() # 3 is good
                self._future_live_cells.append(future_cell)
        else:
            if n == 3:
                future_cell.live() # 3 is good
                self._future_live_cells.append(future_cell)
            else:
                future_cell.die() # remain dead

        current_cell.processed()
        self._processed_cells.append(current_cell)

    def _num_live_neighbours(self, cell):
        n = 0
        for r in range(cell.row-1, cell.row+1+1):
            for c in range(cell.col-1, cell.col+1+1):
                if not (r == cell.row and c == cell.col):
                    if ((r >= 0) and (r < self._grid_rows)) and ((c >= 0) and (c < self._grid_cols)):
                        if self._current_grid[r][c].is_live():
                            n += 1
        return n

    def _progress(self):
        tmp_grid = self._current_grid
        self._current_grid = self._future_grid 
        self._future_grid = tmp_grid

        self._current_live_cells = self._future_live_cells
        self._future_live_cells = []

        for cell in self._processed_cells:
            cell.unprocessed()
        self._processed_cells = []

    def _make_grid(self, grid_rows, grid_cols, live_cells_coords):
        grid = [[Cell(False, row=r, col=c) for c in range(grid_cols)] for r in range(grid_rows)]
        
        for row, col in live_cells_coords:
            cell = grid[row][col]
            cell.live()
            self._current_live_cells.append(cell)

        return grid


if __name__ == '__main__':
    game = GameOfLife(40, 40, [(12, 10), (11, 11), (12, 12), (11, 10), (13, 10)])

    while game.num_live_cells() > 0:
        grid = game.grid

        for r in range(game.rows):
            for c in range(game.cols):
                print(grid[r][c], end='')
            print()
        sleep(0.3)
        game.tick()
