import time as t
from _thread import *
from chat import Chat

class Round:
    def __init__(self, word, player_drawing, game):
        self.word = word
        self.player_drawing = player_drawing
        self.player_guessed = []
        self.skips = 0
        self.game = game
        self.player_scores = {player: 0 for player in self.game.players}
        self.time = 75
        self.chat = Chat(self)
        start_new_thread(self.time_thread, ())

    def time_thread(self):
        while self.time > 0:
            t.sleep(1)
            self.time -= 1
        self.end_round("Time is up")

    def guess(self, player, wrd):
        correct = wrd == self.word
        if correct:
            self.player_guessed.append(player)
            self.chat.update_chat(f"{player.get_name()} has guessed the word")
            return True
        self.chat.update_chat(f"{player.get_name()}: {wrd}")
        return False
    
    def player_left(self, player):
        if player in self.player_scores:
            del self.player_scores[player]

        if player in self.player_guessed:
            self.player_guessed.remove(player)

        if player == self.player_drawing:
            self.chat.update_chat("Drawing player disconnected - round skipped")
            self.end_round("Drawing player left")

    def skip(self):
        self.skips += 1
        if self.skips > len(self.player_scores.keys()) - 2:
            return True
        return False
    
    def get_scores(self):
        return self.player_scores
    
    def get_score(self, player):
        if player in self.player_scores:
            return self.player_scores[player]
        else:
            raise Exception("Player not in score list")

    def end_round(self, msg):
        for player in self.game.players:
            if player in self.player_scores:
                player.update_score(self.player_scores[player])
        self.game.round_ended()