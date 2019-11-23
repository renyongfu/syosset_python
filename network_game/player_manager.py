import client
import sys
import time

"""
PlayerManager is a class in charge of get this player's state and draw other players
"""
class PlayerManager:
    def __init__(self, canvas, server_ip, player_name, ball, paddle):
        self.canvas_ = canvas
        self.player_name_ = player_name
        self.ball_ = ball
        self.paddle_ = paddle
        self.other_players_ = {}
        self.other_draw_ids_ = {}
        self.proxy_ = client.ClientProxy(server_ip)

    def get_my_state(self):
        try:
            ball_cord = self.canvas_.coords(self.ball_.id)
            pad_cord = self.canvas_.coords(self.paddle_.id)
            return {'name': self.player_name_, 'ball': ball_cord, 'paddle': pad_cord, 'score': self.ball_.score}
        except:
            return None

    def get_other_players(self):
        self.other_players_ = self.proxy_.get_other_players()

    def quit(self):
        self.proxy_.quit()

    def draw(self):
        quit_players = set()
        for address, info in self.other_players_.items():
            ball_coord = info['ball']
            if not ball_coord:
                quit_players.add(address)
                continue
            pad_coord = info['paddle']
            name = info['name']
            if address not in self.other_draw_ids_:
                # A new player just joined
                ball_id = self.canvas_.create_oval(ball_coord[0], ball_coord[1], ball_coord[2], ball_coord[3])
                pad_id = self.canvas_.create_rectangle(pad_coord[0], pad_coord[1], pad_coord[2], pad_coord[3])
                text_id = self.canvas_.create_text(pad_coord[0] + 30, pad_coord[1]-10, text=name)
                self.other_draw_ids_[address] = (ball_id, pad_id, text_id)
            else:
                # Existing player update
                ids = self.other_draw_ids_[address]
                cords = self.canvas_.coords(ids[0])
                self.canvas_.move(ids[0], ball_coord[0] - cords[0], ball_coord[1] - cords[1])
                cords = self.canvas_.coords(ids[1])
                self.canvas_.move(ids[1], pad_coord[0] - cords[0], pad_coord[1] - cords[1])
                self.canvas_.move(ids[2], pad_coord[0] - cords[0], pad_coord[1] - cords[1])

        # Remove the players who just quit
        for address, ids in self.other_draw_ids_.items():
            if address not in self.other_players_:
                quit_players.add(address)
        for address in quit_players:
            if address not in self.other_draw_ids_:
                continue
            ids = self.other_draw_ids_[address]
            self.canvas_.delete(ids[0])
            self.canvas_.delete(ids[1])
            self.canvas_.delete(ids[2])
            self.other_draw_ids_.pop(address, None)

    def update(self):
        # Get this player's state and send the information to the sever
        my_state = self.get_my_state()
        if not my_state:
            return False
        self.proxy_.set_my_state(my_state)
        # Get other players states and draw them
        self.get_other_players()
        self.draw()
        return True
