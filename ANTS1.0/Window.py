import pygame
from Graph import *


class Window:
    pygame.init()
    pygame.display.set_caption("ANTS SIMULATOR")
    WINDOW = None
    graph = None
    window_run = True
    myfont = pygame.font.SysFont("monospace", 15)

    def __init__(self, graph):
        self.WINDOW = pygame.display.set_mode((graph.max_X * graph.Vertex_size, graph.max_Y * graph.Vertex_size))
        self.graph = graph

    def DrawObjects(self):
        for row in range(self.graph.max_Y):
            for col in range(self.graph.max_X):
                field = self.graph.FieldArray[row][col]
                if field is not None:
                    pygame.draw.rect(self.WINDOW, field.Color,
                                     (field.X * self.graph.Vertex_size, field.Y * self.graph.Vertex_size,
                                      self.graph.Vertex_size, self.graph.Vertex_size))
                    label = self.myfont.render(str(field.Index), 1, (0, 0, 255))
                    self.WINDOW.blit(label, (field.X * self.graph.Vertex_size, field.Y * self.graph.Vertex_size))
        self.DrawEdges(self.graph.Best_path_edges)
        # CODE BELOW PRINT ALL EDGES IN GRAPH.EDGES ON SCREEN
        # for i in range(self.graph.N):
        #     for j in range(i+1, self.graph.N):
        #         edge = self.graph.Edges[i][j]
        #         pygame.draw.aaline(self.WINDOW, edge.Color,
        #                            ((edge.v1.X + 1/2) * self.graph.Vertex_size, (edge.v1.Y + 1/2) * self.graph.Vertex_size),
        #                            ((edge.v2.X + 1/2) * self.graph.Vertex_size, (edge.v2.Y + 1/2) * self.graph.Vertex_size))

    def DrawEdges(self, Edges):
        for edge in Edges:
            pygame.draw.aaline(self.WINDOW, edge.Color,
                               ((edge.v1.X + 1 / 2) * self.graph.Vertex_size,
                                (edge.v1.Y + 1 / 2) * self.graph.Vertex_size),
                               ((edge.v2.X + 1 / 2) * self.graph.Vertex_size,
                                (edge.v2.Y + 1 / 2) * self.graph.Vertex_size))
        pygame.display.update()

    def DisplayWindow(self):
        while self.window_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.window_run = False
            self.ClearWindow()
            self.DrawObjects()
            self.graph.AntsPath(self, 5)
            # self.VerticesMoveAnimation(self.graph.Vertices[0], self.graph.Vertices[4], 0.2)
            pygame.display.update()

    def VerticesMoveAnimation(self, v1, v2, color, velocity):
        # vector = [v2.X - v1.X, v2.Y - v1.Y]
        # x = v1.X * self.graph.Vertex_size
        # y = v1.Y * self.graph.Vertex_size
        # while x != v2.X * self.graph.Vertex_size and y != v2.Y * self.graph.Vertex_size:
        #     pygame.draw.circle(self.WINDOW, color, (x + self.graph.Vertex_size/2, y + self.graph.Vertex_size/2), 2)
        #     pygame.display.update()
        #     time.sleep(0.2)
        #     x += vector[0] * 1/4 * velocity * self.graph.Vertex_size
        #     y += vector[1] * 1/4 * velocity * self.graph.Vertex_size
        pygame.draw.aaline(self.WINDOW, color,
                           ((v1.X + 1 / 2) * self.graph.Vertex_size,
                            (v1.Y + 1 / 2) * self.graph.Vertex_size),
                           ((v2.X + 1 / 2) * self.graph.Vertex_size,
                            (v2.Y + 1 / 2) * self.graph.Vertex_size))
        pygame.display.update()
        # time.sleep(0.2)
        return

    def ClearWindow(self):
        self.WINDOW.fill((0, 0, 0))
        self.DrawObjects()
        pygame.display.update()