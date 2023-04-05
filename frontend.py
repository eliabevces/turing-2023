# Example file showing a circle moving on screen
import pygame
from turing import TuringMachine
from machine import Machine

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
mac = Machine()
turingMac = TuringMachine(mac)
turingMac.tape.entrada = ['0','0','1']
width_center = screen.get_width() / 2
height_center = screen.get_height() / 2
player_pos =  pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

def drawTape():
    for i in range(len(turingMac.tape.entrada)):
        pygame.draw.polygon(screen, "white", (((20 + i*40)+player_pos.x, 350), ((60 + i*40)+player_pos.x, 350), ((60 + i*40)+player_pos.x, 250), ((20 + i*40)+player_pos.x, 250)))
        pygame.draw.line(screen, "black", ((20 + i*40)+player_pos.x, 250), ((20 + i*40)+player_pos.x, 350), 2)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(turingMac.tape.entrada[i], True, (0, 0, 0), (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = ((i*40)+player_pos.x, 300)
        screen.blit(text, textRect)



turingMac.runMachine(turingMac.tape.entrada)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    pygame.draw.polygon(screen, "purple", ((width_center, height_center), (width_center+50, height_center+50), (width_center-50, height_center+50)))
    pygame.draw.polygon(screen, "white", ((20, 350), (1240, 350), (1240, 250), (20,250))) #L_D , R_D, R_U, L_U
    drawTape()
   

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player_pos.x -= 40
        print(turingMac.tape.entrada)
    if keys[pygame.K_LEFT]:
        player_pos.x += 40

    # flip() the display to put your work on screen
    pygame.display.flip()


    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()

