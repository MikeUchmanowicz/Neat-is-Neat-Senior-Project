import pygame
import os
import random as rnd
import math

# set window size and title
WINDOW_WIDTH:int = 640
WINDOW_HEIGHT:int = 480

#Load all class images. 
FISH_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "fishup.png")), (49, 38)),
            pygame.transform.scale(pygame.image.load(os.path.join("imgs", "fishmid.png")), (49, 38)), 
            pygame.transform.scale(pygame.image.load(os.path.join("imgs", "fishdown.png")), (49, 38))]

FISH_GRAD = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "fishTrained.png")), (49, 38))

SHARK_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "shark.png")), (180, 82)), #(170, 78)
            pygame.transform.scale(pygame.image.load(os.path.join("imgs", "shark2.png")), (180, 82))]  #(170, 78)
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
        
    def raycast(self, sharks, win, fisherman):
        ray_length = 150
        centerx = self.x + self.img.get_width()
        centery = self.y + self.img.get_height() / 2
        start_pos = (centerx, centery)

        distances = [ray_length] * 9  # initialize with maximum possible distance

        bg_color = (0, 128, 255)  # blue
        win.fill(bg_color)

        wall_rects = (pygame.Rect(0,5,640,1), pygame.Rect(0,475,640, 1))

        angles = [80, 60, 40, 20, 0, -20, -40, -60, -80]
        
        distances = [ray_length] * len(angles)  # initialize with maximum possible distance

        
        # Send out rays from the fish object and check for collisions
        for i, angle in enumerate(angles):
            # Convert the angle to radians
            angle_rad = math.radians(angle)

            # Calculate the endpoint of the ray
            end_pos = (centerx + ray_length * math.cos(angle_rad),
                    centery + ray_length * math.sin(angle_rad))
            
            # Draw the ray
            pygame.draw.line(win, (255, 0, 0), start_pos, end_pos)

            obstacles = []
            
            rect = fisherman.get_rect()
            obstacles.append(rect)
                    
            for rect in wall_rects:
                obstacles.append(rect)
                
            for shark in sharks:
                rect = shark.get_rect()
                obstacles.append(rect)

            # Calculate the distance between the ray and each shark
            for j, object in enumerate(obstacles):
                sect_tuple = object.clipline(start_pos, end_pos)
                if sect_tuple:
                    intersect_tuple = sect_tuple[0]
                    pygame.draw.circle(win, (0, 255, 0), intersect_tuple, 5)
                    distance = math.hypot(intersect_tuple[0] - start_pos[0], intersect_tuple[1] - start_pos[1])
                    distances[i] = distance

        for i, d in enumerate(distances):
            distances[i] = round(d,3)
            
        return distances

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
        self.y=rnd.randrange(130, 260)
    
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
    
    def get_rect(self):
        return self.img.get_rect(topleft=(self.x, self.y))
        
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
    
    def get_rect(self):
        return self.img.get_rect(topleft=(self.x, self.y))

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