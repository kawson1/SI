import math
import time

import pygame.time


class Receptor:
    Size = 5
    Food = []
    Pheromones = []
    Color = (160, 160, 160)

    X = int
    Y = int

    def __init__(self, x, y, food, pheromones):
        self.Food = food
        self.Pheromones = pheromones
        self.X = x
        self.Y = y

    # 1 - FOUND FOOD
    # 0 - DIDNT FOUND
    def CheckFood(self):
        for f in self.Food:
            if math.dist((self.X, self.Y), (f.X, f.Y)) <= (self.Size + f.Size):
                return 1
        return 0

    def CheckPheromones(self):
        count = 0
        for p in self.Pheromones:
            if math.dist((self.X, self.Y), (p.X, p.Y)) <= (self.Size + p.Size):
                count += 1
        return count

    # offset - DISTANCE BETWEEN ANT AND RECEPTOR
    def UpdatePosition(self, X, Y, angle, offset):
        self.X = math.cos(angle) * offset + X
        self.Y = math.sin(angle) * offset + Y
