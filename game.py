import pygame
import enum
import random

pygame.init()

display_height = 600
display_width = 800
car_width = 56
car_height = 100
ROAD_RECT = (235,0,563,800)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')

# load images.
carImage = pygame.image.load('images/car.png')
bgImage = pygame.image.load("images/road.png")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = carImage
        self.x = (display_width * 0.45)
        self.y = (display_height * 0.8)
        self.x_change = 0
        self.y_change = 0
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def carPosition(self):
        gameDisplay.blit(carImage, (self.x, self.y))

    def press(self,key):
        if key == pygame.K_LEFT:
            self.x_change = -10
        elif key == pygame.K_RIGHT:
            self.x_change = 10
        elif key == pygame.K_UP:
            self.y_change = -10
        elif key == pygame.K_DOWN:
            self.y_change = 10

    def update(self):
        if self.rect.x <= 234.5 and self.x_change == -10:
            self.x_change = 0
        elif self.rect.x >= 556 - car_width and self.x_change == 10:
            self.x_change = 0

        if self.rect.y <= 0  and self.y_change == -10:
            self.y_change = 0
        elif self.rect.y > display_height - car_height   and self.y_change == 10:
            self.y_change = 0

        self.rect.x += self.x_change
        self.rect.y += self.y_change   

    def reset(self,key):
        if key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self.x_change =0
        elif key == pygame.K_UP or key == pygame.K_DOWN:
            self.y_change =0    

class OpponentCar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = random.choice((300,400,500))
        self.y = (-100)
        self.image = carImage
        #self.frame = 0
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed= random.choice((3,4,5,6,7,8))
        #gameDisplay.blit(carImage, ((self.x, self.y))

    def update(self):
        self.rect.move_ip(0,self.speed)
        #self.frame = self.frame + 1

def game_loop():

    
    sprites = pygame.sprite.Group()
    player = Player()
    sprites.add(player)

    # Background scrolling variables.
    bgImage_y = display_height - bgImage.get_rect().height
    bgImage_dy = 10

    clock = pygame.time.Clock()
    gameExit = False

    opps = pygame.sprite.Group()
    for i in range(4):
        opp = OpponentCar()
        sprites.add(opp)
        opps.add(opp)

    while not gameExit:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                player.press(event.key)
            if event.type == pygame.KEYUP:
                player.reset(event.key)
        
        
        
        # Scroll the background
        gameDisplay.fill((255,255,255))
        if bgImage_y == 0:
            bgImage_y =  display_height - bgImage.get_rect().height
        bgImage_y = bgImage_y + bgImage_dy

        #print(bgImage_y)
        bgImage_y = bgImage_y % (display_height- bgImage.get_rect().height)
        gameDisplay.blit(bgImage, (0, bgImage_y))
        player.update()
    
        #player.carPosition()
        sprites.draw(gameDisplay)
        sprites.update()
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
