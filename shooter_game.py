from pygame import *
from random import randint
from time import time as timer

#parent class for other sprites
class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Call for the class (Sprite) constructor:
        super().__init__() #sprite.Sprite.__init__(self)
 
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

#child class for player
class Player(GameSprite):
    #method to control the sprite with arrow keys
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #method to shoot the bullet/launch the bullet
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

#child class for enemies
class Enemy (GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        #if you reach the edges of the window, enemies disappear
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width -80) #random x-coordinates
            missed = missed + 1

#child class for obstacle
class Obstacle (GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width -80) #random x-coordinates

#child class for bullet
class Bullet (GameSprite):
    def update(self):
        self.rect.y += self.speed
        #disappears upon touching the top edge
        if self.rect.y < 0:
            self.kill()

# Create variables
score = 0 #number of ships destroyed
missed = 0 #number of ships I failed to destroy
goal = 10
max_lost = 5 #max ships to be missed
lives = 3 #3 attempts at the game
life_color = (0, 0, 0)

#Fonts and captions
font.init()
displayText = font.Font("PoorStory-Regular.ttf", 36)

endText = font.Font('CaveatBrush-Regular.ttf', 80)
WIN = endText.render("You win!", True, (235, 52, 116))
LOSE = endText.render("You lose!", True, (250, 250, 50))

warningText = font.Font ("PoorStory-Regular.ttf", 56)
WARNING =   warningText.render("Reloading...", True, (255, 0, 0))

#we need the following images
img_bg ="galaxy.jpg" #background
img_hero = "rocket.png" #player
img_enemy = "ufo.png" #enemy
img_bullet = "bullet.png" #bullet
img_ast = "asteroid.png"

#window properties
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter game")
background = transform.scale(image.load(img_bg), (win_width, win_width))

#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

UFOs = sprite.Group()
for i in range(1, 6):
    ufo = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    UFOs.add(ufo)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Obstacle(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 3))
    asteroids.add(asteroid)

bullets = sprite.Group()

#background music
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg") #sound effect for bullet

#game loop
game = True #exit with "close window"
finish = False #end with win/lose
FPS = 60
clock = time.Clock()
rel_time = False #Is it time to reload the gun?
num_fire = 0 #counter for number of bullets shot

while game:
    #exit when "close window" is clicked
    for e in event.get():
        if e.type == QUIT:
            game = False
    #Event of pressing the spacebar - the player shoots
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #check how many shots have been fired and whether reload is in progress
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play() #sound effects for shooting
                    ship.fire()
                if num_fire >= 5 and rel_time == False: #if the player has shot 5 bullets
                    start_time = timer()
                    rel_time = True  
    #end the game when win/lose
    if not finish:
        #update the background
        window.blit(background, (0,0))

        #update the Player
        bullets.update()
        ship.update()
        ship.reset()
        #update the enemy
        UFOs.update()
        UFOs.draw(window)
        bullets.draw(window)
        #update the obstacles
        asteroids.update()
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer() #current time

            if now_time - start_time < 3:
                window.blit(WARNING, (260, 360))
            else:
                num_fire = 0 #reset the counter
                rel_time = False #reset the timer
                

        #checking for collision between enemies and bullets
        collides = sprite.groupcollide(UFOs, bullets, True, True)
        for c in collides: 
            score += 1
            ufo = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            UFOs.add(ufo)

        #checking for collision between enemies and player- each collision, reduce lives
        if sprite.spritecollide(ship, UFOs, False) or sprite.spritecollide(ship, asteroids, False):
            lives = lives - 1

        #losing condition
        if lives == 0 or missed >= max_lost:
            finish = True
            window.blit(LOSE, (200, 200))

        #checking for points scored? if 10, then win
        if score >= goal:
            finish = True
            window.blit(WIN, (200, 200))

        #set different color for number of lives
        if lives == 3:
            life_color = (173,255,47)
        if lives == 2: 
            life_color = (255,255,0)
        if lives == 1:
            life_color = (255, 0, 0)

        #write text on the screen
        LIVES = displayText.render(str(lives) + " lives", 1, life_color)
        window.blit(LIVES, (600, 10))

        SCORE = displayText.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(SCORE, (10, 10))

        MISSED = displayText.render("Missed: " + str(missed), 1, (255, 255, 255))
        window.blit(MISSED, (10, 40))

        #update the window
        display.update()
        clock.tick(FPS)


    #BONUS: automatic restart of the game
    else:
        finish = False
        score = 0
        missed = 0
        for b in bullets:
            b.kill()
        for e in UFOs:
            e.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)

        for i in range(1, 6):
            ufo = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            UFOs.add(ufo)
        
        for i in range(1, 2):
            asteroid = Obstacle(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 3))
            asteroids.add(asteroid)

    time.delay(10)
