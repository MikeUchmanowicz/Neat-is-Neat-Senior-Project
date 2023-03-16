import pygame
import os
import random as rnd

# set window size and title
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

#Load all class images. 
FISH_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "fishup.png")), (55, 42)),
            pygame.transform.scale(pygame.image.load(os.path.join("imgs", "fishmid.png")), (55, 42)), 
            pygame.transform.scale(pygame.image.load(os.path.join("imgs", "fishdown.png")), (55, 42))]

SHARK_IMGS = [pygame.image.load(os.path.join("imgs", "shark.png")),
            pygame.image.load(os.path.join("imgs", "shark2.png"))]
WORM_IMG = pygame.image.load(os.path.join("imgs", "worm.png"))
FISHERMAN_IMG = pygame.image.load(os.path.join  ("imgs", "fisherman2.png"))
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
    
    # causes fish to "go up" when called
    def swimUp(self):
        self.SPEED = -3.5
        
    # causes fish to "fall down" due to gravity when called, this is perpetual.
    def move(self):
        self.tick_count += 1
        
        # # calculate distance to move based on current velocity and tick count
        # # Distance = (velocity * time^2 ) / 2
        # distance = ( self.SPEED * self.tick_count**2 ) / 5
        
        # #if distance greater than 10 (down), set to 10 (down)
        # if distance>=5.5:
        #     distance = 5.5
        # #if distance less than 0 (up), set to 5.5 (down)
        # elif distance<0:
        #     distance = - 5.5
            
        self.y=self.y+self.SPEED       
        self.SPEED = 7.5
        
        #check what image to show based on current image count.
        if self.tick_count < 6:
            self.img=self.IMGS[0]
        elif self.tick_count < 12:
            self.img=self.IMGS[1]
        elif self.tick_count < 18:
            self.img=self.IMGS[2]
        elif self.tick_count < 24:
            self.img=self.IMGS[1]
        elif self.tick_count < 30:
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
        self.passed = False
        
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
        self.x=rnd.randrange(650, 850)    
    
    # causes shark to "go left" when called
    def move(self):
        self.x -= self.SPEED
        self.tick_count += 1
        
        # show animation image based on tick count.
        if self.tick_count < 8:
            self.img=self.IMGS[0]
        elif self.tick_count < 16:
            self.img=self.IMGS[1]
        elif self.tick_count < 24:
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