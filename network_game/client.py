import socket
import pickle
from threading import *
import time

class Client(Thread):
    def __init__(self, host):
        Thread.__init__(self)
        self.host_ = host
        self.other_players_ = {}
        self.my_state_ = None
        self.quit_ = False
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start()
    
    def get_other_players(self):
        return self.other_players_

    def set_my_state(self, state):
        self.my_state_ = state


    def run(self):
        port =8000
        self.socket_.settimeout(1)
        try:
            self.socket_.connect((self.host_, port))
        except:
            print("cannot connect")
            return
        while not self.quit_:
            if self.my_state_:
                data = pickle.dumps(self.my_state_)
                self.socket_.send(data)
            try:
                data = self.socket_.recv(1024)
                self.other_players_ = pickle.loads(data)
            except:
                self.other_players_ = {}
            time.sleep(0.01)
        data = pickle.dumps("quit")
        self.socket_.send(data)
        print("I am quiting")
        self.socket_.close()

    def quit(self):
        self.quit_ = True

class ClientProxy:
    def __init__(self, host):
        self.other_players_ = []
        self.impl_ = Client(host)
    
    def get_other_players(self):
        return self.impl_.get_other_players().copy()

    def set_my_state(self, state):
        self.impl_.set_my_state(state)
    
    def quit(self):
        self.impl_.quit()