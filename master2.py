import pygame
import pygame.freetype
import math
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
    rot= 0.1
    speed = 0
    vel = [0,0]
    velang = 0
    tempvelx = 0
    tempvely = 0
    maxspead = 10
    maxvelang = 10*math.pi
    densidade = 120
    correntcoord = [0,0]
    front = [0,size]
    densplaneta = 2700
    constgrav = 0.00000006
    #maxcoord = [((size+1)*res[0])/2,(size+1)*res[1]]
    space = Space(size, screen, res, densidade)
    space.Background()
    space.createPlanets()
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
            #velx=velx+mov
            velang -= rot
            print("to the left")
        if (keys[pygame.K_d]):
            #velx=velx-mov
            velang += rot
            print("to the right")
        if (keys[pygame.K_s]):
            speed=speed-mov
            print("back")
        if (keys[pygame.K_w]):
            speed=speed+mov        
            print("foward")
        
        if (velang > maxvelang):
            velang = maxvelang
            print("slow down")
        elif (velang < -maxvelang):
            velang = -maxvelang
            print("slow down")

        print(velang*0.2)
        front = rotateShip(front, velang)
        vel = calcVel(front, speed, vel)
        print(velang)

        if (vel[0] > maxspead):
            vel[0] = maxspead
            print("slow down")
        elif (vel[0] < -maxspead):
            vel[0] = -maxspead
            print("slow down")
        if (vel[1] > maxspead):
            vel[1] = maxspead
            print("slow down")
        elif (vel[1] < -maxspead):
            vel[1] = -maxspead
            print("slow down")

        print(vel)

        #Gravidade = aplayGrav(res[0]/2, res[1]/2, size, densplaneta, constgrav, space)

        correntcoord[0] = correntcoord[0] - vel[0]
        correntcoord[1] = correntcoord[1] - vel[1]

        if (correntcoord[0] < (size-1)*res[0]  and  correntcoord[0] > -(size-1)*res[0]):
            tempvelx = int(vel[0])
        else:
            tempvelx = 0

        if (correntcoord[1] < (size-1)*res[1]  and  correntcoord[1] > -(size-1)*res[1]):
            tempvely = int(vel[1])
        else:
            tempvely = 0

        #tempvelx -= int(Gravidade[0])
        #tempvely -= int(Gravidade[1])

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0,0,20))
        if space.checkifInside(space.Planets, space.planetnumb, [res[0]/2, res[1]/2]):
            tempvelx= 0
            tempvely= 0

        space.Paint(screen, tempvelx, tempvely)
        createShip(res[0]/2, res[1]/2, 20, screen, tempvelx, tempvely)
        #pygame.draw.circle(screen, (245,0,0), (200, 200), 40, 0)
        #planet 20min max 100
        #sun 150min 300max
        #black hole 10min 40max
        pygame.display.flip()

def rotateShip(vector, w):
    vector[0] = math.cos(w*0.2)*vector[0] - math.sin(w*0.2)*vector[1]
    vector[1] = math.sin(w*0.2)*vector[0] + math.cos(w*0.2)*vector[1]
    return vector

def calcVel(vector, acelaracao, velocidade):
    velocidade[0] += acelaracao * (vector[0]/math.sqrt(vector[0]**2 + vector[1]**2))
    velocidade[1] += acelaracao * (vector[1]/math.sqrt(vector[0]**2 + vector[1]**2))
    return velocidade

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

def aplayGrav(originx, originy, size, densidade, constGravitacional, space):
    i=0
    G=[0,0]
    for i in range(space.planetnumb):
        temp = calcGrav(originx, originy, size, densidade, space.Planets[i], constGravitacional)
        G[0] += temp[0]
        G[1] += temp[1]
    return G

def calcGrav(originx, originy, size, densidade, planet, constGravitacional):
    dis = math.sqrt( (originx-planet.coord[0])**2 + (originy-planet.coord[1])**2 )
    f = constGravitacional*( massCirc(planet.size, densidade)*(((size**2)-((size-1)**2))*7874 )/(dis**2) )
    F = [f*(planet.coord[0]-originx)/(math.sqrt((planet.coord[0]-originx)**2 + (planet.coord[1]-originy)**2 )) , f*(planet.coord[1]-originy)/(math.sqrt((planet.coord[0]-originx)**2 + (planet.coord[1]-originy)**2 ))]
    return F

def massCirc(raio, densidade):
    return areaCirc(raio)*densidade

def areaCirc(raio):
    return (raio**2)*math.pi

# Run the main function
main()