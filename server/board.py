class Board:
    ROWS = COLS = 80
    def __init__(self):
        self.data = self._create_empty_board()

    def update(self, x, y, color):
        neighbors = [(x, y)] + self.get_neighbors(x, y)
        for x, y in list(neighbors):
            if 0 <= x < self.COLS and 0 <= y < self.ROWS:
                self.data[y][x] = color
    
    def get_neighbors(self, x, y):
        return [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1), 
                (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]

    def clear(self):
        self.data = self._create_empty_board()

    def _create_empty_board(self):
        return [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
    
    def fill(self, x, y):
        pass

    def get_board(self):
        return self.data