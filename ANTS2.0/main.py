import Window
from Ant import Ant
from Food import Food
from random import randint

win = Window.Window(300, 300)
win.Ants.append(Ant(150, 150, win.Food, win.Pheromones))
# win.Food.append(Food(randint(0, 300), randint(0, 300)))
# win.Food.append(Food(randint(0, 300), randint(0, 300)))
# win.Food.append(Food(randint(0, 300), randint(0, 300)))
win.DisplayWindow()
