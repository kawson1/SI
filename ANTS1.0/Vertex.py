class Vertex:
    # ANTS FROM T
    Ants_1 = []
    # ANTS FROM T+1
    Ants_2 = []
    Color = (255, 255, 255)
    Index = None

    def __init__(self, X, Y, Index):
        self.X = X
        self.Y = Y
        self.Index = Index
        self.Ants_1 = []
        self.Ants_2 = []
