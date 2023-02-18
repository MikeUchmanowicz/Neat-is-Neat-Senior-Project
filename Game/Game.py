import pygame
from GameModels import Fish, Fisherman, Shark, Worm, Background, draw_background, draw_gameWindow
import time

# set window size and title
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
pygame.display.set_caption('Swim, Fish, Swim!')

    
# title screen
def title_screen():

    # Initialize window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    draw_background(win, Background())
    
    # Initialize colors and variables used within title screen
    color = (255,255,255)
    color_light = (170,170,170)
    color_dark = (100,100,100)
    
    tiny_font = pygame.font.SysFont('Verdana',20)
    small_font = pygame.font.SysFont('Verdana',35)
    large_font = pygame.font.SysFont('Verdana',69)
    
    game_text = small_font.render('Play Game' , True , color)
    demo_text = small_font.render(' AI DEMO ' , True , color)
    not_ready_text = tiny_font.render('Not Ready Yet' , True , color)
    title_text = large_font.render('Swim, Fish, Swim!' , True , color)
    
    # title screen loop
    run = True
    while run:
        # Initialize mouse
        mouse = pygame.mouse.get_pos()
        
        # Play Game button (2), changes color when mouse hovers over
        play_hovered = WINDOW_WIDTH/2-255 <= mouse[0] <= WINDOW_WIDTH/2-50 and WINDOW_HEIGHT/2 <= mouse[1] <= WINDOW_HEIGHT/2+50
        if play_hovered:
            pygame.draw.rect(win,color_light,[WINDOW_WIDTH/2-255,WINDOW_HEIGHT/2,200,50])
        else:
            pygame.draw.rect(win,color_dark,[WINDOW_WIDTH/2-255,WINDOW_HEIGHT/2,200,50])
            
        # View AI Demo Button (2), changes color when mouse hovers over
        demo_hovered = WINDOW_WIDTH/2+45 <= mouse[0] <= WINDOW_WIDTH/2+255 and WINDOW_HEIGHT/2 <= mouse[1] <= WINDOW_HEIGHT/2+50
        if demo_hovered:
            pygame.draw.rect(win,color_light,[WINDOW_WIDTH/2+45,WINDOW_HEIGHT/2,210,50])
        else:
            pygame.draw.rect(win,color_dark,[WINDOW_WIDTH/2+45,WINDOW_HEIGHT/2,210,50])
        
        # Place Text for all buttons and title
        win.blit(game_text , (WINDOW_WIDTH/2-250,WINDOW_HEIGHT/2))
        win.blit(demo_text , (WINDOW_WIDTH/2+50,WINDOW_HEIGHT/2))
        win.blit(not_ready_text , (WINDOW_WIDTH/2+80,WINDOW_HEIGHT/2+50))
        win.blit(title_text , (5,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()  
            if event.type == pygame.MOUSEBUTTONDOWN:    #If mouse is clicked
                if play_hovered:    # if mouse is clicked on play game button
                    game(False)
                    run=False
                elif demo_hovered: # if mouse is clicked on view demo button
                    game(True)
                    run = False
        #update display
        pygame.display.update()

# main game loop. AI is a boolean that determines whether the game is being played by a human or an AI
def game(AI:bool):
    
    # Initialize window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    draw_background(win, Background())
    
    # Sleeps a half second to allow the user to see the window before the game starts
    time.sleep(.5)
    
    # sets variables for use in determining frame rate
    clock=pygame.time.Clock()
    FPS = 30
    
    # define lists of objects used in game
    fishes = []
    sharks = []
    fishermen = []
    worms = []

    # adds objects to lists of objects in use
    if not AI:
        fishes = [Fish(15, 240)]
    sharks = [Shark(), Shark()]
    fishermen = [Fisherman()]
    worms = [Worm()]
    background = Background()
    
    run = True
    while run:
        # limit frame rate to 30 fps
        clock.tick(FPS)
        # check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                
        # move all objects
        background.move()
        for fish in fishes:
            if (not AI): # if AI is not being used, check for key presses
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    fishes[0].swimUp()
                fish.move()
            else:
                fish.move()
        
        toRemove=[] #list of objects to remove (if they go off screen)
        
        # move shark perpetually, if shark goes off screen, add them to a remove list
        for shark in sharks:
            shark.move()   
            if shark.x + shark.img.get_width() < 0:
                toRemove.append(shark)
                
        # if shark is in remove List, remove it from current sharks, and append a new one to "spawn" it again
        for shark in toRemove:
            sharks.append(Shark())
            sharks.remove(shark)
            
        toRemove.clear()
        
        # move fisherman perpetually, if fisherman goes off screen, add them to a remove list
        for fisherman in fishermen:
            fisherman.move()
            if fisherman.x + fisherman.img.get_width() < 0:
                toRemove.append(fisherman)
            
        # if fisherman is in remove List, remove it from current fishermen, and append a new one to "spawn" it again
        for fisherman in toRemove:
            fishermen.remove(fisherman)
            fishermen.append(Fisherman())
        
        toRemove.clear()    
        
        # move worm perpetually, if worm goes off screen, add them to a remove list
        for worm in worms:
            worm.move()
            if worm.x + worm.img.get_width() < 0:
                toRemove.append(worm)
            
        # if worm is in remove List, remove it from current worms, and append a new one to "spawn" it again
        for worm in toRemove:
            worms.remove(worm)
            worms.append(Worm())
            
        toRemove.clear()
    
        # draw all objects perpetually, updating the screen with current positions / locations
        draw_gameWindow(win, background, fishes, sharks, fishermen, worms)

# "Main" function, calls game and tells game whether an AI is being used.
if __name__ == "__main__":
    title_screen()
    
