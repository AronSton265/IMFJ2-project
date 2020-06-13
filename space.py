import pygame
import random
import numpy as np
from Planet import *

class Space:
    def __init__(self, size, screen, res, densi):
        self.size = size
        self.den=densi
        self.starnumb = size*size*self.den
        self.planetnumb = int((self.den*size)/20)
        self.stars = np.zeros((self.starnumb, 2))
        self.Planets = []
        self.res = res

    def Background(self):
        i = 0
        
        for i in range(self.starnumb):
            x = random.randrange(-(self.size-1)*self.res[0], self.size*self.res[0])
            y = random.randrange(-(self.size-1)*self.res[1], self.size*self.res[1])
            self.stars[[i],[0]]=x
            self.stars[[i],[1]]=y

            i += 1

    def createPlanets(self):
        i = 0
        for i in range(self.planetnumb):
            x = random.randrange(-(self.size-1)*self.res[0], self.size*self.res[0])
            y = random.randrange(-(self.size-1)*self.res[1], self.size*self.res[1])
            temp= Planet(x, y)
            self.Planets.append(temp)
            i += 1


    def Paint(self, screen, velx, vely):
        i = 0
        for i in range(self.starnumb):
            x= self.stars[[i],[0]] + velx
            self.stars[[i],[0]] = x
            y= self.stars[[i],[1]] + vely
            self.stars[[i],[1]] = y
            if (x >= 0 and x < self.res[0] and y >= 0 and y < self.res[1]):
                pygame.draw.circle(screen, (245,240,220), (int(x), int(y)), 3, 0)
            i += 1
        i = 0
        for i in range(self.planetnumb):
            self.Planets[i].paint(screen, velx, vely)
            i += 1

    def checkifInside(self, enteties, entetienumb, ship):
        i=0
        for i in range(entetienumb):
            check = enteties[i].checkifInsede(ship)
            if check:
                return True

        return False

