import pygame
import sys
from network import Network
from game import Game
from player import Player

def initialize_pygame():
    try:
        pygame.init()
        if not pygame.display.get_init():
            pygame.display.init()
        if not pygame.font.get_init():
            pygame.font.init()
        return True
    except pygame.error as e:
        print(f"Failed to initialize Pygame: {e}")
        return False

class MainMenu:
    def __init__(self):
        if not initialize_pygame():
            print("Failed to initialize Pygame. Exiting.")
            sys.exit(1)
        
        self.WIDTH = 1300
        self.HEIGHT = 1000
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pictionary Online")
        self.name = ""
        self.waiting = False
        self.BG = (255, 255, 255)
        self.name_font = pygame.font.SysFont("comicsans", 60)
        self.title_font = pygame.font.SysFont("comicsans", 120)
        self.enter_font = pygame.font.SysFont("comicsans", 40)

    def draw(self):
        self.win.fill(self.BG)
        title = self.title_font.render("Pictionary Online", 1, (0, 0, 0))
        self.win.blit(title, (self.WIDTH // 2 - title.get_width() // 2, 50))
        name = self.name_font.render("Enter Display Name: " + self.name, 1, (0, 0, 0))
        self.win.blit(name, (100, 400))

        if self.waiting:
            waiting = self.enter_font.render("In Queue...", 1, (0, 0, 0))
            self.win.blit(waiting, (self.WIDTH // 2 - waiting.get_width() // 2, 800))
        else:
            enter = self.enter_font.render("Press Enter to join a game", 1, (0, 0, 0))
            self.win.blit(enter, (self.WIDTH // 2 - enter.get_width() // 2, 800))

        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            self.draw()
            clock.tick(30)
            
            if self.waiting:
                response = self.n.send({-1:[]})
                if response:
                    g = Game(self.win, self.n)
                    for player in response:
                        p = Player(player)
                        g.add_player(p)
                    g.run()
                    return  # Exit the method after game ends

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(self.name) > 1:
                            self.waiting = True
                            self.n = Network(self.name)
                    else:
                        self.type(pygame.key.name(event.key).lower())

    def type(self, char):
        if char == "backspace":
            self.name = self.name[:-1]
        elif char == "space":
            self.name += " "
        elif len(char) == 1:
            self.name += char
        
        self.name = self.name[:16]  # Limit name to 16 characters

if __name__ == "__main__":
    main = MainMenu()
    main.run()