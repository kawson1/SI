from datetime import time


class Pheromone:
    X = int
    Y = int
    Size = float
    # TIME IN ms
    EvaporateMaxTime = 600.0
    EvaporateTime = float
    Color = (102, 178, 255)

    # TYPE OF PHEROMONE
    # 0 - BLUE, WAY TO HOME
    # 1 - RED, WAY TO FOOD
    Type = int

    def __init__(self, X_position, Y_position, Type):
        self.X = X_position
        self.Y = Y_position
        self.Size = 2.0
        self.EvaporateTime = self.EvaporateMaxTime
        self.Type = Type
        if Type == 0:
            self.Color = (102, 178, 255)
        else:
            self.Color = (255, 102, 102)
