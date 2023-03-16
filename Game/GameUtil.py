import pygame

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
    
def draw_background(win:pygame.display, background):

    # draw background
    background.draw(win)

    # update the display
    pygame.display.update()
    
def moveObjects(Object, objects, toRemove):
    
    for obj in objects: # move objects passed in
        obj.move()
                
        if obj.x + obj.img.get_width() < 0: # if object is off screen (left), remove it 
            toRemove.append(obj)
    
    for obj in toRemove:
        try:
            objects.remove(obj)
        except:
            pass
        objects.append(Object()) # add new object to replace removed object (right)
    
    toRemove.clear()