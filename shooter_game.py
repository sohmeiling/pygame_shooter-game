#Create your own shooter

from pygame import *
from random import randint

#parent class for other sprites
class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Call for the class (Sprite) constructor:
        sprite.Sprite.__init__(self)
 
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    #method drawing the character on the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#main player class
class Player(GameSprite):
    #method to control the sprite with arrow keys
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    #method to "shoot" (use the player position to create a bullet there)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet) 

#child class for enemy
class Enemy (GameSprite):
    #movemement method for the UFO
    def update(self):
        self.rect.y +=self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width -80)
            self.rect.y = 0
            lost = lost + 1
            
#child class for bullets
class Bullet(GameSprite):
    #enemy movement
    def update(self):
        self.rect.y += self.speed
        #disappears upon reaching the screen edge
        if self.rect.y < 0:
            self.kill()

#variables
score = 0 #tally of ships destroyed
lost = 0 #tally of ships that we missed
goal= 10 #number of ships to shoot down to win
max_lost = 3 #lose if we lose 3 ships

#fonts and captions
font.init()
displayText = font.Font(None, 36) #Varriable texts

endText = font.Font(None, 80) #win/lose texts
win = endText.render("YOU WIN!", True, (252, 244, 3))
lose = endText.render("YOU LOSE!", True, (196, 16, 31))           
            
#we need the following images:
img_bg = "space.jpg" #game background
img_hero = "rocket.png" #hero
img_enemy = "ufo.png" #enemy
img_bullet = "bullet.png" #bullet

#window properties
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_bg), (win_width, win_height))

#background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg') #sound effects

#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

UFOs = sprite.Group()
for i in range(1, 6):
    ufo = Enemy(img_enemy, randint(80, win_width -80), -40, 80, 50, randint(1, 5))
    UFOs.add(ufo)

#create Bullet sprites
bullets = sprite.Group()

#game loop
game = True
finish = False
FPS = 60
clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        #event of pressing the spacebar - the sprite shoots
        elif e.type == KEYDOWN:
            fire_sound.play()
            ship.fire() 

    if not finish:
        #update the background
        window.blit(background, (0,0))

        #launch sprite movements
        ship.update()
        ship.reset()

        #enemies falling down
        UFOs.update()
        UFOs.draw(window)

        #launch bullets
        bullets.update()
        bullets.draw(window)

        #write text on the screen
        SCORE = displayText.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(SCORE, (10,20))

        MISSED = displayText.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(MISSED, (10, 50))

        #check for collision
        collides = sprite.groupcollide(UFOs, bullets, True, True)

        display.update()
        clock.tick(FPS)
        
    #the loop is executed each 0.05 sec
    time.delay(50)
