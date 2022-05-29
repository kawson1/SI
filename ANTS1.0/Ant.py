import random


class Ant:
    # DETERMINES HOW STRONGLY ANT IS IMPLIED BY NUMBER OF PHEROMONE
    # 0 - ANTS DOESN'T LOOK AT PHEROMONE
    alfa = 1
    # DECIDE HOW STRONGLY DISTANCE BETWEEN i & j MATTERS
    # BIGGER BETA - BIGGER CHANCE THAT ANT WILL GO THE SHORTEST EDGE
    # LOWER BETA  - DISTANCE DOESN'T MATTER
    beta = 3
    # INDEXES OF VISITED VERTICES
    tabu = []
    # HOW MUCH PHEROMONE ANT LEAVES
    Q1 = 1
    color = None

    def __init__(self):
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.tabu = []
        self.distance = 0
        self.Current_vertex = None

    # j - potential city (i -> j)
    # possible_vertices - vertices which are not in tabu
    def ComputeProbability(self, j, possible_vertices, edges):
        if len(possible_vertices) == 0:
            return 0
        if len(possible_vertices) == 1:
            return 1
        probability = 0
        suma = 0
        for vertex_idx in possible_vertices:
            pheromone = edges[self.tabu[-1]][vertex_idx].Pheromone
            distance = edges[self.tabu[-1]][vertex_idx].Distance
            suma += pow(pheromone, self.alfa)*pow(1/distance, self.beta)
        pheromone = edges[self.tabu[-1]][j].Pheromone
        distance = edges[self.tabu[-1]][j].Distance
        if suma == 0:
            return 1/len(possible_vertices)
        probability = (pow(pheromone, self.alfa)*pow(1/distance, self.beta))/suma
        # if probability == 0 and len(possible_vertices) == 2:
        #     print()
        return probability
