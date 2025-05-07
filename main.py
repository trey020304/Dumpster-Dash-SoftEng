import pygame
from pygame.locals import *
import sys
from states import MainMenu, Game, GameOver
from resources import load_resources, SCREEN_W, SCREEN_H, FPS

class GameApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption('Dumpster Dash')
        
        self.resources = load_resources()
        self.game = Game(self.resources)
        self.main_menu = MainMenu(self.resources, self.game)
        self.game_over = GameOver(self.resources, self.game)
        self.current_state = "MainMenu"
        self.clock = pygame.time.Clock()
        
    def switch_state(self, state):
        self.current_state = state
        
    def update_background(self):
        """Handle background scrolling logic"""
        for pos_key in ['b_pos', 'o_pos']:
            if self.resources[pos_key] >= SCREEN_H:
                self.resources[pos_key] = -SCREEN_H
            self.resources[pos_key] += self.resources['speed']
        
    def draw_background(self):
        """Draw the scrolling background"""
        self.screen.blit(self.resources['bg_image'], (0, self.resources['b_pos']))
        self.screen.blit(self.resources['overlap_bg_image'], (0, self.resources['o_pos']))
        
    def handle_events(self):
        """Process all pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Delegate event handling to current state
            if self.current_state == "MainMenu":
                self.main_menu.handle_events(event, self.switch_state)
            elif self.current_state == "Game":
                self.game.handle_events(event, self.switch_state)
            elif self.current_state == "GameOver":
                self.game_over.handle_events(event, self.switch_state)
                
    def update(self):
        """Update game state"""
        if self.current_state == "MainMenu":
            self.main_menu.update()
        elif self.current_state == "Game":
            self.game.update(self.switch_state)
        elif self.current_state == "GameOver":
            self.game_over.update()
            self.game_over.highest_score = self.game.highest_score
            
    def draw(self):
        """Draw current game state"""
        if self.current_state == "MainMenu":
            self.main_menu.draw(self.screen)
        elif self.current_state == "Game":
            self.game.draw(self.screen)
        elif self.current_state == "GameOver":
            self.game_over.draw(self.screen)
            
    def run(self):
        """Main game loop"""
        while True:
            self.update_background()
            self.draw_background()
            self.handle_events()
            self.update()
            self.draw()
            
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    app = GameApp()
    app.run()