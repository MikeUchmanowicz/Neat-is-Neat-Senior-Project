import pygame
import os
import random as rnd

#Load all class images. 
FISH_IMGS = [pygame.image.load(os.path.join("imgs", "fishup.png")), 
            pygame.image.load(os.path.join("imgs", "fishmid.png")), 
            pygame.image.load(os.path.join("imgs", "fishdown.png"))]
WORM_IMG = pygame.image.load(os.path.join("imgs", "worm.png"))
SHARK_IMG = pygame.image.load(os.path.join("imgs", "shark.png"))
FISHERMAN_IMG = pygame.image.load(os.path.join  ("imgs", "fisherman.png"))
BG_IMG = pygame.image.load(os.path.join  ("imgs", "background2.png"))

# initialize font and display for score and other stats
pygame.font.init()
STAT_FONT = pygame.font.SysFont("verdana", 50)

# class Fish: used by player or ai in python game.py
class Fish:
    IMGS = FISH_IMGS    
    
    # constructor
    def __init__(self, x:int, y:int):
        self.x=x
        self.y=y
        self.height = self.y
        self.tick_count = 0
        self.img = self.IMGS[0]
        self.img_count = 0
    
    # causes fish to "go up" when called
    def swimUp(self):
        None
        
    # causes fish to "fall down" due to gravity when called, this is perpetual.
    def move(self):
        None

    # Draws the fish on the screen
    def draw(self, win:pygame.display):
        win.blit(self.img, (self.x, self.height))
    
    # gets mask to later be used with collision detection        
    def get_mask(self):
        None

# class Worm: used by computer in python game.py
class Worm:
    VEL = 7.5
    
    # constructor
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.height = self.y
        self.img = WORM_IMG
    
    # causes worm to "go left" when called
    def move(self):
        self.x -= self.VEL
        
    # sets the height of the worm
    def set_Height(self):
        self.height=rnd.randrange(150, 650)
    
    # Draws the worm on the screen
    def draw(self, win:pygame.display):
        win.blit(self.img, (self.x, self.height))
    
    # determines collision with fish to be later used with collision detection
    def collide(self, Fish:Fish):
        None

class Fisherman:
    VEL = 7.5
    
    # constructor
    def __init__(self, x:int, y:int):
        self.x=x
        self.y=y
        self.height = self.y
        self.img = FISHERMAN_IMG
        
    # causes fisherman to "go left" when called
    def move(self):
        self.x -= self.VEL
        
    # sets the height of the fisherman
    def set_Height(self):
        self.height=rnd.randrange(150, 650)
    
    # Draws the fisherman on the screen
    def draw(self, win:pygame.display):
        win.blit(self.img, (self.x, self.height))
    
    # determines collision with fish to be later used with collision detection
    def collide(self, Fish:Fish):
        None
        
class Shark:
    VEL = 7.5
    
    # constructor
    def __init__(self, x:int, y:int):
        self.x=x
        self.y=y
        self.height = self.y
        self.img = SHARK_IMG
    
    # causes shark to "go left" when called
    def move(self):
        self.x -= self.VEL
    
    # sets the height of the shark
    def set_Height(self):
        self.height=rnd.randrange(150, 650)
    
    # Draws the shark on the screen
    def draw(self, win:pygame.display):
        win.blit(self.img, (self.x, self.height))
    
    # determines collision with fish to be later used with collision detection
    def collide(self, Fish:Fish):
        None

# Function Draw Window: used to place all class images onto the screen
def draw_window(win:pygame.display, fishes, sharks, fishermen, worms):
    # draw background
    win.blit(BG_IMG, (0,0))

    # draw all fishes, sharks, fishermen, and worms
    for fish in fishes:
        fish.draw(win)
    
    for shark in sharks:
        shark.draw(win)
        
    for fisherman in fishermen:
        fisherman.draw(win)
        
    for worm in worms:
        worm.draw(win)
        
    pygame.display.update()

# AI Stats to be uploaded with each iteration of the fitness function
class DataModel:
    gen:int = None
    popSize:int = None
    avgFit:float = None
    stdDevFit:float = None
    bestFit:float = None
    adjFit:float = None
    stag:int = None
    
    # constructor
    def __init__(self, gen, popSize, avgFit, stdDevFit, bestFit, adjFit, stag):
        self.gen = gen
        self.popSize = popSize
        self.avgFit = avgFit
        self.stdDevFit = stdDevFit
        self.bestFit = bestFit
        self.adjFit = adjFit
        self.stag = stag