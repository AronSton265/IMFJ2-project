import pygame
import pygame.freetype
from space import *

# Define a main function, just to keep things nice and tidy
def main():

    # Initialize pygame, with the default parameters
    pygame.init()

    # Define the size/resolution of our window
    #res = (640, 360)
    res = (848, 480)
    # Create a window and a display surface
    screen = pygame.display.set_mode(res)
    # Game loop, runs forever
    size = 3
    mov = 1
    velx = 0
    vely = 0
    tempvelx = 0
    tempvely = 0
    maxspead = 8
    densidade = 120
    correntcoord = [0,0]
    #maxcoord = [((size+1)*res[0])/2,(size+1)*res[1]]
    space = Space(size, screen, res, densidade)
    space.Background()
    space.createPlanets()
    space.calcGrav()
    while (True):
        pygame.time.delay(10)
        # Process OS events
        for event in pygame.event.get():
            # Checks if the user closed the window
            if (event.type == pygame.QUIT):
                # Exits the application immediately
                exit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a]):
            velx=velx+mov
        if (keys[pygame.K_d]):
            velx=velx-mov
        if (keys[pygame.K_s]):
            vely=vely-mov
        if (keys[pygame.K_w]):
            vely=vely+mov

        if (velx > maxspead):
            velx = maxspead
        elif (velx < -maxspead):
            velx = -maxspead
        if (vely > maxspead):
            vely = maxspead
        elif (vely < -maxspead):
            vely = -maxspead

        correntcoord[0] = correntcoord[0] - velx
        correntcoord[1] = correntcoord[1] - vely

        if (correntcoord[0] < (size-1)*res[0]  and  correntcoord[0] > -(size-1)*res[0]):
            tempvelx = velx
        else:
            tempvelx = 0

        if (correntcoord[1] < (size-1)*res[1]  and  correntcoord[1] > -(size-1)*res[1]):
            tempvely = vely
        else:
            tempvely = 0
        #if ((maxcoord[0]-correntcoord[0]) > maxcoord[0]-200):
        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0,0,20))

        space.Paint(screen, tempvelx, tempvely)
        createShip(res[0]/2, res[1]/2, 20, screen, tempvelx, tempvely)
        #pygame.draw.circle(screen, (245,0,0), (200, 200), 40, 0)
        #planet 20min max 100
        #sun 150min 300max
        #black hole 10min 40max
        pygame.display.flip()

def createShip(originx, originy, size, screen, velx, vely):
        
        if (vely >= 0):
            if (velx < 0):
                A=[originx + size, originy - size]
                B=[originx, originy + size]
                C=[originx - size, originy]
            elif (velx > 0):
                A=[originx - size, originy - size]
                B=[originx, originy + size]
                C=[originx + size, originy]
            else:
                A=[originx, originy - size]
                B=[originx + (size/2), originy + size]
                C=[originx - (size/2), originy + size]
            
        else:
            if (velx < 0):
                A=[originx + size, originy + size]
                B=[originx, originy - size]
                C=[originx - size, originy]
            elif (velx > 0):
                A=[originx - size, originy + size]
                B=[originx, originy - size]
                C=[originx + size, originy]
            else:
                A=[originx, originy + size]
                B=[originx + (size/2), originy - size]
                C=[originx - (size/2), originy - size]

        if (vely == 0 and velx > 0):
            A=[originx - size, originy]
            B=[originx + size, originy + (size/2)]
            C=[originx + size, originy - (size/2)]
        elif (vely == 0 and velx < 0):
            A=[originx + size, originy]
            B=[originx - size, originy + (size/2)]
            C=[originx - size, originy - (size/2)]
            
        pygame.draw.polygon(screen, (151,151,156), [(A[0],A[1]), (B[0],B[1]), (C[0],C[1])], 0)


    #def calcGrav(originx, originy, Space):
    #    space.Planest[0].coord
# Run the main function
main()