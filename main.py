import tkinter as tk

from organism import Organism
from microbe import Microbe
from genome import Genome
from environment import Environment
from brain import Brain
from generation import Generation


start_at_gen = 100
num_members = 500

root = tk.Tk()
root.title('Evolution Simulator')

win_height = 400
win_width = 400

frame_rate = 100

env = Environment(root, win_height, win_width, frame_rate, num_members=num_members)

m_list = []
for i in range(num_members):
    m_list.append(Microbe())

env.add_members(m_list)

env.pack()
env.tick()
env.mainloop()