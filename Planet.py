import pygame
import random
import numpy as np

class Planet:
    def __init__(self, x, y):
        self.size = random.randrange(20, 100)
        self.gravaty = self.size*1.5
        self.coord=[x,y]

    def paint(self, screen, velx, vely):
        pygame.draw.circle(screen, (60,179,113), (self.coord[0] + velx, self.coord[1] + vely), self.size, 0)
        self.coord[0] += velx
        self.coord[1] += vely
        