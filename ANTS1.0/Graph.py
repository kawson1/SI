import os
import random
import math
import itertools
import time
from copy import copy

from Ant import Ant
from Vertex import *
from Edge import *

class Graph:
    Vertices = []
    Edges = [[]]
    Best_path_edges = []
    # DEFAULT START VERTEX = 0 !YET!
    Start_vertex = 0
    Possible_paths = []
    Vertex_size = 20

    def __init__(self, max_X=50, max_Y=50, N=5):
        self.max_X = max_X
        self.max_Y = max_Y
        self.N = N
        self.FieldArray = [[None for i in range(max_X)] for i in range(max_Y)]
        self.GenerateVertices()
        self.Vertices[self.Start_vertex].Color = (0, 255, 0)
        self.GenerateEdges()
        # self.Possible_paths = self.PossiblePaths()

    def GenerateVertices(self):
        X_coords = random.sample(range(0, self.max_X), self.N);
        Y_coords = random.sample(range(0, self.max_Y), self.N);
        # CREATE N VERTICES
        for i in range(self.N):
            self.Vertices.append(Vertex(X_coords[i], Y_coords[i], i))
            self.FieldArray[Y_coords[i]][X_coords[i]] = self.Vertices[i]

    def GenerateEdges(self):
        self.Edges = [[None for i in range(self.N)] for i in range(self.N)]
        for idx, vertex in enumerate(self.Vertices):
            for next_idx in range(idx+1, len(self.Vertices)):
                self.Edges[idx][next_idx] = self.Edges[next_idx][idx] = Edge(vertex, self.Vertices[next_idx])

    def PossiblePaths(self, start_vertex=0):
        values = list(range(0, self.N))
        values.remove(start_vertex)
        return list(itertools.permutations(values))

    def ComputeBestPath(self, window):
        min_distance = math.inf
        best_path = None
        # POSSIBLE PATHS ARRAY DOESN'T HAVE START VERTEX INDEX!
        # SO VERTEX_IDX IS NEXT
        iterations = 0
        # CLEAR CONSOLE
        clear = lambda: os.system('cls')
        clear()
        for possible_path in self.Possible_paths:
            window.ClearWindow()
            iterations += 1
            print(f"Searched: {iterations}/{len(self.Possible_paths)}")
            print(f"Progress: {iterations/len(self.Possible_paths)*100:.2f}%")
            # time.sleep(0.5)
            clear()
            previous_vertex_idx = self.Start_vertex
            distance = 0
            # EDGES WHICH ARE USED IN POSSIBLE_PATH
            current_edges = []
            for vertex_idx in possible_path:
                current_edges.append(self.Edges[previous_vertex_idx][vertex_idx])
                distance += self.Edges[previous_vertex_idx][vertex_idx].Distance
                previous_vertex_idx = vertex_idx
            distance += self.Edges[previous_vertex_idx][self.Start_vertex].Distance
            current_edges.append(self.Edges[previous_vertex_idx][self.Start_vertex])
            if distance < min_distance:
                min_distance = distance
                best_path = possible_path
            window.DrawEdges(current_edges)
        best_path = list(best_path)
        best_path.append(self.Start_vertex)
        self.Best_path_edges = current_edges
        print(f"BEST PATH: {best_path}")
        print(f"DISTANCE : {min_distance}")
        return best_path, min_distance

    def DisplayDistances(self):
        for v1 in range(self.N):
            for v2 in range(v1+1, self.N):
                print(f"V{v1} -> V{v2} = ", self.Edges[v1][v2].Distance)

    # m - NUMBER OF ANTS
    def AntsPath(self, window, m=1):
        # LIST OF CURRENT ANTS
        ants = []
        for i in range(m):
            random_vertex_idx = random.randint(0, self.N-1)
            ant = Ant()
            ants.append(ant)
            # APPEND START VERTEX IDX
            ant.tabu.append(random_vertex_idx)
            self.Vertices[random_vertex_idx].Ants_1.append(ant)

        min_distance = math.inf
        best_path = []
        # MAX CYCLES OF ANT 
        MC = 100000000
        cycles = 0
        # ANTS GENERATION
        t = 0
        p1 = [1]
        p2 = [2]
        k = 0
        # LOOP FOR ANTS GENERATIONS (t, t+1 etc)
        while cycles < MC:
            window.ClearWindow()
            # HOW MUCH VISITED VERTICES PER ANT
            n = 0
            cycles += 1
            # LOOP FOR ANT MOVES ( 1n = 1 ants move [from i to j])
            while n != self.N-1:
                n += 1
                # LOOP FOR EVERY VERTEX
                for i in range(self.N):
                    # LOOP FOR EVERY ANT IN VERTEX
                    for ant in self.Vertices[i].Ants_1:
                        ant.Current_vertex = None
                        possible_vertices = self.PossibleAntVertices(ant)
                        rand = random.random()
                        probabilities = []
                        # COMPUTE PROBABILITY OF EVERY POSSIBLE MOVE FOR SINGLE ANT
                        for vertex_idx in possible_vertices:
                            probabilities.append(ant.ComputeProbability(vertex_idx, possible_vertices, self.Edges))
                        left_limit = 0
                        # CHOSE 1 VERTEX FOR ANT TO MOVE
                        for j in range(0, len(probabilities)):
                            if rand < probabilities[j]+left_limit:
                                # ANT GOES FROM i -> j
                                self.Vertices[possible_vertices[j]].Ants_2.append(ant)
                                # self.Vertices[ant.tabu[-1]].Ants_1.remove(ant)
                                # ANIMATION HERE (??)
                                window.VerticesMoveAnimation(self.Vertices[ant.tabu[-1]], self.Vertices[possible_vertices[j]], ant.color, 1)
                                self.Edges[ant.tabu[-1]][possible_vertices[j]].Delta_T += ant.Q1
                                ant.distance += self.Edges[ant.tabu[-1]][possible_vertices[j]].Distance
                                ant.tabu.append(possible_vertices[j])
                                ant.Current_vertex = self.Vertices[possible_vertices[j]]
                                break
                            else:
                                left_limit += probabilities[j]
                        if ant.Current_vertex is None:
                            print()
                # COMPUTE EDGE PHEROMONE FOR (t+1)
                for i in range(self.N):
                    for j in range(i+1, self.N):
                        e = self.Edges[i][j]
                        e.Pheromone_2 = e.p * e.Pheromone + e.Delta_T
                        e.Delta_T = 0
                for vertex in self.Vertices:
                    vertex.Ants_1 = vertex.Ants_2
                    vertex.Ants_2 = []
            # ADD DISTANCE FROM LAST VERTEX TO START VERTEX
            for ant in ants:
                # if k == 0:
                #     p1 = ant.tabu
                # else:
                #     p2 = ant.tabu
                # k += 1
                ant.distance += self.Edges[ant.tabu[-1]][ant.tabu[0]].Distance
                window.VerticesMoveAnimation(self.Vertices[ant.tabu[-1]], self.Vertices[ant.tabu[0]], ant.color, 1)
                if ant.distance < min_distance:
                    min_distance = ant.distance
                    # SHOULD ADD START VERTEX IDX TO END OF ant.tabu
                    best_path = ant.tabu
                # UPDATE EDGES FROM LAST TO STARTING VERTEX
                e = self.Edges[ant.tabu[-1]][ant.tabu[0]]
                e.Pheromone_2 = e.p * e.Pheromone + ant.Q1
                try:
                    self.Vertices[ant.tabu[-1]].Ants_1.remove(ant)
                except ValueError:
                    print()
                ant.tabu = [ant.tabu[0]]
                ant.distance = 0
                self.Vertices[ant.tabu[0]].Ants_1.append(ant)
            for i in range(0, len(self.Edges)):
                for j in range(i + 1, len(self.Edges)):
                    self.Edges[i][j].Pheromone = self.Edges[i][j].Pheromone_2
                    self.Edges[i][j].Pheromone_2 = 0
            #self.PrintPheromones()
        # return best_path, min_distance
        print("BEST PATH: ", best_path)
        print("DISTANCE : ", min_distance)
        return

    def PossibleAntVertices(self, ant):
        possible_vertices_idx = [i for i in range(self.N)]
        for vertex_idx in ant.tabu:
            possible_vertices_idx.remove(vertex_idx)
        return possible_vertices_idx

    def ArePathsEquals(self, p1, p2):
        p1_copy = copy(p1)
        p2_copy = copy(p2)
        p1_copy.sort()
        p2_copy.sort()
        for i in range(0, len(p1)):
            if p1_copy[i] != p2_copy[i]:
                return False
        return True

    def PrintPheromones(self):
        for i in range(0, len(self.Edges)):
            for j in range(i+1, len(self.Edges)):
                print(f"{i} -> {j} = {self.Edges[i][j].Pheromone}")
