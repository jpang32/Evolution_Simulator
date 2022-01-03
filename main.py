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

info_box = tk.Text(root, width=50)
info_box.insert('1.0', 'Generation: ')
info_box.insert('1.12', 'TEst')

env = Environment(root, win_height, win_width, frame_rate, num_members=num_members)

m_list = []
for i in range(num_members):
    m_list.append(Microbe())

env.add_members(m_list)
env.grid(column=0, row=0, padx=5, pady=5)
info_box.grid(column=1, row=0)
env.tick()
env.mainloop()