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
