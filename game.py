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
opponentCarImage = pygame.image.load("images/opp.png")
bgImage = pygame.image.load("images/road.png")
start_menu = pygame.image.load('images/start_menu.png') 
game_over  = pygame.image.load('images/game_over.png') 
pause_menu = pygame.image.load('images/pause_menu.png')

# load music
menu_select = pygame.mixer.Sound('sounds/menu_select.wav')

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
        self.boost = 2

    def carPosition(self):
        gameDisplay.blit(carImage, (self.x, self.y))

    def collision(self):
        self.x_change = 0
        self.y_change = 0

    def press(self,key):
        if key == pygame.K_LEFT:
            self.x_change = -self.boost
        elif key == pygame.K_RIGHT:
            self.x_change = self.boost
        elif key == pygame.K_UP:
            self.y_change = -self.boost
        elif key == pygame.K_DOWN:
            self.y_change = self.boost

    def update(self):
        if self.rect.x <= 234.5 and self.x_change == -self.boost:
            self.x_change = 0
        elif self.rect.x >= 556 - car_width and self.x_change == self.boost:
            self.x_change = 0

        if self.rect.y <= 0  and self.y_change == -self.boost:
            self.y_change = 0
        elif self.rect.y > display_height - car_height   and self.y_change == self.boost:
            self.y_change = 0

        self.rect.x += self.x_change
        self.rect.y += self.y_change   

    def reset(self,key):
        if key == pygame.K_LEFT or key == pygame.K_RIGHT:
            self.x_change =0
        elif key == pygame.K_UP or key == pygame.K_DOWN:
            self.y_change =0    

class Health(pygame.sprite.Sprite):
    def __init__(self):
        pygame.font.init()
        pygame.sprite.Sprite.__init__(self)
        self.health = 100
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        self.image = self.myfont.render("End Game", 1, (255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 10

    def dec_health(self):
        self.health -= 1
        if self.health == 0:
            return True
        return False

    def update(self):
        self.image = self.myfont.render('Health: ' + str(self.health), 1, (255,0,0))

class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.font.init()
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        self.image = self.myfont.render("Score: 0", 1, (255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = 650
        self.rect.y = 10

    def inc_score(self):
        self.score += 1
    
    def update(self):
        self.image = self.myfont.render('Score: ' + str(self.score), 1, (255,0,0))
    
class OpponentCar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = random.choice((300,400,500))
        self.y = (-100)
        self.image = opponentCarImage
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed= random.choice((3,4,5,6,7,8))
        #gameDisplay.blit(carImage, ((self.x, self.y))

    def update(self):
        self.rect.move_ip(0,self.speed)
        #self.frame = self.frame + 1

def start_screen(): 
    pygame.event.clear()
    gameDisplay.blit(start_menu, (0, 0))
    pygame.display.update()
    pygame.mixer.music.load('sounds/excite_music.wav')
    pygame.mixer.music.play(-1)

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(menu_select)
            game_loop()
        else:
            continue
def gameover(score):
    pygame.event.clear()

    myfont = pygame.font.SysFont('Comic Sans MS', 100)
    img= myfont.render("Score "+str(score), 1, (255,0,0))
    rect = img.get_rect()

    gameDisplay.blit(game_over, (0, 0))
    gameDisplay.blit(img, (200, 300))
    pygame.display.update()
    pygame.mixer.music.load('sounds/excite_music.wav')
    pygame.mixer.music.play(-1)

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(menu_select)
            game_loop()
        else:
            continue


def game_loop():
    pygame.mixer.music.load('sounds/game_music.wav')
    pygame.mixer.music.play(-1)
    sprites = pygame.sprite.Group()
    player = Player()
    sprites.add(player)

    health = Health()
    sprites.add(health)

    score = Score()
    sprites.add(score)

    # Background scrolling variables.
    bgImage_y = display_height - bgImage.get_rect().height
    bgImage_dy = 10
    odd_dy = 500

    clock = pygame.time.Clock()
    gameExit = False
    odds = 60
    
    
    opps = pygame.sprite.Group()
    while not gameExit:
        
        if odds == 0:
            opp = OpponentCar()
            sprites.add(opp)
            opps.add(opp)
            odds = 60  
        else:
            odds-=1 
        
        collide_opponent = pygame.sprite.spritecollideany(player, opps)
        score.inc_score()

        if collide_opponent:
            killed = health.dec_health()
            if killed:
                gameover(score.score)
            player.collision()

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
        if odd_dy > 0:
            if bgImage_y == 0:
                bgImage_y =  display_height - bgImage.get_rect().height
            bgImage_y = bgImage_y + bgImage_dy
            odd_dy-=1
        else:
            odd_dy = 500  
            bgImage_dy+=3

        #print(bgImage_y)
        bgImage_y = bgImage_y % (display_height- bgImage.get_rect().height)
        gameDisplay.blit(bgImage, (0, bgImage_y))
        player.update()
    
        #player.carPosition()
        sprites.draw(gameDisplay)
        sprites.update()
        pygame.display.update()
        clock.tick(60)

start_screen()
pygame.quit()
quit()