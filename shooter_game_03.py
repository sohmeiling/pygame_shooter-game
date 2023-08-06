from pygame import *
from random import randint

# Window settings
width = 700
height = 500
window = display.set_mode((width, height))
display.set_caption("Shooter Game!")

# Background
background = transform.scale(image.load("galaxy.jpg"), (width, height))

# Set music
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

# Sound effects
fire_sound = mixer.Sound("fire.ogg")

# Set colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

# Set fonts
font.init()
font_counter = font.Font(None, 22) # This is for score and missed

font_win = font.Font(None, 80) # This is for win message
win_text = font_win.render("YOU WIN!", True, GREEN)
font_lose = font.Font(None, 80) # This is for lose message
lose_text = font_lose.render("YOU LOSE!", True, RED)

# Parent class
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Player class
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 10)
        bullets.add(bullet)

# Enemy class
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.y = 0
            self.rect.x = randint(80, width - 80)

# Bullet class
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

# Create variables
score = 0
missed = 0

# Create sprites
rocket = Player("rocket.png", 5, height - 100, 80, 100, 10)

ufos = sprite.Group()
for i in range(1, 6):
    ufo = Enemy("ufo.png", randint(80, width - 80), -40, 80, 50, randint(1, 5))
    ufos.add(ufo)

# Unlimited bullets
bullets = sprite.Group()

# Set game loop
game = True
finish = False
clock = time.Clock()
FPS = 60

while game:
    # Events
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()

    
    if not finish:
        window.blit(background, (0, 0))
        # Draw sprites
        rocket.reset()
        ufos.draw(window)
        bullets.draw(window)

        # Counter score
        text_counter = font_counter.render("Score: " + str(score), True, WHITE)
        window.blit(text_counter, (10, 10))
        text_missed = font_counter.render("Missed: " + str(missed), True, WHITE)
        window.blit(text_missed, (10, 35))

        # Move sprites
        rocket.update()
        ufos.update()
        bullets.update()

    # Update
    display.update()
    clock.tick(FPS)
