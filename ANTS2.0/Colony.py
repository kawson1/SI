from Ant import Ant


class Colony:
    Size = 30
    Color = (153, 76, 0)
    X = int
    Y = int
    Ants = []
    Food = 0

    def __init__(self, X_position, Y_position):
        self.X = X_position
        self.Y = Y_position

    def Status(self):
        print(f"Food: {self.Food}")

    def FoodDelivered(self):
        self.Food += 1
        print("DONIESIONO JEDZENIE!")
        self.Status()
        return

    def AddAnt(self, food, pheromones):
        self.Ants.append(Ant(self.X, self.Y, self.Size, food, pheromones))
