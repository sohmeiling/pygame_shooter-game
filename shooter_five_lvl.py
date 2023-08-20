# Modifications for Louis (Adding 10 levels to the game)

from pygame import *
from random import randint
from time import time as timer  

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

font_main = font.Font(None, 80) # This is for main menu

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
        global missed
        if self.rect.y > height:
            self.rect.y = 0
            self.rect.x = randint(80, width - 80)
            missed += 1

# Bullet class
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

# Create variables
score = 0 # How many ufos you hit
missed = 0 # How many ufos you missed
goal = 10 # How many ufos you need to hit to win
max_missed = 1000 # How many ufos you can miss before you lose
lives = 3 # How many lives you have
current_level = 0 # What level you are on

# Limited bullets
num_fire = 0
max_fire = 20

# Create sprites
rocket = Player("rocket.png", 5, height - 100, 80, 100, 10)

ufos = sprite.Group()
for i in range(1, 6): 
    ufo = Enemy("ufo.png", randint(80, width - 80), -40, 80, 50, randint(1,5))
    ufos.add(ufo)

# Unlimited bullets
bullets = sprite.Group()

# Set game loop
game = True
start = False # This is to keep track of whether the game is started or not (press s to start)
finish = False
game_won = False # This is to keep track of whether the game is won or not
clock = time.Clock()
FPS = 60

# Add levels
levels = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5']
# Define the goals for each level
level_goals = [10, 20, 30, 40, 50]

# Set initial goal using the level_goals list
goal = level_goals[current_level]

while game:
    events = event.get()  # Store events obtained from event.get()

    # Events
    for e in events:
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                rocket.fire()
            elif e.key == K_s:
                if not start:
                    start = True
                    mixer.music.play()
                elif game_won:  # Restart the game if 's' is pressed after winning
                    # Reset game state
                    current_level = 0
                    goal = level_goals[current_level]
                    score = 0
                    missed = 0
                    game_won = False

                    for ufo in ufos:
                        ufo.kill()
                    for bullet in bullets:
                        bullet.kill()

                    rocket.rect.x = window.get_width() // 2 - rocket.rect.width // 2
                    rocket.rect.y = height - 100
                    ufos.add(Enemy("ufo.png", randint(80, width - 80), -40, 80, 50, randint(1, 5)))

    if not finish:
        window.blit(background, (0, 0))
        # Counter score
        text_counter = font_counter.render("Score: " + str(score), True, WHITE)
        window.blit(text_counter, (10, 10))
        text_missed = font_counter.render("Missed: " + str(missed), True, WHITE)
        window.blit(text_missed, (10, 35))

        # Text for current level
        if current_level < len(levels):
            text_level = font_counter.render(levels[current_level], True, WHITE)
            window.blit(text_level, (width // 2 - text_level.get_width() // 2, 10))

        # Start the game
        if not start:
            text_start = font_win.render("Press s to start", True, WHITE)
            window.blit(text_start, (width // 2 - text_start.get_width() // 2, height // 2 - text_start.get_height() // 2))
            display.update()  # Add this line to update the display

         # Add UFO update logic here to start when 's' key is pressed
        if start:
            # Draw sprites
            rocket.reset()
            ufos.draw(window)
            bullets.draw(window)

            # Check if the player has won the game
            if current_level < len(level_goals) and score >= goal and not game_won:
                # Display "Level Cleared" text for 3 seconds
                if current_level < len(levels) - 1:  # For levels 1 to 4
                    text_cleared = font_main.render("Level Cleared!", True, GREEN)
                else:  # For level 5
                    text_cleared = font_main.render("You Win!", True, GREEN)

                text_cleared_rect = text_cleared.get_rect(center=(width // 2, height // 2))
                window.blit(text_cleared, text_cleared_rect)
                display.update()

                # Wait for 3 seconds
                start_time = time.get_ticks()
                while time.get_ticks() - start_time < 3000:
                    display.update()

                # Reset the score to 0 and reset UFOs
                score = 0
                for ufo in ufos:
                    ufo.kill()
                for i in range(1, 6):
                    ufo = Enemy("ufo.png", randint(80, width - 80), -40, 80, 50, randint(1, 5))
                    ufos.add(ufo)

                # Move to the next level
                current_level += 1
                if current_level < len(levels):
                    goal = level_goals[current_level]
                    text_level = font_counter.render(levels[current_level], True, WHITE)
                    window.blit(text_level, (width // 2 - text_level.get_width() // 2, 10))
                else:
                    game_won = True  # Set game won state to True

            # Check collisions
            collides = sprite.groupcollide(ufos, bullets, True, True)
            for c in collides:
                score += 1
                ufo = Enemy("ufo.png", randint(80, width - 80), -40, 80, 50, randint(1,5))
                ufos.add(ufo)

            # # Check lose
            # if sprite.spritecollide(rocket, ufos, False) or missed >= max_missed:
            #     finish = True
            #     game_won = False
            #     window.blit(lose_text, (width // 2 - lose_text.get_width() // 2, height // 2 - lose_text.get_height() // 2))

            # Check if all levels are cleared and win the game
            if current_level >= len(levels):
                finish = True
                game_won = True

            # Move sprites
            rocket.update()
            ufos.update()
            bullets.update()

    #bonus: automatic restart to level 1 if game_won is True
    #bonus: automatic restart to current level if game_won is False
    else:
        # Reset the game state after 5 seconds
        start_time = time.get_ticks()  # Assign the start time before entering the loop
        while time.get_ticks() - start_time < 5000:  # Check if 5 seconds have passed
            display.update()

        if game_won:
            # Reset game state for winning
            current_level = 0
            goal = level_goals[current_level]
        else:
            # Reset game state for losing
            goal = level_goals[current_level]

        score = 0
        missed = 0
        game_won = False
        finish = False

        for ufo in ufos:
            ufo.kill()
        for bullet in bullets:
            bullet.kill()

        rocket.rect.x = window.get_width() // 2 - rocket.rect.width // 2
        rocket.rect.y = height - 100
        ufos.add(Enemy("ufo.png", randint(80, width - 80), -40, 80, 50, randint(1, 5)))

        display.update()

    # Update
    display.update()
    clock.tick(FPS)

quit()
