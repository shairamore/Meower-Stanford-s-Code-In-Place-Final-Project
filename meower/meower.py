"""
In Meower, the main character is a cat whose goal is to
catch as many fishes as it could. The player should not
lose five lives or else the cat will get hungry and the
game will be over.

Created by Shaira Lapus // @ shairamore
20210527 6:00 PM
"""

import pygame
import random
import os
pygame.font.init()
pygame.mixer.init()

pygame.init()

# Create a window
WIDTH = 500
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meower by shairamore")
FONT_STYLE = pygame.font.SysFont("comicsans", 40)
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 100)
SUBSCRIPT = pygame.font.SysFont("comicsans", 50)
SMALL_FONT = pygame.font.SysFont("comicsans", 20)

# SOUND EFFECTS
MEOW_SOUND = pygame.mixer.Sound('Assets/audio/meow.mp3')
MEOW_SOUND.set_volume(0.4)
GAME_OVER_SOUND = pygame.mixer.Sound('Assets/audio/game over.mp3')
MISSED_SOUND = pygame.mixer.Sound('Assets/audio/missed.mp3')
BG_MUSIC = pygame.mixer.Sound('Assets/audio/background.mp3')

# SET CONSTANTS:
# background
WHITE = (255, 255, 255)
BACKGROUND = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'images', 'background.png')), (WIDTH, HEIGHT))
# speed / time
FPS = 60
VEL = 5
FISH_VEL = 2.5
HEART_VEL = 1.5
# load the cat
CAT_WIDTH = 50
CAT_HEIGHT = 50
CAT_IMAGE = pygame.image.load(os.path.join('Assets', 'images', 'cat.png'))
CAT_RIGHT = pygame.transform.scale(CAT_IMAGE, (CAT_WIDTH, CAT_HEIGHT))
CAT_LEFT = pygame.transform.flip(CAT_RIGHT, True, False)
# load the fish
FISH_WIDTH = 40
FISH_HEIGHT = 40
FISH_IMAGE = pygame.image.load(os.path.join('Assets', 'images', 'fish.png'))
FISH = pygame.transform.scale(FISH_IMAGE, (FISH_WIDTH, FISH_HEIGHT))
# load the heart
HEART_WIDTH = 20
HEART_HEIGHT = 20
HEART_IMAGE = pygame.image.load(os.path.join('Assets', 'images', 'heart.png'))
HEART = pygame.transform.scale(HEART_IMAGE, (HEART_WIDTH, HEART_HEIGHT))

FISH_CAUGHT = pygame.USEREVENT + 1
FISH_MISSED = pygame.USEREVENT + 2

# Check if the cat caught a fish
def check_catch(cat, fishes):
    for fish in fishes:
        if cat.colliderect(fish):
            pygame.event.post(pygame.event.Event(FISH_CAUGHT))
            fishes.remove(fish)
        elif fish.y > 400:
            pygame.event.post(pygame.event.Event(FISH_MISSED))
            fishes.remove(fish)

# Make the fishes fall from the top of the game window
def falling_fishes(fish):
    fish.move_ip(0, FISH_VEL)

# Make the cat move left or right
def cat_movement(cat_direction, cat):
    if cat_direction == 'right' and (cat.x + VEL) < (WIDTH - CAT_WIDTH):
        cat.x += VEL
    if cat_direction == 'left' and (cat.x - VEL) > 0:
        cat.x -= VEL

# Text shown if the user loses all five lives
def draw_game_over_screen(score):
    game_over_text = GAME_OVER_FONT.render("Game over!", 1, WHITE)
    WINDOW.blit(game_over_text, ((WIDTH / 2 - game_over_text.get_width() / 2), 80))
    subtext = SUBSCRIPT.render("Your score is " + str(score), 1, WHITE)
    WINDOW.blit(subtext, ((WIDTH / 2 - subtext.get_width() / 2), 150))
    play_again_text = SMALL_FONT.render("Press 'Enter' if you wish to play again", 1, WHITE)
    WINDOW.blit(play_again_text, ((WIDTH / 2 - play_again_text.get_width() / 2), 190))
    pygame.display.update()

