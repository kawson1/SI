import Window
import Graph
import os
from multiprocessing import Process
import time


def BestPath():
    best_path, distance = win.graph.ComputeBestPath(win)
    print(best_path, distance)


graph = Graph.Graph(40, 40, 5)
win = Window.Window(graph)

# win.graph.DisplayDistances()
BestPath()
win.graph.AntsPath(win, 4)
# win.DisplayWindow()
