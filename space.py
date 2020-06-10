import pygame
import random
import numpy as np

class Space:
    def __init__(self, size, screen):
        self.size = size
        self.starnumb = size*size*100
        self.stars = np.zeros((self.starnumb, 2))

    def Background(self):
        i = 0
        
        for i in range(self.starnumb):
            x = random.randrange(-(self.size-1)*640, self.size*640)
            y = random.randrange(-(self.size-1)*360, self.size*360)
            self.stars[[i],[0]]=x
            self.stars[[i],[1]]=y

            i += 1

    def Paint(self, screen, velx, vely):
        i = 0
        for i in range(self.starnumb):
            x= self.stars[[i],[0]] + velx
            self.stars[[i],[0]] = x
            y= self.stars[[i],[1]] + vely
            self.stars[[i],[1]] = y
            if (x >= 0 and x < 640 and y >= 0 and y < 360):
                pygame.draw.circle(screen, (245,240,220), (int(x), int(y)), 3, 0)
            i += 1
