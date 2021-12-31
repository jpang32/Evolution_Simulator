import tkinter as tk

from organism import Organism
from microbe import Microbe
from genome import Genome
from environment import Environment
from brain import Brain
from generation import Generation


start_at_gen = 100
population = 500

root = tk.Tk()
root.title('Evolution Simulator')

win_height = 400
win_width = 400

frame_rate = 100

env = Environment(root, win_height, win_width, frame_rate)
Organism.env = env

m_list = []
for i in range(population):
    m_list.append(Microbe())

env.add_members(m_list)

env.pack()
env.tick()
env.mainloop()