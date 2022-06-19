import Window
from Ant import Ant
from Colony import Colony
from Food import Food
from random import randint

win = Window.Window(600, 600)
win.Colony = Colony(300, 300)
for n in range(40):
    win.Ants.append(Ant(win.Colony.X, win.Colony.Y, win.Colony.Size, win.Food, win.Pheromones))


# win.Food.append(Food(randint(0, 300), randint(0, 300)))
# win.Food.append(Food(randint(0, 300), randint(0, 300)))
# win.Food.append(Food(randint(0, 300), randint(0, 300)))
win.DisplayWindow()
