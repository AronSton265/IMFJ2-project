import pygame
import random
import numpy as np

class Sun:
    def __init__(self, x, y):
        self.size = random.randrange(150, 300)
        self.coord=[x,y]
        self.color = (random.randrange(200, 255), random.randrange(180, 240), random.randrange(130, 190))

    def paint(self, screen, velx, vely):
        pygame.draw.circle(screen, self.color, (self.coord[0] + velx, self.coord[1] + vely), self.size, 0)
        self.coord[0] += velx
        self.coord[1] += vely

    def checkifInsede(self, ship):
        if(ship[0]-self.size-5 < self.coord[0]  and  self.coord[0] < ship[0]+self.size+5):
            if(ship[1]-self.size-5 < self.coord[1]  and  self.coord[1] < ship[1]+self.size+5):
                return True
        return False