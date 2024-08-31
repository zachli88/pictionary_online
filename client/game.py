import pygame
from button import Button, TextButton
from top_bar import TopBar
from main_menu import MainMenu
from board import Board
from leaderboard import Leaderboard
from player import Player
from bottom_bar import BottomBar
from chat import Chat

class Game:
    def __init__(self):
        self.WIDTH = 1300
        self.HEIGHT = 1000
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.leaderboard = Leaderboard(40, 125)
        self.board = Board(310, 125)
        self.top_bar = TopBar(10, 10, 1280, 100)
        self.top_bar.change_round(1)
        self.bottom_bar = BottomBar(310, 770, self)
        self.chat = Chat(1000, 125)
        self.players = [Player("Zach"), Player("2wwwwwwww22"), Player("John"), Player("Joe")]
        for player in self.players:
            self.leaderboard.add_player(player)
        self.skip_button = TextButton(120, 675, 80, 40, (255, 255, 0), "Skip")
        self.draw_color = (0, 0, 0)
        self.BG = (255, 255, 255)

    def draw(self):
        self.win.fill(self.BG)
        self.leaderboard.draw(self.win)
        self.top_bar.draw(self.win)
        self.board.draw(self.win)
        self.skip_button.draw(self.win)
        self.bottom_bar.draw(self.win)
        self.chat.draw(self.win)
        pygame.display.update()

    def check_clicks(self):
        mouse = pygame.mouse.get_pos()
        if self.skip_button.click(*mouse):
            print("Clicked skip button")

        click_board = self.board.click(*mouse)
        if click_board:
            self.board.update(click_board[1], click_board[0], self.draw_color)

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                
                if pygame.mouse.get_pressed()[0]:
                    self.check_clicks()
                    self.bottom_bar.button_events()

                if event.type == pygame.KEYDOWN:
                    key_name = pygame.key.name(event.key)
                    key_name = key_name.lower()
                    self.chat.type(key_name)
        
        pygame.quit()

if __name__ == "__main__":
    pygame.font.init()
    g = Game()
    g.run()