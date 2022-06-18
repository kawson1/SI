import Window
from Ant import Ant
from Colony import Colony
from Food import Food
from random import randint

win = Window.Window(300, 300)
win.Colony = Colony(randint(0, 300), randint(0, 300))
win.Ants.append(Ant(win.Colony.X, win.Colony.Y, win.Colony.Size, win.Food, win.Pheromones))
win.Ants.append(Ant(win.Colony.X, win.Colony.Y, win.Colony.Size, win.Food, win.Pheromones))

# win.Food.append(Food(randint(0, 300), randint(0, 300)))
# win.Food.append(Food(randint(0, 300), randint(0, 300)))
# win.Food.append(Food(randint(0, 300), randint(0, 300)))
win.DisplayWindow()
