import math
import random

import numpy as np
import pygame
import Functions
import Receptor
from Pheromone import Pheromone
from copy import copy


class Ant:
    X = 0
    Y = 0

    Color = (255, 100, 0)
    Size = 5
    Max_velocity = 20.0
    Max_acceleration = 6.0
    # HOW STRONG (FAST) ANT CAN TURN
    SteerStrength = 35.0
    WanderStrength = 1.0
    ReceptorDistance = 7
    ReceptorAngle = math.pi / 3
    PheromoneDropTime = 6
    LifeTime = 1200.0

    HandlingFood = False
    Angle = int
    Velocity = None
    DesiredDirection = None
    LeftReceptor = MiddleReceptor = RightReceptor = None
    # IF ANT SEE FOOD TARGET IS FOOD
    IsTarget = bool
    # IF ANT DOESN'T SEE ANY FOOD && DOESN'T HANDLE ANY FOOD SHE IS SearchingForFood
    SearchingForFood = bool
    PheromoneType = int

    def __init__(self, Colony_X, Colony_Y, Colony_r, food, pheromones):
        self.Angle = random.random() * math.pi
        self.X = math.cos(self.Angle) * (Colony_r + self.Size + 1) + Colony_X
        self.Y = math.sin(self.Angle) * (Colony_r + self.Size + 1) + Colony_Y
        self.HandlingFood = False
        # self.Velocity = 5
        self.Velocity = pygame.Vector2(0, 0)
        self.DesiredDirection = pygame.Vector2(0, 0)
        self.LeftReceptor = Receptor.Receptor(math.cos(self.Angle-self.ReceptorAngle) * self.ReceptorDistance, math.sin(self.Angle-self.ReceptorAngle) * self.ReceptorDistance, food, pheromones)
        self.MiddleReceptor = Receptor.Receptor(math.cos(self.Angle) * self.ReceptorDistance, math.sin(self.Angle) * self.ReceptorDistance, food, pheromones)
        self.RightReceptor = Receptor.Receptor(math.cos(self.Angle+self.ReceptorAngle) * self.ReceptorDistance, math.sin(self.Angle+self.ReceptorAngle) * self.ReceptorDistance, food, pheromones)
        self.Receptors = [self.LeftReceptor, self.MiddleReceptor, self.RightReceptor]
        self.IsTarget = False
        self.SearchingForFood = True
        # TIMER not TIME
        self.PheromoneDropColdown = 0
        self.PheromoneType = 0
        self.LifeTime = self.LifeTime


    # def __init__(self, Colony_X, Colony_Y, Colony_r, food, pheromones):
    #     self.Angle = random.random() * math.pi
    #     x = math.cos(self.Angle) * (Colony_r + self.Size) + Colony_X
    #     y = math.sin(self.Angle) * (Colony_r + self.Size) + Colony_Y
    #     self.__init__(self, x, y, food, pheromones)

    def Move(self, max_X, max_Y, pheromones, food, colony):
        if self.CheckCollision(colony.X, colony.Y, colony.Size):
            if self.HandlingFood:
                colony.FoodDelivered()
                self.HandlingFood = False
                self.SearchingForFood = True
                self.IsTarget = False
            self.FlipAnt()
            self.X += math.cos(self.Angle) * 2
            self.Y += math.cos(self.Angle) * 2

        if self.CheckField(food):
            self.SearchingForFood = False
            self.IsTarget = False
            self.FlipAnt()
            return
        if self.HandlingFood:
            for receptor in self.Receptors:
                if receptor.CheckColony(colony, self.HandlingFood):
                    self.IsTarget = True
                    self.DesiredDirection = pygame.Vector2(receptor.X - self.X, receptor.Y - self.Y)
                    break
            if not self.IsTarget:
                self.FollowPheromones()
            # self.DesiredDirection = pygame.Vector2(math.cos(self.Angle), math.sin(self.Angle))
        elif not self.IsTarget:
            for receptor in self.Receptors:
                if receptor.CheckFood():
                    self.IsTarget = True
                    # self.DesiredDirection = pygame.Vector2(receptor.X - self.X, receptor.Y - self.Y) / 10
                    self.DesiredDirection = pygame.Vector2(receptor.X - self.X, receptor.Y - self.Y)
                    break
            if not self.IsTarget:
                self.FollowPheromones()
                # self.DesiredDirection = Functions.RandomReceptorDirection(self.Angle, self.ReceptorAngle)
                # self.DesiredDirection = self.Forward()
                # self.DesiredDirection = Functions.RandomCirclePoint(self.Angle, self.ReceptorAngle)
        self.DesiredDirection = (self.DesiredDirection * self.WanderStrength).normalize()
        desiredVelocity = self.DesiredDirection * self.Max_velocity
        desiredSteeringForce = (desiredVelocity - self.Velocity) * self.SteerStrength
        acceleration = copy(desiredSteeringForce)
        if acceleration.length() > self.SteerStrength:
            acceleration.scale_to_length(self.SteerStrength)

        self.Velocity += acceleration * 0.1
        if self.Velocity.length() > self.Max_velocity:
            self.Velocity.scale_to_length(self.Max_velocity)

        self.X += self.Velocity.x * 0.1
        self.Y += self.Velocity.y * 0.1
        if self.X < 0:
            self.X = max_X
        elif self.X > max_X:
            self.X = 0
        if self.Y < 0:
            self.Y = max_Y
        elif self.Y > max_Y:
            self.Y = 0

        self.Angle = math.atan2(self.Velocity.y, self.Velocity.x)
        self.UpdateReceptors()
        self.PheromoneDropColdown += 1
        if self.PheromoneDropColdown == self.PheromoneDropTime:
            pheromones.append(Pheromone(self.X, self.Y, self.HandlingFood))
            self.PheromoneDropColdown = 0

    def FollowPheromones(self):
        leftValue = self.LeftReceptor.CheckPheromones(self.SearchingForFood)
        middleValue = self.MiddleReceptor.CheckPheromones(self.SearchingForFood)
        rightValue = self.RightReceptor.CheckPheromones(self.SearchingForFood)
        if leftValue == middleValue == rightValue:
            self.DesiredDirection = Functions.RandomReceptorDirection(self.Angle, self.ReceptorAngle)
        elif leftValue > max(middleValue, rightValue):
            self.DesiredDirection = self.Left()
        elif middleValue >= rightValue:
            self.DesiredDirection = self.Forward()
        elif rightValue > middleValue:
            self.DesiredDirection = self.Right()

    def Left(self):
        return pygame.Vector2(math.cos(self.Angle-self.ReceptorAngle), math.sin(self.Angle-self.ReceptorAngle))

    def Forward(self):
        return pygame.Vector2(math.cos(self.Angle), math.sin(self.Angle))

    def Right(self):
        return pygame.Vector2(math.cos(self.Angle+self.ReceptorAngle), math.sin(self.Angle+self.ReceptorAngle))

    def UpdateReceptors(self):
        self.LeftReceptor.UpdatePosition(self.X, self.Y, self.Angle - self.ReceptorAngle, self.ReceptorDistance)
        self.MiddleReceptor.UpdatePosition(self.X, self.Y, self.Angle, self.ReceptorDistance)
        self.RightReceptor.UpdatePosition(self.X, self.Y, self.Angle + self.ReceptorAngle, self.ReceptorDistance)
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

    # FLIPS ANT 180 DEG
    def FlipAnt(self):
        self.Angle += math.pi
        self.DesiredDirection.rotate(180)
        self.Velocity = pygame.Vector2(0, 0)
        self.UpdateReceptors()
        return

    def CheckCollision(self, x, y, r):
        if math.dist((self.X, self.Y), (x, y)) <= self.Size + r:
            return True
        return False

    def CheckField(self, food):
        if self.HandlingFood:
            return
        for f in food:
            # FOOD RADIUS HAVE TO BE SMALLER THAN ANT !!!
            if math.dist((self.X, self.Y), (f.X, f.Y)) <= self.Size + f.Size:
                f.Amount -= 1
                if f.Amount == 0:
                    food.remove(f)
                self.HandlingFood = True
                return 1
        # strength = 0
