import pygame
from pygame.locals import *
import sys
from states import MainMenu, Game, GameOver
from resources import load_resources, SCREEN_W, SCREEN_H, FPS

# Initialize pygame
pygame.init()

# Create window
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption('Dumpster Dash')

# Load all resources
resources = load_resources()

# Create game instance first
game = Game(resources)
# Create game states
main_menu = MainMenu(resources, game)
# Change this line where you create GameOver:
game_over = GameOver(resources, game)  # Instead of (resources, game.score, game.highest_score)

# Set starting game state
current_state = "MainMenu"

def switch_state(state):
    global current_state
    current_state = state

clock = pygame.time.Clock()

while True:
    # Draw scrolling background
    if resources['b_pos'] >= SCREEN_H:
        resources['b_pos'] = -SCREEN_H
    if resources['o_pos'] >= SCREEN_H:
        resources['o_pos'] = -SCREEN_H

    resources['b_pos'] += resources['speed']
    resources['o_pos'] += resources['speed']

    screen.blit(resources['bg_image'], (0, resources['b_pos']))
    screen.blit(resources['overlap_bg_image'], (0, resources['o_pos']))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if current_state == "MainMenu":
            main_menu.handle_events(event, switch_state)
        elif current_state == "Game":
            game.handle_events(event, switch_state)
        elif current_state == "GameOver":
            game_over.handle_events(event, switch_state)

    if current_state == "MainMenu":
        main_menu.update()
        main_menu.draw(screen)
    # In the main game loop, modify the Game state handling:
    elif current_state == "Game":
        game.update(switch_state)
        game.draw(screen)
    elif current_state == "GameOver":
        game_over.update()
        game_over.draw(screen)
        # Update the highest score from the current game
        game_over.highest_score = game.highest_score

    pygame.display.update()
    clock.tick(FPS)