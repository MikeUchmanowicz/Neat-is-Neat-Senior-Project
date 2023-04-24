import pygame
import os
import neat
import math

# set window size and title
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
TITLE = "Swim, Fish, Swim!"


# initialize font and display for score and other stats
pygame.font.init()
STAT_FONT = pygame.font.SysFont("verdana", 25)

# Function Draw Window: used to place all class images onto the screen
def draw_gameWindow(win:pygame.display, background, fishes, sharks, fishermen, worms, stats):
    
    # draw background
    background.draw(win)

    # for each stat, draw the stat and its value
    for key, value in stats.items():
        text = STAT_FONT.render(key + ": " + str(round(value, 3)), 1, (0,0,0))
        win.blit(text, (10, 10 + text.get_height()*list(stats.keys()).index(key)))

    # draw all fishes, sharks, fishermen, and worms
    for fish in fishes:
        fish.draw(win)
    
    for shark in sharks:
        shark.draw(win)
        
    for fisherman in fishermen:
        fisherman.draw(win)
        
    for worm in worms:
        worm.draw(win)
        
    # update the display
    pygame.display.update()
    
# draw background, used by title screen and game over screen
def draw_background(win:pygame.display, background):
    # draw background
    background.draw(win)
    # update the display
    pygame.display.update()