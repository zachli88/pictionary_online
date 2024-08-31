import pygame

class Board:
    ROWS = COLS = 80
    COLORS = {
        0: (255, 255, 255),
        1 : (0, 0, 0),
        2: (255, 0, 0),
        3: (0, 255, 0),
        4: (0, 0, 255),
        5: (255, 255, 0),
        6: (255, 140, 0),
        7: (139, 69, 19),
        8: (128, 0, 128),
    }
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.WIDTH = self.HEIGHT = self.ROWS * 8
        self.compressed_board = []
        self.board = self.create_board()

    def create_board(self):
        return [[(255, 255, 255) for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def translate_board(self):
        for row, _ in enumerate(self.compressed_board):
            for col, rgb in enumerate(self.compressed_board[row]):
                self.board[row][col] = self.COLORS[rgb]

    def draw(self, win):
        for row, _ in enumerate(self.board):
            for col, rgb in enumerate(self.board[row]):
                pygame.draw.rect(win, rgb, (self.x + col * 8, self.y + row * 8, 8, 8), 0)

        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.WIDTH, self.HEIGHT), 5)


    def click(self, x, y):
        col = int(x - self.x) // 8
        row = int(y - self.y) // 8
        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            return (row, col)
        return None

    def update(self, x, y, color, thickness = 3):
        neighbors = [(x, y)] + self.get_neighbors(x, y)
        for x, y in list(neighbors):
            if 0 <= x < self.COLS and 0 <= y < self.ROWS:
                self.board[y][x] = color
    
    def get_neighbors(self, x, y):
        return [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1), 
                (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]

    def clear(self):
        self.board = self.create_board()