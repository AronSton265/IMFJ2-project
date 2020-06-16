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

    coord =[res[0]/2, res[1]/2]
    correntcoord = [0,0]
    crashed = False
    #size of the space
    size = 2
    #size of the ship , player
    sizeShip = 20
    #acceleration
    mov = 0.25
    #angular acceleration
    rot= 0.05
    #velocity
    speed = 0
    #vector velocity
    vel = [0,0]
    #angular velocity
    velang = 0
    tempvelx = 0
    tempvely = 0
    maxspead = 20
    maxvelang = 5*math.pi
    #densety of start/planets, the bigger more stars7planets
    densidade = 120
    #vector that point to the front of the ship
    front = [0,sizeShip]
    #densety of a plante, the bigger more gravaty will the planet have
    densplaneta = 2700
    #constant for the gravaty calcolations
    constgrav = 0.00000006
    #--creation of the object space--
    space = Space(size, screen, res, densidade)
    space.Background()
    space.createPlanets()
    #--------------------------------
    # Game loop, runs forever
    while (True):
        pygame.time.delay(10)
        # Process OS events
        for event in pygame.event.get():
            # Checks if the user closed the window
            if (event.type == pygame.QUIT):
                # Exits the application immediately
                exit()
        #--controlss--
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a]):
            velang -= rot
        if (keys[pygame.K_d]):
            velang += rot
        if (keys[pygame.K_s]):
            speed=speed-mov
        if (keys[pygame.K_w]):
            speed=speed+mov  
        #-------------     
        
        #verefys if the speeds(normal and angular)are above the max, if so froces them to be equal max
        if (velang > maxvelang):
            velang = maxvelang
        elif (velang < -maxvelang):
            velang = -maxvelang

        if (speed > maxspead):
            speed = maxspead
        elif (speed < -maxspead):
            speed = -maxspead
        #----------------------------------------------------------------------------------------------
        
        #rotates the vector front
        front = rotateShip(front, velang, sizeShip)
        #aplays a force with the value of speed and the direction of the vector front
        vel = calcVel(front, speed, vel) 

        #calculates the gravaty of all the planest in the object space
        Gravidade = aplayGrav(res[0]/2, res[1]/2, size, densplaneta, constgrav, space)


        #--checks if the ship will leave the player area, if so the speed will became 0--
        correntcoord[0] = coord[0] - vel[0]
        correntcoord[1] = coord[1] - vel[1]

        if (coord[0] - vel[0] < (size-1)*res[0]  and  coord[0] - vel[0] > 0):
            tempvelx = int(vel[0])
        else:
            tempvelx = 0
        if (coord[1] - vel[1] < (size-1)*res[1]  and  coord[1] - vel[1] > 0):
            tempvely = int(vel[1])
        else:
            tempvely = 0
        #---------------------------------------------------------------------------------

        #aplays the gravaty to the force that will be aplyed to the ship
        tempvelx -= int(Gravidade[0])
        tempvely -= int(Gravidade[1])

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0,0,20))
        #checks if the shipis inside of another planet/sun
        if space.checkifInside(space.Planets, space.planetnumb, [coord[0], coord[1]]):
            tempvelx= 0
            tempvely= 0
            crashed = True 

        #--paints every ogject--
        #paints the space object with tthe velocity of 0 so it satys still
        space.Paint(screen, 0, 0)
        #so the velocity is aplied to the coordenates of the ship so it moves, in main2 its the oposite
        coord[0] -= tempvelx
        coord[1] -= tempvely
        createShip(coord[0], coord[1], sizeShip, screen, front)
        if crashed: my_font.render_to(screen, (150, 150), "You crashed", (255, 0, 0),  None, pygame.freetype.STYLE_DEFAULT, 0, 100)
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
    #velocidade=A*(x/|vector|)
    velocidade[0] = acelaracao * (vector[0]/math.sqrt(vector[0]**2 + vector[1]**2))
    velocidade[1] = acelaracao * (vector[1]/math.sqrt(vector[0]**2 + vector[1]**2))
    return velocidade

#desenhar a nave
def createShip(originx, originy, size, screen, front):
    #finds a vector perpendicular to front and with half its size
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