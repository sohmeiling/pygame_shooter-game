#Create your own shooter

from pygame import *

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
        pass


#we need the following images:
img_bg = "galaxy.jpg" #game background
img_hero = "rocket.png" #hero

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

#game loop
game = True
finish = False
FPS = 60
clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        #update the background
        window.blit(background, (0,0))

        #launch sprite movements
        ship.update()

        #update them in a new location in each loop iteration
        ship.reset()

        display.update()
        clock.tick(FPS)

    #the loop is executed each 0.05 sec
    time.delay(50)