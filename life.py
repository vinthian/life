from bit_array import BitArray2D

class LifeGrid(BitArray2D):
    def __setitem__(self, coords, value):
        x, y = coords
        if x == -1 or x == self._width or y == -1 or y == self._height:
            pass
        else:
            super().__setitem__(coords, value)

    def __getitem__(self, coords):
        x, y = coords
        if x == -1 or x == self._width or y == -1 or y == self._height:
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
    def __init__(self, width = 20, height = 10):
        self.grid = LifeGrid(width, height)
        self.generation = 0

    def next(self):
        new_grid = LifeGrid(self.grid.width, self.grid.height)
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                neighbor_count = self._neighbor_count(x, y)
                if self.grid[x, y] == 1:
                    # Any live cell with fewer than two live neighbours dies,
                    #   as if caused by under-population.
                    # Any live cell with more than three live neighbours dies,
                    #   as if by overcrowding.
                    if neighbor_count < 2 or neighbor_count > 3:
                        new_grid[x, y] = 0
                    # Any live cell with two or three live neighbours lives on to
                    #   the next generation.
                    if neighbor_count == 2 or neighbor_count == 3:
                        new_grid[x, y] = 1
                # Any dead cell with exactly three live neighbours becomes a
                #   live cell, as if by reproduction.
                if self.grid[x, y] == 0 and neighbor_count == 3:
                    new_grid[x, y] = 1
        self.grid = new_grid
        self.generation += 1

    def _neighbor_count(self, x, y):
        neighbor_pos = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                        (x,     y - 1),             (x,     y + 1),
                        (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]
        neighbor_count = 0
        for coords in neighbor_pos:
            neighbor_count += self.grid[coords]
        return neighbor_count

    def draw(self):
        for y in range(self.grid.height):
            row = ""
            for x in range(self.grid.width):
                row += (str(self._neighbor_count(x, y)) if self.grid[x, y]
                        else chr(183))
            print(row)

    def _glider(self, x = 0, y = 0):
        # Clear out 3x3 area
        for j in range(3):
            for i in range(3):
                self.grid[x + i, y + j] = 0
        # Create Glider
        self.grid[x,     y + 2] = 1 #  X
        self.grid[x + 1, y + 2] = 1 #   X
        self.grid[x + 2, y + 2] = 1 # XXX
        self.grid[x + 2, y + 1] = 1
        self.grid[x + 1, y    ] = 1

    def _small_explorer(self, x = 0, y = 0):
        # Clear out 3x4 area
        for j in range(4):
            for i in range(3):
                self.grid[x + i, y + j] = 0
        # Create Small Explorer
        self.grid[x + 1, y    ] = 1 #  X
        self.grid[x    , y + 1] = 1 # XXX
        self.grid[x + 1, y + 1] = 1 # X X
        self.grid[x + 2, y + 1] = 1 #  X
        self.grid[x    , y + 2] = 1
        self.grid[x + 2, y + 2] = 1
        self.grid[x + 1, y + 3] = 1
