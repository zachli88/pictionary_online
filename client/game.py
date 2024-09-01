import pygame
from button import TextButton
from top_bar import TopBar
from board import Board
from leaderboard import Leaderboard
from player import Player
from bottom_bar import BottomBar
from chat import Chat
from network import Network

class Game:
    COLORS = {
        (255, 255, 255): 0,
        (0, 0, 0): 1,
        (255, 0, 0): 2,
        (0, 255, 0): 3,
        (0, 0, 255): 4,
        (255, 255, 0): 5,
        (255, 140, 0): 6,
        (139, 69, 19): 7,
        (128, 0, 128): 8,
    }
    def __init__(self, win, connection = None):
        pygame.font.init()
        self.connection = connection
        self.win = win
        self.WIDTH = 1300
        self.HEIGHT = 1000
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.leaderboard = Leaderboard(40, 125)
        self.board = Board(310, 125)
        self.top_bar = TopBar(10, 10, 1280, 100)
        self.top_bar.change_round(1)
        self.bottom_bar = BottomBar(310, 770, self)
        self.chat = Chat(1000, 125)
        self.players = []
        self.skip_button = TextButton(120, 675, 80, 40, (255, 255, 0), "Skip")
        self.draw_color = (0, 0, 0)
        self.BG = (255, 255, 255)

    def add_player(self, player):
        self.players.append(player)
        self.leaderboard.add_player(player)

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
            skips = self.connection.send({1:[]})
            print("Clicked skip button")

        click_board = self.board.click(*mouse)
        if click_board:
            self.board.update(click_board[1], click_board[0], self.draw_color)
            self.connection.send({8:[click_board[1], click_board[0], self.COLORS[tuple(self.draw_color)]]})

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            try:
                response = self.connection.send({3:[]})
                self.board.compressed_board = response
                self.board.translate_board()

                response = self.connection.send({9:[]})
                self.top_bar.time = response

                response = self.connection.send({2: []})
                self.chat.update_chat(response)

                if not self.top_bar.word:
                    self.top_bar.word = self.connection.send({6: []})
                    self.top_bar.round = self.connection.send({5: []})
                    self.top_bar.max_round(len(self.players))

                # response = self.connection.send()
                # for player in response:
                #     p = Player(player)
                #     self.add_player(p)
            except:
                run = False
                break
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                
                if pygame.mouse.get_pressed()[0]:
                    self.check_clicks()
                    self.bottom_bar.button_events()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.connection.send({0:[self.chat.typing]})
                        self.chat.typing = ""
                    else:
                        key_name = pygame.key.name(event.key)
                        key_name = key_name.lower()
                        self.chat.type(key_name)
        
        pygame.quit()