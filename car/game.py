import pygame
import enum

pygame.init()

display_height = 600
display_width = 800
car_width = 150
car_heigth = 109

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
carImage = pygame.image.load('car.png')

class X_Direction(enum.Enum):
    STATIC = 0
    LEFT = 1
    RIGHT = 2


def car(x, y):
    gameDisplay.blit(carImage, (x, y))


def game_loop():

    black = (0, 0, 0)
    white = (255, 255, 255)
    x = (display_width * 0.45)
    y = (display_height * 0.8)
    x_change = 0

    clock = pygame.time.Clock()
    gameExit = False
    change_key = False
    moving_direction = X_Direction.STATIC


    while not gameExit:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -10
                    change_key = True
                elif event.key == pygame.K_RIGHT:
                    x_change = 10
                    change_key = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                    x_change = 0
        
        if x == 0 and x_change == -10:
            x_change = 0
        elif x == x == display_width - car_width and x_change == 10:
            x_change = 0

        x += x_change
        gameDisplay.fill(white)
        car(x, y)
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
