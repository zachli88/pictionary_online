class Player:
    def __init__(self, ip, name):
        self.game = None
        self.ip = ip
        self.name = name
        self.score = 0
    
    def set_game(self, game):
        self.game = game

    def update_score(self, x):
        self.score += x
    
    def guess(self, wrd):
        return self.game.player_guess(self, wrd)

    def disconnect(self):
        self.game.player_disconnected(self)

    def get_score(self):
        return self.score
    
    def get_name(self):
        return self.name
    
    def get_ip(self):
        return self.ip