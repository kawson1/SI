import random
import math

import numpy as np
import pygame

import Functions
import Receptor
from Pheromone import Pheromone


class Ant:
    X = 0
    Y = 0

    Color = (255, 100, 0)
    Size = 5
    Max_velocity = 3
    Max_acceleration = 0.3
    SteerStrength = 2
    WanderStrength = 3
    ReceptorDistance = 7
    ReceptorAngle = math.pi / 3

    HandlingFood = False
    Angle = int
    Velocity = None
    DesiredDirection = None
    LeftReceptor = MiddleReceptor = RightReceptor = None
    PheromoneDropTime = int
    IsTargetFood = bool

    def __init__(self, X_position, Y_position, food, pheromones):
        self.X = X_position
        self.Y = Y_position
        self.Angle = 0
        self.HandlingFood = False
        # self.Velocity = 5
        self.Velocity = pygame.Vector2(0, 0)
        self.DesiredDirection = pygame.Vector2(0, 0)
        self.LeftReceptor = Receptor.Receptor(math.cos(self.Angle-self.ReceptorAngle) * self.ReceptorDistance, math.sin(self.Angle-self.ReceptorAngle) * self.ReceptorDistance, food, pheromones)
        self.MiddleReceptor = Receptor.Receptor(math.cos(self.Angle) * self.ReceptorDistance, math.sin(self.Angle) * self.ReceptorDistance, food, pheromones)
        self.RightReceptor = Receptor.Receptor(math.cos(self.Angle+self.ReceptorAngle) * self.ReceptorDistance, math.sin(self.Angle+self.ReceptorAngle) * self.ReceptorDistance, food, pheromones)
        self.Receptors = [self.LeftReceptor, self.MiddleReceptor, self.RightReceptor]
        self.PheromoneDropTime = 3
        self.IsTargetFood = False

    def Move(self, max_X, max_Y, pheromones, food):
        self.CheckField(food)
        if self.HandlingFood:
            self.FollowPheromones()
            # self.DesiredDirection = pygame.Vector2(math.cos(self.Angle), math.sin(self.Angle))
        if not self.IsTargetFood:
            for receptor in self.Receptors:
                if receptor.CheckFood():
                    self.IsTargetFood = True
                    self.DesiredDirection = pygame.Vector2(receptor.X - self.X, receptor.Y - self.Y) / 10
                    break
            if not self.IsTargetFood:
                self.DesiredDirection = Functions.RandomCirclePoint(self.Angle, self.ReceptorAngle)

        desiredVelocity = self.DesiredDirection * self.Max_velocity
        self.X += desiredVelocity.x
        self.Y += desiredVelocity.y
        if self.X < 0:
            self.X = max_X
        elif self.X > max_X:
            self.X = 0
        if self.Y < 0:
            self.Y = max_Y
        elif self.Y > max_Y:
            self.Y = 0

        self.Angle = math.atan2(desiredVelocity.y, desiredVelocity.x)
        self.LeftReceptor.UpdatePosition(self.X, self.Y, self.Angle-self.ReceptorAngle, self.ReceptorDistance)
        self.MiddleReceptor.UpdatePosition(self.X, self.Y, self.Angle, self.ReceptorDistance)
        self.RightReceptor.UpdatePosition(self.X, self.Y, self.Angle+self.ReceptorAngle, self.ReceptorDistance)
        self.PheromoneDropTime -= 1
        if self.PheromoneDropTime == 0:
            pheromones.append(Pheromone(self.X, self.Y, self.IsTargetFood))
            self.PheromoneDropTime = 3

    def FollowPheromones(self):
        leftValue = self.LeftReceptor.CheckPheromones()
        middleValue = self.MiddleReceptor.CheckPheromones()
        rightValue = self.RightReceptor.CheckPheromones()
        if leftValue > max(middleValue, rightValue):
            self.DesiredDirection = self.Left()
        elif middleValue > rightValue:
            self.DesiredDirection = self.Forward()
        elif rightValue > middleValue:
            self.DesiredDirection = self.Right()
        else:
            self.DesiredDirection = Functions.RandomCirclePoint(self.Angle, self.ReceptorAngle)

    def Left(self):
        return pygame.Vector2(math.cos(self.Angle-self.ReceptorAngle))

    def Forward(self):
        return pygame.Vector2(math.cos(self.Angle))

    def Right(self):
        return pygame.Vector2(math.cos(self.Angle+self.ReceptorAngle))

    # def Move(self, max_X, max_Y, pheromones, food):
    #     i = self.CheckPotentialField(pheromones, food)
    #     # if potential_move == 0:
    #     #     self.X += math.cos(self.Angle) * self.Velocity
    #     #     self.Y += math.sin(self.Angle) * self.Velocity
    #     # elif potential_move == 1:
    #     if i == -1:
    #         i = random.randint(0, 2)
    #     # LEFT CIRCLE
    #     if i == 1:
    #         self.Angle -= math.pi/3
    #     # RIGHT CIRCLE
    #     if i == 2:
    #         self.Angle += math.pi/3
    #     self.X += math.cos(self.Angle) * self.Velocity
    #     self.Y += math.sin(self.Angle) * self.Velocity
    #     if self.X < 0:
    #         self.X = max_X
    #     elif self.X > max_X:
    #         self.X = 0
    #
    #     if self.Y < 0:
    #         self.Y = max_Y
    #     elif self.Y > max_Y:
    #         self.Y = 0
        # self.CheckField(food)
        # pheromones.append(Pheromone(self.X, self.Y))


    # RESULTS:
    # 0 - MIDDLE CIRCLE
    # 1 - LEFT CIRCLE
    # 2 - RIGHT CIRCLE
    # -1 - RANDOM
    def CheckPotentialField(self, pheromones, food):
        if not self.HandlingFood:
            for f in food:
                # FOR MIDDLE CIRCLE
                if self.X + math.cos(self.Angle) < f.X < math.cos(self.Angle) and self.X + math.cos(self.Angle) < f.X < math.cos(self.Angle):
                    if self.Y + math.sin(self.Angle) < f.Y < math.sin(self.Angle) and self.Y + math.sin(self.Angle) < f.Y < math.sin(self.Angle):
                        return 0
    
                if self.X + math.cos(self.Angle-5) < f.X < math.cos(self.Angle-5) and self.X + math.cos(self.Angle-5) < f.X < math.cos(self.Angle-5):
                    if self.Y + math.sin(self.Angle-5) < f.Y < math.sin(self.Angle-5) and self.Y + math.sin(self.Angle-5) < f.Y < math.sin(self.Angle-5):
                        return 1
    
                if self.X + math.cos(self.Angle+5) < f.X < math.cos(self.Angle+5) and self.X + math.cos(self.Angle+5) < f.X < math.cos(self.Angle+5):
                    if self.Y + math.sin(self.Angle+5) < f.Y < math.sin(self.Angle+5) and self.Y + math.sin(self.Angle+5) < f.Y < math.sin(self.Angle+5):
                        return 2
        if self.HandlingFood:
            leftSensorStrength = 0
            middleSensorStrength = 0
            rightSensorStrength = 0
            for p in pheromones:
                if self.Size - p.Size < math.dist((self.X + math.cos(self.Angle) * self.Velocity, self.Y + math.sin(self.Angle) * self.Velocity), (p.X, p.Y)) < self.Size + p.Size:
                    middleSensorStrength += 1
                if self.Size - p.Size < math.dist((self.X + math.cos(self.Angle-5) * self.Velocity, self.Y + math.sin(self.Angle-5) * self.Velocity), (p.X, p.Y)) < self.Size + p.Size:
                    leftSensorStrength += 1
                if self.Size - p.Size < math.dist((self.X + math.cos(self.Angle+5) * self.Velocity, self.Y + math.sin(self.Angle+5) * self.Velocity), (p.X, p.Y)) < self.Size + p.Size:
                    rightSensorStrength += 1
            if leftSensorStrength == middleSensorStrength == rightSensorStrength:
                return -1
            return np.argmax([middleSensorStrength, leftSensorStrength, rightSensorStrength])
        return -1
            # if leftSensorStrength > middleSensorStrength and leftSensorStrength > rightSensorStrength:
            #     return 1
            # if rightSensorStrength > middleSensorStrength and rightSensorStrength > leftSensorStrength:
            #     return 2
            # if middleSensorStrength > leftSensorStrength and middleSensorStrength > rightSensorStrength:
            #     return 0

    def CheckField(self, food):
        if self.HandlingFood:
            return
        for f in food:
            # FOOD RADIUS HAVE TO BE SMALLER THAN ANT !!!
            if math.dist((self.X, self.Y), (f.X, f.Y)) <= self.Size + f.Size:
                food.remove(f)
                self.HandlingFood = True
                self.Angle += math.pi
                return
        # strength = 0
