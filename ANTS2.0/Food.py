class Food:
    X = int
    Y = int
    Amount = int

    Color = (0, 150, 0)
    Size = 20

    def __init__(self, X_position, Y_position):
        self.X = X_position
        self.Y = Y_position
        self.Amount = 30
