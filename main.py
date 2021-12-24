import tkinter as tk

from organism import Organism
from microbe import Microbe
from genome import Genome
from environment import Environment
from brain import Brain
from generation import Generation

'''
root = tk.Tk()
canvas = tk.Canvas(root, height=700, width=700, bg='white')

a= canvas.create_rectangle(210, 210, 220, 220)
b = canvas.create_rectangle(220, 220, 230, 230)

canvas.addtag_enclosed('alive',200, 200, 300, 300)
g = canvas.create_rectangle(250, 250, 260, 260)

print(canvas.gettags(g))
print(canvas.gettags(a))
print(canvas.gettags(b))

'''
start_at_gen = 100
population = 500

root = tk.Tk()
root.title('Evolution Simulator')
win_height = 350
win_width = 350

frame_rate = 100

g0 = Generation()
env = Environment(root, win_height, win_width, g0, frame_rate)
Organism.env = env

m_list = []
for i in range(population):
    m_list.append(Microbe())

g0.add_members(m_list)


env.pack()
env.tick()
env.mainloop()


'''
from abc import ABC, abstractmethod


class A:

    def __init__(self):
        self.test()

    @abstractmethod
    def test(self):
        pass

class B(A):

    def __init__(self):
        super(B, self).__init__()

    def test(self):
        print(type(self))
        print("test")


b = B()
'''