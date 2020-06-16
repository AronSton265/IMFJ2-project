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
    my_font = pygame.freetype.Font("NotoSans-Regular.ttf", 24)
    # Game loop, runs forever
    crashed = False
    size = 3
    sizeShip = 20
    mov = 0.25
    rot= 0.05
    speed = 0
    vel = [0,0]
    velang = 0
    tempvelx = 0
    tempvely = 0
    maxspead = 20
    maxvelang = 5*math.pi
    densidade = 120
    correntcoord = [0,0]
    front = [0,sizeShip]
    densplaneta = 2700
    constgrav = 0.00000006
    space = Space(size, screen, res, densidade)
    space.Background()
    space.createPlanets()
    space.createSuns()
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
            velang -= rot
        if (keys[pygame.K_d]):
            velang += rot
        if (keys[pygame.K_s]):
            speed=speed-mov
        if (keys[pygame.K_w]):
            speed=speed+mov        
        
        if (velang > maxvelang):
            velang = maxvelang
        elif (velang < -maxvelang):
            velang = -maxvelang
        if (speed > maxspead):
            speed = maxspead
        elif (speed < -maxspead):
            speed = -maxspead

        front = rotateShip(front, velang, sizeShip)
        vel = calcVel(front, speed, vel)

        if (vel[0] > maxspead):
            vel[0] = maxspead
        elif (vel[0] < -maxspead):
            vel[0] = -maxspead
        if (vel[1] > maxspead):
            vel[1] = maxspead
        elif (vel[1] < -maxspead):
            vel[1] = -maxspead

        Gravidade = aplayGrav(res[0]/2, res[1]/2, size, densplaneta, constgrav, space)


        if (correntcoord[0] - vel[0] - int(Gravidade[0]) < (size-1)*res[0]  and  correntcoord[0] - vel[0] - int(Gravidade[0]) > -(size-1)*res[0]):
            tempvelx = int(vel[0])-int(Gravidade[0])
        else:
            tempvelx = 0

        if (correntcoord[1] - vel[1] - int(Gravidade[1]) < (size-1)*res[1]  and  correntcoord[1] - vel[1] - int(Gravidade[1]) > -(size-1)*res[1]):
            tempvely = int(vel[1])-int(Gravidade[1])
        else:
            tempvely = 0

        correntcoord[0] = correntcoord[0] - vel[0] - int(Gravidade[0])
        correntcoord[1] = correntcoord[1] - vel[1] - int(Gravidade[1])

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0,0,20))
        if (space.checkifInside(space.Planets, space.planetnumb, [res[0]/2, res[1]/2]) or space.checkifInside(space.Suns, space.sunnumb, [res[0]/2, res[1]/2])):
            tempvelx= 0
            tempvely= 0
            crashed = True 

        space.Paint(screen, tempvelx, tempvely)
        createShip(res[0]/2, res[1]/2, sizeShip, screen, front)
        if crashed: my_font.render_to(screen, (150, 150), "You crashed", (255, 0, 0),  None, pygame.freetype.STYLE_DEFAULT, 0, 100)
        #pygame.draw.circle(screen, (245,0,0), (200, 200), 40, 0)
        #planet 20min max 100
        #sun 150min 300max
        #black hole 10min 40max
        pygame.display.flip()

#rodar a nave
#depois de alguns teste descobri que o vetor ia ficando cada vez mais pequeno emtao para que isso nao aconteca torno o vetor num unitario e multiplicou pelo tamanho original
def rotateShip(vector, w, lenght):
    x = math.cos(w*0.2)*vector[0] - math.sin(w*0.2)*vector[1]
    y = math.sin(w*0.2)*vector[0] + math.cos(w*0.2)*vector[1]
    magnitude = math.sqrt(x**2 + y**2)
    vector[0] = lenght * (x/magnitude)
    vector[1] = lenght * (y/magnitude)
    return vector

def calcVel(vector, acelaracao, velocidade):
    velocidade[0] = acelaracao * (vector[0]/math.sqrt(vector[0]**2 + vector[1]**2))
    velocidade[1] = acelaracao * (vector[1]/math.sqrt(vector[0]**2 + vector[1]**2))
    return velocidade

#desenhar a nave
def createShip(originx, originy, size, screen, front):
    perp=calcVecPerp(front, size/2)

    A= [0,0]
    A[0] = originx - front[0]
    A[1] = originy - front[1]

    B= [0,0]
    B[0] = originx + front[0] + perp[0]
    B[1] = originy + front[1] + perp[1]

    C= [0,0]
    C[0] = originx + front[0] - perp[0]
    C[1] = originy + front[1] - perp[1]
  
    pygame.draw.polygon(screen, (151,151,156), [(A[0],A[1]), (B[0],B[1]), (C[0],C[1])], 0)

def calcVecPerp(vector, lenght):
    x=-1
    y=vector[0]/vector[1]
    magnitude = math.sqrt(x**2 + y**2)
    newx = lenght * (x/magnitude)
    newy = lenght * (y/magnitude)
    return [newx, newy]

#calculos da gravidade
def aplayGrav(originx, originy, size, densidade, constGravitacional, space):
    i=0
    G=[0,0]
    for i in range(space.planetnumb):
        temp = calcGrav(originx, originy, size, densidade, space.Planets[i], constGravitacional)
        G[0] += temp[0]
        G[1] += temp[1]
    i=0
    for i in range(space.sunnumb):
        temp = calcGrav(originx, originy, size, densidade*1.5, space.Suns[i], constGravitacional)
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