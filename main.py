import tkinter as tk

from microbe import Microbe
from environment import Environment


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
env.grid(column=0, row=0, padx=5, pady=5)
env.info_box.grid(column=1, row=0)
env.tick()
env.mainloop()