import math as m
import random


def ComputeDistance(x1, x2, y1, y2):
    return m.sqrt(pow(x2-x1, 2) + pow(y2-y1, 2))


class Edge:
    v1 = None
    v2 = None
    Distance = 0
    Pheromone = 1   # τ(t)
    Pheromone_2 = 0 # τ(t+1)
    # PHEROMONE FROM (t, t+1)
    Delta_T = 0     # ∆τ(t, t+1)
    # HOW FAST PHEROMONE EVAPORATES
    p = 0.5

    Color = (255, 255, 255)

    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.Distance = round(ComputeDistance(v1.X, v2.X, v1.Y, v2.Y))
        self.Pheromone = 1
        self.Pheromone_2 = 0
        self.Delta_T = 0
        # self.Distance = random.randint(1, 20)
