import tkinter as tk

from organism import Organism
from microbe import Microbe
from genome import Genome
from environment import Environment
from brain import Brain
from generation import Generation


population = 1000

root = tk.Tk()
win_height = 700
win_width = 700

g0 = Generation()
env = Environment(root, win_height, win_width, g0, 10)
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