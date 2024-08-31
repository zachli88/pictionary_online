import pygame

class Leaderboard:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.WIDTH = 240
        self.HEIGHT_ENTRY = 80
        self.players = []
        self.name_font = pygame.font.SysFont("comicsans", 20, bold = True)
        self.score_font = pygame.font.SysFont("comicsans", 15, bold = True)
        self.rank_font = pygame.font.SysFont("comicsans", 30, bold = True)


    def draw(self, win):
        scores = [(player.get_name(), player.get_score()) for player in self.players]
        scores.sort(key = lambda x: x[1], reverse = True)

        for index, score in enumerate(scores):
            if index % 2 == 0:
                color = (255, 255, 255)
            else:
                color = (200, 200, 200)
            pygame.draw.rect(win, color, (self.x, self.y + index * self.HEIGHT_ENTRY, self.WIDTH, self.HEIGHT_ENTRY))

            rank = self.rank_font.render("#" + str(index + 1), 1, (0, 0, 0))
            win.blit(rank, (self.x + 10, self.y + index * self.HEIGHT_ENTRY + self.HEIGHT_ENTRY / 2 - rank.get_height() / 2))

            name = self.name_font.render(score[0], 1, (0, 0, 0))
            win.blit(name, (self.x+ self.WIDTH / 3, self.y + index * self.HEIGHT_ENTRY + 20))

            score = self.score_font.render("Score: " + str(score[1]), 1, (0, 0, 0))
            win.blit(score, (self.x + self.WIDTH / 3, self.y + index * self.HEIGHT_ENTRY + 45))

        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.WIDTH, self.HEIGHT_ENTRY * len(self.players)), 5)

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)