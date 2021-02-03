#%%
from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
from pathlib import Path
from threading import Thread
import tkinter as tk
#%%
model = load_model("./best.h5")

#%%
class GameUI(tk.Frame):
    def __init__(self, master=None, model=None):
        tk.Frame.__init__(self, master)
        self.master.title("三目並べ")

        self.state = State()

        self.next_action = pv_mcts_action(model, 0.0)

        self.c = tk.Canvas(self, width=240, height=240, highlightthickness=0)
        self.c.bind("<Button-1>", self.turn_of_human)
        self.c.pack()

        self.on_draw()
    
    def turn_of_human(self, event):
        if self.state.is_done():
            self.state = State()
            self.on_draw()
            return
        
        if not self.state.is_first_player():
            return

        x = int(event.x/80)
        y = int(event.y/80)
        if x < 0 or 2 < x or y < 0 or 2 < y:
            return
        action = x + y * 3

        if not (action in self.state.legal_actions()):
            return

        self.state = self.state.next(action)
        self.on_draw()

        self.master.after(1, self.turn_of_ai)

    def turn_of_ai(self):
        if self.state.is_done():
            return

        action = self.next_action(self.state)
        self.state = self.state.next(action)
        self.on_draw()

    def draw_piece(self, index, first_player):
        x = (index%3)*80+10
        y = int(index/3)*80+10
        if first_player:
            self.c.create_oval(x, y, x+60, y+60, width=2.0, outline="#FFFFFF")
        else:
            self.c.create_line(x, y, x+60, y+60, width=2.0, fill="#5D5D5D")
            self.c.create_line(x+60, y, x, y+60, width=2.0, fill="#5D5D5D")

    def on_draw(self):
        self.c.delete("all")
        self.c.create_rectangle(0,0,240,240,width=0.0,fill="#00A0FF")
        self.c.create_line(80,0,80,240,width=2.0,fill="#0077BB")
        self.c.create_line(160,0,160,240,width=2.0,fill="#0077BB")
        self.c.create_line(0,80,240,80,width=2.0,fill="#0077BB")
        self.c.create_line(0,160,240,160,width=2.0,fill="#0077BB")
        for i in range(9):
            if self.state.pieces[i] == 1:
                self.draw_piece(i, self.state.is_first_player())
            if self.state.enemy_pieces[i] == 1:
                self.draw_piece(i, not self.state.is_first_player())


#%%
f = GameUI(model=model)
f.pack()
f.mainloop()
# %%
