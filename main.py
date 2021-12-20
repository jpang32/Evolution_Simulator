import tkinter as tk

from microbe import Microbe
from genome import Genome
from environment import Environment


population = 1000

root = tk.Tk()
win_height = 700
win_width = 700
c = tk.Canvas(root, height=win_height, width=win_width, bg='white')

## Draw one Microbe on a Tkinter Canvas

m_list = []
for i in range(population):
    m_list.append(Microbe())

env = Environment(root, win_height, win_width, m_list, 10)

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