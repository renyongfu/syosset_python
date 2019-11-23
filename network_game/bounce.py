from tkinter import *
import random
import time
import player_manager
import sys


class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.color = color
        self.score = 0

        self.reset()

    def reset(self):
        self.id = canvas.create_oval(10, 10, 25, 25, fill=self.color)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)

        self.x = starts[0]
        self.y = -3
        self.canvas_height = canvas.winfo_height()
        self.canvas_width = canvas.winfo_width()

        self.is_hitting_bottom = False
        self.score = 0
        print("your score =", self.score)

        canvas.move(self.id, 245, 100)

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)

        pos = self.canvas.coords(self.id)

        if pos[1] <= 0:
            self.y = 1

        if pos[3] >= self.canvas_height:
            # self.y = -1
            self.is_hitting_bottom = True

        if self.hit_top_paddle(pos) == True:
            self.score += 1
            print("your score=", self.score)
            self.y = -3

        if self.hit_bottom_paddle(pos) == True:
            self.y = 1

        if pos[0] <= 0:
            self.x = 3

        if pos[2] >= self.canvas_width:
            self.x = -3
        if self.is_hitting_bottom:
            old_id = self.id
            self.reset()
            self.canvas.delete(old_id)

    def hit_top_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True

        return False

    def hit_bottom_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[1] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
                return True

        return False

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)

        self.x = 0
        self.canvas_width = canvas.winfo_width()

        canvas.move(self.id, 200, 300)

        canvas.bind_all('<KeyPress-Left>', self.move_left)
        canvas.bind_all('<KeyPress-Right>', self.move_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)

        pos = self.canvas.coords(self.id)

        if pos[0] <= 0:
            self.x = 0

        if pos[2] >= self.canvas_width:
            self.x = 0

    def move_left(self, event):
        self.x = -5

    def move_right(self, event):
        self.x = 5


tk = Tk()
tk.title('Game')
canvas = Canvas(tk, width=550, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

paddle = Paddle(canvas, 'green')
ball = Ball(canvas, paddle, 'red')

if len(sys.argv) < 3:
    print("please run as 'bounce.py server_ip your_player_name")
    quit()

player_man = player_manager.PlayerManager(canvas, sys.argv[1], sys.argv[2], ball, paddle)

while 1:
    if not player_man.update():
        break

    ball.draw()
    paddle.draw()


    tk.update_idletasks()
    tk.update()
    time.sleep(0.02)
player_man.quit()