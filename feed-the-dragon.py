import random

import pygame

# Initialize Pygame
pygame.init()

# Set display surface
WINDOW_WIDTH, WINDOW_HEIGTH = 1000, 400
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGTH))
pygame.display.set_caption("Feed the dragon!")

# Set colors
FILLCOLOR = (32, 52, 71)
GREEN = (0, 255, 0)
DARKGREEN = (10, 55, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set FPS and clock
FPS = 100
clock = pygame.time.Clock()

# Set game values
PLAYER_VELOCITY = 5
PLAYER_STARTING_LIVES = 5
COIN_STARTING_VELOCITY = 5
COIN_ACCELERATION = .5
BUFFER_DISTANCE = 100

score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

# Set sounds and music
coin_sound = pygame.mixer.Sound('sounds/coin_sound.wav')
miss_sound = pygame.mixer.Sound('sounds/miss_sound.wav')
miss_sound.set_volume(.1)
pygame.mixer.music.load('sounds/ftd_background_music.wav')

# Set fonts
font = pygame.font.Font('AttackGraffiti.ttf', 32)

# Define text
score_text = font.render("Score: " + str(score), True, GREEN, DARKGREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

title_text = font.render("Feed the dragon!", True, GREEN)
title_rect = title_text.get_rect()
title_rect.centerx = (WINDOW_WIDTH // 2)
title_rect.y = (10)

lives_text = font.render("Lives: " + str(player_lives), True, GREEN, DARKGREEN)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

game_over_text = font.render("GAME OVER!", True, GREEN, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGTH // 2)

continue_text = font.render("Press any key to try again!", True, GREEN, DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGTH // 2 + 15)

boom_text = font.render("boom!", True, GREEN, DARKGREEN)
boom_rect = boom_text.get_rect()
boom_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGTH // 2)

# Set images
player_image = pygame.image.load("img/dragon_right.png")
player_rect = player_image.get_rect()
player_rect.topleft = (10, WINDOW_HEIGTH // 2)

coin_img = pygame.image.load("img/coin.png")
coin_rect = coin_img.get_rect()
coin_rect.x = (WINDOW_WIDTH + BUFFER_DISTANCE)
coin_rect.y = random.randint(64, WINDOW_HEIGTH - 32)

# The main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    # Check to see if user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Check players wants to ove
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_rect.top > 64:
        player_rect.y -= PLAYER_VELOCITY
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_rect.bottom < WINDOW_HEIGTH:
        player_rect.y += PLAYER_VELOCITY

    # Move the coin
    if coin_rect.x < 0:
        # Player missed the coin
        player_lives -= 1
        miss_sound.play()
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGTH - 32)
    else:
        #Move the coin
        coin_rect.x -= coin_velocity

    # Check for collision between two rects
    if player_rect.colliderect(coin_rect):
        coin_sound.play()
        score += 1
        coin_velocity += COIN_ACCELERATION
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGTH - 32)
        display_surface.blit(boom_text, boom_rect)
        pygame.display.update()

    # Update HUD
    score_text = font.render("Score: " + str(score), True, GREEN, DARKGREEN)
    lives_text = font.render("Lives: " + str(player_lives), True, GREEN, DARKGREEN)

    # Check game over condition
    if player_lives == 0:
        display_surface.blit(game_over_text, game_over_rect)
        pygame.display.update()
        pygame.time.delay(3000)
        display_surface.fill(FILLCOLOR)

        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        #Pause the game until reset the game
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                # Quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False
                # Play again
                if event.type == pygame.KEYDOWN:
                    score = 0
                    pygame.mixer.music.play(-1, 0.0)
                    player_lives = PLAYER_STARTING_LIVES
                    player_rect.y = WINDOW_HEIGTH//2
                    coin_velocity = COIN_STARTING_VELOCITY
                    is_paused = False



    # Fill the display surface to cover old images
    display_surface.fill(FILLCOLOR)

    # Blit assets to screen + HUD
    display_surface.blit(player_image, player_rect)
    display_surface.blit(coin_img, coin_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text, lives_rect)
    pygame.draw.line(display_surface, WHITE, (0, 64), (WINDOW_WIDTH, 64), 2)

    # Update display
    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()
