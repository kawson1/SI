class Pheromone:
    X = int
    Y = int

    Color = (102, 178, 255)
    Size = 3

    # TYPE OF PHEROMONE
    # 0 - BLUE, WAY TO HOME
    # 1 - RED, WAY TO FOOD
    Type = int

    def __init__(self, X_position, Y_position, Type):
        self.X = X_position
        self.Y = Y_position
        self.Type = Type
        if Type == 0:
            self.Color = (102, 178, 255)
        else:
            self.Color = (255, 102, 102)
