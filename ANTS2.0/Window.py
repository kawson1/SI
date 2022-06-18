import time
import math

import pygame

from Food import Food


class Window:
    FPS = 30
    clock = pygame.time.Clock()

    pygame.init()
    pygame.display.set_caption("ANTS SIMULATOR")
    WINDOW = None
    window_run = True
    myfont = pygame.font.SysFont("monospace", 15)

    X_size = int
    Y_size = int
    Ants = []
    Food = []
    Pheromones = []
    Colony = None

    def __init__(self, X_Size, Y_Size):
        self.WINDOW = pygame.display.set_mode((X_Size, Y_Size))
        self.X_size = X_Size
        self.Y_size = Y_Size

    def DisplayWindow(self):
        while self.window_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.window_run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.AddFood(pygame.mouse.get_pos())
            self.DrawObjects()
            # time.sleep(0.05)
            # time.sleep(0.03)
            dt = self.clock.tick(self.FPS) / self.FPS
            self.PheromonesEvaporation(dt)
            self.ClearWindow()
            # self.VerticesMoveAnimation(self.graph.Vertices[0], self.graph.Vertices[4], 0.2)
            # pygame.display.update()

    def ClearWindow(self):
        self.WINDOW.fill((0, 0, 0))
        pygame.display.update()

    def DrawObjects(self):
        # ANTS
        for ant in self.Ants:
            old_X = ant.X
            old_Y = ant.Y
            ant.Move(self.X_size, self.Y_size, self.Pheromones, self.Food, self.Colony)
            pygame.draw.circle(self.WINDOW, ant.Color, (ant.X, ant.Y), ant.Size)
            self.DrawReceptors()
        # FOOD
        for f in self.Food:
            pygame.draw.circle(self.WINDOW, f.Color, (f.X, f.Y), f.Size)
        # PHEROMONES
        for p in self.Pheromones:
            pygame.draw.circle(self.WINDOW, p.Color, (p.X, p.Y), p.Size)
        # COLONY
        pygame.draw.circle(self.WINDOW, self.Colony.Color, (self.Colony.X, self.Colony.Y), self.Colony.Size)
        pygame.display.update()

    def DrawReceptors(self):
        ant = self.Ants[0]
        # left circle
        pygame.draw.circle(self.WINDOW, ant.LeftReceptor.Color, (ant.LeftReceptor.X, ant.LeftReceptor.Y), ant.LeftReceptor.Size)
        # middle circle
        pygame.draw.circle(self.WINDOW, ant.MiddleReceptor.Color, (ant.MiddleReceptor.X, ant.MiddleReceptor.Y), ant.MiddleReceptor.Size)
        # right circle
        pygame.draw.circle(self.WINDOW, ant.RightReceptor.Color, (ant.RightReceptor.X, ant.RightReceptor.Y), ant.RightReceptor.Size)

    def AddFood(self, position):
        self.Food.append(Food(position[0], position[1]))

    def PheromonesEvaporation(self, dt):
        for p in list(self.Pheromones):
            p.EvaporateTime -= dt
            # p.Color[0] += 1.3
            # p.Color[1] += 2.59
            if p.EvaporateTime <= 0:
                self.Pheromones.remove(p)
