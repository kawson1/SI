import math

import pygame
from numpy import random


# RETURNS RANDOM POINT ON CIRCLE WITH RADIUS = 1
def RandomCirclePoint(angle, receptor_angle):
    # 1/3 => LOOKING FOR POINT BETWEEN angle-30 < angle < angle+30
    alpha = 2 * receptor_angle * math.pi * random.random() + angle - receptor_angle * math.pi
    x = math.cos(alpha)
    y = math.sin(alpha)
    return pygame.Vector2(x, y)


def RandomReceptorDirection(angle, receptor_angle):
    r = random.randint(0, 3)
    if r == 0:
        return pygame.Vector2(math.cos(angle-receptor_angle), math.sin(angle-receptor_angle))
    elif r == 1:
        return pygame.Vector2(math.cos(angle), math.sin(angle))
    else:
        return pygame.Vector2(math.cos(angle+receptor_angle), math.sin(angle+receptor_angle))
