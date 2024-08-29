from round import Round
from board import Board
import random

class Game:
    def __init__(self, id, players):
        self.id = id
        self.players = players
        self.words_used = set()
        self.round = None
        self.board = Board()
        self.round_count = 1
        self.player_draw_ind = 0
        self.start_new_round()

    def start_new_round(self):
        try:
            round_word = self.get_word()
            self.round = Round(round_word, self.players[self.player_draw_ind], self)
            self.round_count += 1

            if self.player_draw_ind >= len(self.players):
                self.round_ended()
                self.end_game()

            self.player_draw_ind += 1

        except Exception:
            self.end_game()

    def player_guess(self, player, guess):
        return self.round.guess(player, guess)
    
    def get_player_scores(self):
        scores = {player.get_name():player.get_score() for player in self.players}
        return scores

    def player_disconnected(self, player):
        if player in self.players:
            player_ind = self.players.index(player)
            if player_ind >= self.player_draw_ind:
            # if player_ind <= self.player_draw_ind:
                self.player_draw_ind -= 1
            self.players.remove(player)
            self.round.player_left(player)
        else:
            raise Exception("Player not in game")
        
        if len(self.players) <= 2:
            self.end_game()

    def skip(self):
        if self.round:
            new_round = self.round.skip()
            if new_round:
                self.round_ended()
            return new_round
        else:
            raise Exception("No round started")

    def round_ended(self):
        self.start_new_round()
        self.board.clear()

    def update_board(self, x, y, color):
        if not self.board:
            raise Exception("No board created")
        self.board.update(x, y, color)

    def get_word(self):
        with open("words.txt") as file:
            words = []

            for line in file:
                word = line.strip()
                if word not in self.words_used:
                    words.append(word)

            r = random.randint(0, len(words) - 1)
            round_word = words[r].strip()
            self.words_used.add(round_word)
            return round_word

    def end_game(self):
        print(f"[GAME] Game {self.id} ended")
        for player in self.players:
            player.game = None