import uuid
import numpy as np
import sockets
from libserver import Message
from server import sessions, players
import uuid
from utils import send_object_message
import types

HEADER = 10

class Player():
    """
    Player class used to identify playes and how the are represented in the game session.
    """
    def __init__(self, sign="", username=None, message_obj=None):
        self.id  = uuid.uuid4()
        self.sign = sign
        self.username = username
        self.message_obj = message_obj
        self.game_session = None


    @property
    def in_session(self):
        if not self.game_session:
            return False
        
        if self.game_session.id in sessions:
            if self.id in sessions[self.game_session.id].players:
                return True
        return False

    @staticmethod
    def remove_user(id):
        try:
            del players[id]
        except KeyError:
            pass

class GameSession(Object):
    signs = ["X", "O"]
    def __init__(self, player1=None, player2=None)
        self.id = self.gen_id()
        self.player1 = player1
        self.player2 = player2
        self.board = np.full((3, 3), "", dtype=str)
        self.assign_player_signs()
    
    @property
    def players(self):
        res = []
        self.player1 and res.append(self.player1.id)
        self.player2 and res.append(self.player2.id)
        return res

    def gen_id(self):
        id = uuid.uuid4()
        while id in sessions:
            id  = uuid.uuid4()
        return id
    

    def update_board(self, row, col, player):
        if self.player1.id == player.id:
            player = self.player1
        elif self.player2.id == player.id:
            player = self.player2
        if player is None:
            return False

        value = player.sign

        if (self.board[row, col] == ""):
            if value.lower() in ["o", "x"] :
                self.board.
                data = {"action": "UPDATE:BOARD", self.board.tolist() }
                self.board[row, col] = value
                send_object_message(self.player1, "update:board", self.board)  
                send_object_message(self.player2, "update:board", self.board)
            else:
                send_object_message(player, "error", "Please use a valid input or you'll be blocked!")  
                return False
            game_state = self._check_game()
            if not game_state is None:
                send_object_message(self.player1, "update:board", self.board)  
                send_object_message(self.player2, "update:board", self.board)
        return True

        def _check_game(self):
            for i in range(3):
                if self.board[i, 0] != "" and self.board[i, 0] == self.board[i, 1] == self.board[i, 2] :
                    return self.board[i, 0]
                if self.board[0, i] != "" and self.board[0, i] == self.board[1, i] == self.board[2, i] :
                    return self.board[0, i]
                if self.board[0, 0] != "" and self.board[0, 0] == self.board[1, 1] == self.board[2, 2] :
                    return self.board[0, 0]
                if self.board[0, 2] != "" and self.board[0, 2] == self.board[1, 1] == self.board[2, 0] :
                    return self.board[0, 2]
                for i in range(3):
                    for j in range(3):
                        if self.board[i, j] == "":
                            return None
                return ""

    def assign_player_signs(self):
        if self.player1:
            self.player1.sign = self.signs.pop(0)
        if self.player2:
            self.player2.sign = self.signs.pop(0)

    def join_game_session(self):
        pass





        
