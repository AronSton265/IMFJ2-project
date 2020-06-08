import pygame
import pygame.freetype
from space import *

# Define a main function, just to keep things nice and tidy
def main():

    # Initialize pygame, with the default parameters
    pygame.init()

    # Define the size/resolution of our window
    res = (640, 360)
    # Create a window and a display surface
    screen = pygame.display.set_mode(res)
    # Game loop, runs forever
    size = 2
    space = Space(size, screen)
    space.Background()
    while (True):
        pygame.time.delay(20)
        # Process OS events
        for event in pygame.event.get():
            # Checks if the user closed the window
            if (event.type == pygame.QUIT):
                # Exits the application immediately
                exit()

        # Clears the screen with a very dark blue (0, 0, 20)
        screen.fill((0,0,20))

        #space.Background(0,0,screen,2)
        space.Paint(screen, 0, 0)
        pygame.display.flip()

# Run the main function
main()