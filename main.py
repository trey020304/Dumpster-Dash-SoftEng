import pygame
from pygame.locals import *
import sys
from states import MainMenu, Game, GameOver, Leaderboard
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

# Create all game states
main_menu = MainMenu(resources, game)
game_over = GameOver(resources, game)
leaderboard = Leaderboard(resources, game)

# Dictionary to manage all states
states = {
    "MainMenu": main_menu,
    "Game": game,
    "GameOver": game_over,
    "Leaderboard": leaderboard
}

# Set starting game state
current_state = "MainMenu"

def switch_state(state):
    global current_state
    print(f"Switching state from {current_state} to {state}")  # Debug print
    current_state = state

clock = pygame.time.Clock()

# Main game loop
while True:
    # Handle background scrolling
    scroll_speed = 0
    
    if current_state == "MainMenu" or current_state == "Leaderboard":
        scroll_speed = resources['menu_speed']
    elif current_state == "Game" and not game.dead:
        scroll_speed = game.speed
    
    # Update scroll position (using modulo for seamless wrapping)
    resources['scroll_pos'] = (resources['scroll_pos'] + scroll_speed) % resources['bg_height']
    
    # Draw the background - two copies for seamless scrolling
    screen.blit(resources['bg_image'], (0, resources['scroll_pos'] - resources['bg_height']))
    screen.blit(resources['bg_image'], (0, resources['scroll_pos']))
    
    # If your background is smaller than screen height, draw a third copy
    if resources['bg_height'] < SCREEN_H:
        screen.blit(resources['bg_image'], (0, resources['scroll_pos'] + resources['bg_height']))
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Pass events to the current state
        if current_state in states:
            states[current_state].handle_events(event, switch_state)
    
    # Update and draw current state
    if current_state in states:
        if current_state == "Game":
            states[current_state].update(switch_state)  # Pass switch_state for Game
        else:
            states[current_state].update()  # Other states don't need it
        states[current_state].draw(screen)
    
    pygame.display.update()
    clock.tick(FPS)