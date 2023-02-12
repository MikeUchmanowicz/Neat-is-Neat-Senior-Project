import pygame
from GameModels import Fish, Fisherman, Shark, Worm, Background, draw_window

pygame.font.init()
pygame.display.set_caption('Swim, Fish, Swim!')

def game():
    # set window size
    win = pygame.display.set_mode((640, 480))
    
    fishes = []
    sharks = []
    fishermen = []
    worms = []
    
    fishes = [Fish(15, 240)]
    sharks = [Shark(), Shark()]
    fishermen = [Fisherman()]
    worms = [Worm()]
    background = Background()
    
    clock=pygame.time.Clock()
    
    run = True
    while run:
        # limit frame rate to 30 fps
        clock.tick(30)
        # check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False

        # move all objects
        background.move()
        for fish in fishes:
            fish.move()
        
        toRemove=[] #list of objects to remove (if they go off screen)
        
        for shark in sharks:
            shark.move()
            if shark.x + shark.img.get_width() < 0:
                toRemove.append(shark)
            
        for shark in toRemove:
            sharks.append(Shark())
            sharks.remove(shark)
            
        toRemove.clear()
            
        for fisherman in fishermen:
            fisherman.move()
            if fisherman.x + fisherman.img.get_width() < 0:
                toRemove.append(fisherman)
            
        
        for fisherman in toRemove:
            fishermen.remove(fisherman)
            fishermen.append(Fisherman())
        
        toRemove.clear()    
            
        for worm in worms:
            worm.move()
            if worm.x + worm.img.get_width() < 0:
                toRemove.append(worm)
            
        
        for worm in toRemove:
            worms.remove(worm)
            worms.append(Worm())
            
        toRemove.clear()
    
        # draw all objects
        draw_window(win, background, fishes, sharks, fishermen, worms)

if __name__ == "__main__":
    game()
    
