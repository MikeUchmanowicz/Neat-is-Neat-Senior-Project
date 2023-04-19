import pygame
import os
import random as rnd

# set window size and title
WINDOW_WIDTH:int = 640
WINDOW_HEIGHT:int = 480

#Load all class images. 
FISH_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "fishup.png")), (49, 38)),
            pygame.transform.scale(pygame.image.load(os.path.join("imgs", "fishmid.png")), (49, 38)), 
            pygame.transform.scale(pygame.image.load(os.path.join("imgs", "fishdown.png")), (49, 38))]

SHARK_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "shark.png")), (170, 78)),
            pygame.transform.scale(pygame.image.load(os.path.join("imgs", "shark2.png")), (170, 78))]
WORM_IMG = pygame.image.load(os.path.join("imgs", "worm.png"))
FISHERMAN_IMG = pygame.image.load(os.path.join  ("imgs", "fisherman3.png"))
BG_IMG = pygame.image.load(os.path.join  ("imgs", "background.png"))

# class Fish: used by player or ai in python game.py
class Fish:
    IMGS = FISH_IMGS    
    
    # constructor
    def __init__(self, x:int, y:int):
        self.x=x
        self.y=y
        self.SPEED = 5.5
        self.tick_count = 0
        self.img = self.IMGS[0]
        self.lastTime = 0
        self.lastPos = 0
        self.good = False

    # causes fish to "go up" when called
    def swimUp(self, ticks):
        
        ticksup = ticks
        
        if ticksup < 20:
            self.SPEED = -1*ticksup/2.5
        else:
            self.SPEED = -7.5

        self.y += self.SPEED     
        
    # causes fish to "fall down" due to gravity when called, this is perpetual.
    def move(self, ticks):
    
        ticksdown = ticks
        
        if ticksdown < 20:
            self.SPEED = 1*ticksdown/2.5
        else:
            self.SPEED = 7.5

        self.y += self.SPEED        
        
    # animates the fish
    
    def animate(self):
        self.tick_count+=1
        
        #check what image to show based on current image count.
        if self.tick_count < 12:
            self.img=self.IMGS[0]
        elif self.tick_count < 24:
            self.img=self.IMGS[1]
        elif self.tick_count < 36:
            self.img=self.IMGS[2]
        elif self.tick_count < 48:
            self.img=self.IMGS[1]
        elif self.tick_count < 60:
            self.img=self.IMGS[0]
            self.tick_count = 0  

    # Draws the fish on the screen
    def draw(self, win:pygame.display):
        win.blit(self.img, (self.x, self.y))
    
    # determines collision with fish to be used with collision detection
    def collide(self, object):
        object_mask = object.get_mask()
        # Create a mask from surface of image
        mask = pygame.mask.from_surface(self.img)
        # Calculate offset between the two masks
        offset = (int(self.x) - int(object.x), int(self.y) - int(object.y)) 
        
        #IF VALUES EXIST (collision), RETURN TRUE
        if object_mask.overlap(mask, offset):
            return True
        else:
            return False

# class Worm: used by computer in python game.py
class Worm:
    SPEED = 7.5
    
    # constructor
    def __init__(self, x:int=650, y:int=200):
        self.x=x
        self.y=y
        self.img = WORM_IMG
        self.collected = False
        
        self.set_Height()
    
    # sets the height of the worm
    def set_Height(self):
        self.y=rnd.randrange(50, 400)
    
    # causes worm to "go left" when called
    def move(self):
        self.x -= self.SPEED
    
    # Draws the worm on the screen
    def draw(self, win:pygame.display):
        win.blit(self.img, (self.x, self.y))
    
    # gets mask to later be used with collision detection        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Fisherman:
    SPEED = 7.5
    
    # constructor
    def __init__(self, x:int=650, y:int= 0):
        self.x=x
        self.y=y
        self.img = FISHERMAN_IMG
        self.passed = False
    
    # causes fisherman to "go left" when called
    def move(self):
        self.x -= self.SPEED
        
    # Draws the fisherman on the screen
    def draw(self, win:pygame.display):
        win.blit(self.img, (self.x, self.y))

    # gets mask to later be used with collision detection        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
        
class Shark:
    IMGS = SHARK_IMGS
    SPEED = 7.5
    
    # constructor
    def __init__(self, x:int=0, y:int=0):
        self.x=x
        self.y=y
        self.tick_count = 0
        self.img = self.IMGS[0]
        self.passed = False
        
        self.set_Height()
        self.set_x()
        
    # sets the y value of the shark
    def set_Height(self):
        self.y=rnd.randrange(50, 400)
        
    # sets the x value of the shark
    def set_x(self):
        self.x=rnd.randrange(700, 950)    
    
    # causes shark to "go left" when called
    def move(self):
        self.x -= self.SPEED
        self.tick_count += 1
        
    def animate(self):
        # show animation image based on tick count.
        if self.tick_count < 20:
            self.img=self.IMGS[0]
        elif self.tick_count < 40:
            self.img=self.IMGS[1]
        elif self.tick_count < 60:
            self.img=self.IMGS[0]
            self.tick_count = 0
    
    # Draws the shark on the screen
    def draw(self, win:pygame.display):
        win.blit(self.img, (self.x, self.y))
    
    # gets mask to later be used with collision detection        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Background:
    SPEED = 7.5
    WIDTH = BG_IMG.get_width()
    
    # constructor
    def __init__(self, x:int=0, y:int=0):
        self.x1 = x
        self.x2 = self.WIDTH
        self.y = y
        self.img = BG_IMG
    
    # causes background to "go left" when called
    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED
        
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
            
        if self.x2 + self.WIDTH <0:
            self.x2 = self.x1 + self.WIDTH
    
    # Draws the background on the screen
    def draw(self, win:pygame.display):
        win.blit(self.img, (self.x1, self.y))
        win.blit(self.img, (self.x2, self.y))  

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