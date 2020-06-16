import pygame
import random
import numpy as np

class Planet:
    def __init__(self, x, y):
        self.size = random.randrange(20, 100)
        self.coord=[x,y]
        self.color = (random.randrange(20, 90), random.randrange(130, 240), random.randrange(80, 140))

    def paint(self, screen, velx, vely):
        pygame.draw.circle(screen, self.color, (self.coord[0] + velx, self.coord[1] + vely), self.size, 0)
        self.coord[0] += velx
        self.coord[1] += vely

    def checkifInsede(self, ship):
        if(ship[0]-self.size-10 < self.coord[0]  and  self.coord[0] < ship[0]+self.size+10):
            if(ship[1]-self.size-10 < self.coord[1]  and  self.coord[1] < ship[1]+self.size+10):
                return True
        return False
        