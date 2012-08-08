from bit_array import BitArray2D

class LifeGrid(BitArray2D):
    def __init__(self, width, height):
        self._alive_set = set()
        self._dirty_set = set()

        super().__init__(width, height)

        # Decent performance boost when pre-defining ranges
        self.x_range = range(0, self._width)
        self.y_range = range(0, self._height)
        self.range_3 = range(3)

    def __setitem__(self, coords, value):
        x, y = coords
        # Check bounds
        if x not in self.x_range or y not in self.y_range:
            return

        # Update _dirty_set, mark neighbors as dirty
        for near_x, near_y in [(x - 1 + i, y - 1 + j)
                               for i in self.range_3 for j in self.range_3]:
            # For coordinates that are in bounds
            if near_x in self.x_range and near_y in self.y_range:
                if value and coords not in self._alive_set:
                    self._dirty_set.add((near_x, near_y))
                if not value and coords in self._alive_set:
                    if (near_x, near_y) in self._dirty_set:
                        self._dirty_set.remove((near_x, near_y))
        # Update _alive_set
        if value and coords not in self._alive_set:
            self._alive_set.add(coords)
        if not value and coords in self._alive_set:
            self._alive_set.add(coords)

        super().__setitem__(coords, value)

    def __getitem__(self, coords):
        x, y = coords
        if x not in self.x_range or y not in self.y_range:
            return False
        else:
            return super().__getitem__(coords)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height


class Life(object):
    def __init__(self, width=20, height=10):
        self.grid = LifeGrid(width, height)
        self.generation = 0

    @property
    def update_count(self):
        return len(self.grid._dirty_set)

    @property
    def dirty_list(self):
        return self.grid._dirty_set

    def neighbor_count(self, x, y):
        return self.grid[x - 1, y - 1] + self.grid[x - 1, y    ] + \
               self.grid[x - 1, y + 1] + self.grid[x    , y - 1] + \
               self.grid[x    , y + 1] + self.grid[x + 1, y - 1] + \
               self.grid[x + 1, y    ] + self.grid[x + 1, y + 1]

    def next(self):
        new_grid = LifeGrid(self.grid.width, self.grid.height)
        for coords in self.grid._dirty_set:
            neighbor_count = self.neighbor_count(*coords)
            if self.grid[coords]:
                # Any live cell with fewer than two live neighbours dies,
                #   as if caused by under-population.
                # Any live cell with more than three live neighbours dies,
                #   as if by overcrowding.
                if neighbor_count < 2 or neighbor_count > 3:
                    new_grid[coords] = 0
                # Any live cell with two or three live neighbours lives on to
                #   the next generation.
                if neighbor_count == 2 or neighbor_count == 3:
                    new_grid[coords] = 1
                # Any dead cell with exactly three live neighbours becomes a
                #   live cell, as if by reproduction.
            if self.grid[coords] == 0 and neighbor_count == 3:
                new_grid[coords] = 1
        self.grid = new_grid
        self.generation += 1
        return True

    def _glider(self, x=0, y=0):
        self.grid[x,     y + 2] = 1 #  X
        self.grid[x + 1, y + 2] = 1 #   X
        self.grid[x + 2, y + 2] = 1 # XXX
        self.grid[x + 2, y + 1] = 1
        self.grid[x + 1, y    ] = 1

    def _small_explorer(self, x=0, y=0):
        self.grid[x + 1, y    ] = 1 #  X
        self.grid[x    , y + 1] = 1 # XXX
        self.grid[x + 1, y + 1] = 1 # X X
        self.grid[x + 2, y + 1] = 1 #  X
        self.grid[x    , y + 2] = 1
        self.grid[x + 2, y + 2] = 1
        self.grid[x + 1, y + 3] = 1

    def _osc1(self, x=0, y=0):
        self.grid[x, y    ] = 1 # X
        self.grid[x, y + 1] = 1 # X
        self.grid[x, y + 2] = 1 # X

    def _osc2(self, x=0, y=0):
        self.grid[x + 1, y    ] = 1 #  XXX
        self.grid[x + 2, y    ] = 1 # XXX
        self.grid[x + 3, y    ] = 1
        self.grid[x    , y + 1] = 1
        self.grid[x + 1, y + 1] = 1
        self.grid[x + 2, y + 1] = 1

    def _osc3(self, x=0, y=0):
        self.grid[x    , y    ] = 1 # XX
        self.grid[x + 1, y    ] = 1 # X
        self.grid[x    , y + 1] = 1 #    X
        self.grid[x + 2, y + 3] = 1 #   XX
        self.grid[x + 3, y + 3] = 1
        self.grid[x + 3, y + 2] = 1

    def _gospers_glider_gun(self, x=0, y=0):
        self.grid[x + 1, y + 5] = 1 # XX
        self.grid[x + 2, y + 5] = 1 # XX
        self.grid[x + 2, y + 6] = 1
        self.grid[x + 2, y + 6] = 1
        self.grid[x + 11, y + 5] = 1 #   XX
        self.grid[x + 11, y + 6] = 1 #  X
        self.grid[x + 11, y + 7] = 1 # X
        self.grid[x + 12, y + 4] = 1 # X
        self.grid[x + 12, y + 8] = 1 # X
        self.grid[x + 13, y + 3] = 1 #  X
        self.grid[x + 13, y + 9] = 1 #   XX
        self.grid[x + 14, y + 3] = 1
        self.grid[x + 14, y + 9] = 1
        self.grid[x + 15, y + 6] = 1 #  X
        self.grid[x + 16, y + 4] = 1 #   X
        self.grid[x + 16, y + 8] = 1 # X XX
        self.grid[x + 17, y + 5] = 1 #   X
        self.grid[x + 17, y + 6] = 1 #  X
        self.grid[x + 17, y + 7] = 1 #
        self.grid[x + 18, y + 6] = 1
        self.grid[x + 21, y + 3] = 1 #     X
        self.grid[x + 21, y + 4] = 1 #   X X
        self.grid[x + 21, y + 5] = 1 # XX
        self.grid[x + 22, y + 3] = 1 # XX
        self.grid[x + 22, y + 4] = 1 # XX
        self.grid[x + 22, y + 5] = 1 #   X X
        self.grid[x + 23, y + 2] = 1 #     X
        self.grid[x + 23, y + 6] = 1
        self.grid[x + 25, y + 1] = 1
        self.grid[x + 25, y + 2] = 1
        self.grid[x + 25, y + 6] = 1
        self.grid[x + 25, y + 7] = 1
        self.grid[x + 35, y + 4] = 1
        self.grid[x + 35, y + 5] = 1
        self.grid[x + 36, y + 4] = 1
        self.grid[x + 36, y + 5] = 1
