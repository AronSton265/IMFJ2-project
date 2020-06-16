import pygame
import random
import numpy as np
from Planet import *
from Sun import *

class Space:
    def __init__(self, size, screen, res, densi):
        self.size = size
        self.den=densi
        #number of stars
        self.starnumb = size*size*self.den
        #number of planets if any
        self.planetnumb = int((self.den*size)/20)
        #number of suns if any
        self.sunnumb = int(self.planetnumb/8)
        #array with the position of the stars
        self.stars = np.zeros((self.starnumb, 2))
        #array with suns
        self.Suns = []
        #array with planets
        self.Planets = []
        #variable to control if the planets were created
        self.planetsCreated = False
        #variable to control if the suns were created
        self.sunsCreated = False
        #resolution of the window
        self.res = res

#creates the starts(just background)
    def Background(self):
        i = 0
        
        for i in range(self.starnumb):
            x = random.randrange(-(self.size-1)*self.res[0], self.size*self.res[0])
            y = random.randrange(-(self.size-1)*self.res[1], self.size*self.res[1])
            self.stars[[i],[0]]=x
            self.stars[[i],[1]]=y

            i += 1

#creates the planets
    def createPlanets(self):
        i = 0
        for i in range(self.planetnumb):
            x = random.randrange(-(self.size-1)*self.res[0], self.size*self.res[0])
            y = random.randrange(-(self.size-1)*self.res[1], self.size*self.res[1])
            temp= Planet(x, y)
            self.Planets.append(temp)
            i += 1
        self.planetsCreated = True

#creates the suns
    def createSuns(self):
        i = 0
        for i in range(self.sunnumb):
            x = random.randrange(-(self.size-1)*self.res[0], self.size*self.res[0])
            y = random.randrange(-(self.size-1)*self.res[1], self.size*self.res[1])
            temp= Sun(x, y)
            self.Suns.append(temp)
            i += 1
        self.sunsCreated = True

#paints every object
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
        
        if self.planetsCreated:
            i = 0
            for i in range(self.planetnumb):
                self.Planets[i].paint(screen, velx, vely)
                i += 1
        
        if self.sunsCreated:
            i=0
            for i in range(self.sunnumb):
                self.Suns[i].paint(screen, velx, vely)
                i += 1

#checks if the ship is insede any object in this class
    def checkifInside(self, enteties, entetienumb, ship):
        i=0
        for i in range(entetienumb):
            check = enteties[i].checkifInsede(ship)
            if check:
                return True

        return False

