import pygame, sys
pygame.init()
clock=pygame.time.Clock()
screen=pygame.display.set_mode((400,400))


while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            sys.exit() 
    screen.fill((0, 0, 0))


    clock.tick(60)
    pygame.display.update()