# The screen where you play the game
def draw_window(cat, cat_direction, fishes, score, lives, heart):
    cat_image = CAT_RIGHT
    if cat_direction == 'left':
        cat_image = CAT_LEFT

    WINDOW.blit(BACKGROUND, (0, 0))
    score_text = FONT_STYLE.render("Score: " + str(score), 1, WHITE)
    lives_text = FONT_STYLE.render("Lives: " + str(lives), 1, WHITE)
    WINDOW.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    WINDOW.blit(lives_text, (10, 10))
    WINDOW.blit(cat_image, (cat.x, cat.y))
    if heart:
        WINDOW.blit(HEART, (heart.x, heart.y))
    for fish in fishes:
        WINDOW.blit(FISH, (fish.x, fish.y))

    pygame.display.update()

def main():
    # setting the size of the cat + making it movable
    cat = pygame.Rect(250 - (CAT_WIDTH/2), 375, CAT_WIDTH, CAT_HEIGHT)
    cat_direction_facing = 'right'
    cat_direction = 'right'
    fishes = []
    heart = None
    heart_countdown_ms = 0

    lives = 5
    score = 0
    countdown_before_next_fish_ms = 0
    clock = pygame.time.Clock()

    music = pygame.mixer.music.load(os.path.join('Assets', 'audio', 'background.mp3'))
    pygame.mixer.music.play(-1)

    running = True
    while running:
        milliseconds_elapsed = clock.tick(FPS)
        keys_pressed = pygame.key.get_pressed()
        # BG_MUSIC.play(-1)

        countdown_before_next_fish_ms -= milliseconds_elapsed
        heart_countdown_ms -= milliseconds_elapsed

        if countdown_before_next_fish_ms <= 0:
            fish = pygame.Rect(random.randint(0, (500 - FISH_WIDTH)), 0, FISH_WIDTH, FISH_HEIGHT)
            fishes.append(fish)
            speed_up_ms = min(score, 1000) # never exceeds 1000
            countdown_before_next_fish_ms = random.randint(1000 - speed_up_ms, 4000 - speed_up_ms * 4)

        if heart_countdown_ms <= 0:
            heart = None

        for fish in fishes:
            falling_fishes(fish)
        if heart:
            heart.move_ip(0, -HEART_VEL)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == FISH_CAUGHT:
                score += 10
                pygame.mixer.Sound.play(MEOW_SOUND)
                heart = pygame.Rect(cat.x + 15, cat.y - CAT_HEIGHT + 30, HEART_WIDTH, HEART_HEIGHT)
                heart_countdown_ms = 500
            elif event.type == FISH_MISSED:
                lives -= 1
                pygame.mixer.Sound.play(MISSED_SOUND)

        # Cat movement
        if keys_pressed[pygame.K_RIGHT]:
            cat_direction = 'right'
            cat_direction_facing = 'right'
        elif keys_pressed[pygame.K_LEFT]:
            cat_direction = 'left'
            cat_direction_facing = 'left'
        else:
            cat_direction = 'none'
        cat_movement(cat_direction, cat)
        check_catch(cat, fishes)

        draw_window(cat, cat_direction_facing, fishes, score, lives, heart)
        
        # Game over screen
        if lives <= 0:
            pygame.mixer.Sound.play(GAME_OVER_SOUND)
            draw_game_over_screen(score)

            show_game_over_screen = True
            while show_game_over_screen:
                pygame.time.delay(100)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        show_game_over_screen = False
                    if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN):
                        lives = 5
                        score = 0
                        fishes = []
                        heart = None
                        show_game_over_screen = False

    pygame.quit()


if __name__ == "__main__":
    main()
