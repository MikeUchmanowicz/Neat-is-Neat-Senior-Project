from GameModels import Fish, Fisherman, Shark, Worm, Background
from GameUtil import TITLE, WINDOW_HEIGHT, WINDOW_WIDTH, draw_background, draw_gameWindow, moveObjects 
import MyReporter
import pygame
import neat
import time
import random as rnd
import os

"""
    NEAT AI Implementation, allowing a user to start a game of Swim, Fish, Swim! to either play the game themselves or watch the AI play the game.
"""

pygame.display.set_caption(TITLE)


stats = {'Score':0}
GEN = 0  

# main game loop. Used by player
def game():
    
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Initialize window
    draw_background(win, Background()) #Put the background to the screen, so it doesn't look like a black screen
        
    # Initialize window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # sets variables for use in determining frame rate
    clock=pygame.time.Clock()
    FPS = 30
    
    #dictionary keeping track of "points"
    stats['Score'] = 0
    stats['Fishes Alive'] = 0

    # variables for use in determining fish swimming up and down
    ticksDown = 0
    ticksUp = 0 

    # adds base objects
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
        
        stats['Score'] += .1 # increase score by 1 every frame
        toRemove = []
        
        
    
        for fish in fishes: # Check if fish is out of bounds, if so, remove it from the game
            fish.animate()
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                ticksDown = 0
                ticksUp += 1
                fish.swimUp(ticksUp)
            else:
                ticksUp = 0
                ticksDown +=1
                fish.move(ticksDown)
                
            if fish.y + fish.img.get_height() < 0 or fish.y >= 480: # if fish is out of bounds, end game
                run = False
                gameOverScreen()
                break

            for shark in sharks:
                if fish.collide(shark): # if fish collides with shark, decrease fitness of fish, remove fish from game
                    run = False
                    gameOverScreen()
                    break
                    
            moveObjects(Shark, sharks, toRemove)  # move objects perpetually, if object goes off screen, remove them and place a new one.
        
            for fisherman in fishermen:
                if fish.collide(fisherman): # if fish collides with fisherman, decrease fitness of fish, remove fish from game
                    run = False
                    gameOverScreen()
                    break
            moveObjects(Fisherman, fishermen, toRemove) # move objects perpetually, if object goes off screen, remove them and place a new one.
        
            for worm in worms:
                if fish.collide(worm): # if fish collides with worm, increase fitness of fish, remove worm
                    stats['Score'] += 15 # increase score by 1 every frame
                    toRemove.append(worm)
                    
            moveObjects(Worm, worms, toRemove) # move objects perpetually, if object goes off screen, remove them and place a new one.
                            
        stats['Gen'] = GEN # update generation count in stats dictionary
        stats['Fishes Alive'] = len(fishes) # update fish count in stats dictionary
        
        background.move() # move background perpetually
        # draw all objects perpetually, updating the screen with current positions / locations
        draw_gameWindow(win, background, fishes, sharks, fishermen, worms, stats)
        
# main game loop. Used by player
def gameAI(genomes, config):
    
    # Initialize window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # sets variables for use in determining frame rate
    clock=pygame.time.Clock()
    FPS = 30
    
    # variables for use in determining fish swimming up and down
    ticksDown = 0
    ticksUp = 0 
    
    # define variables
    fishes = []
    #networks
    nets=[]
    #genomes
    gens=[]
    #dictionary keeping track of "points"
    stats['Score'] = 0
    stats['Fishes Alive'] = 0

    # loop through tuple of genomes provided by NEAT CONFIG and create a network and fish for each genome
    for _, g in genomes:
        # Create a neural network for each genome
        net=neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        
        # Set fitness of each genome to 0
        g.fitness = 0
        gens.append(g)
        
        # Create a fish for each genome
        fishes.append(Fish(15, 240))

    # adds base objects
    sharks = [Shark(), Shark()]
    fishermen = [Fisherman()]
    worms = [Worm()]
    background = Background()
    toRemove=[] #list of objects to remove (if they go off screen)

    run = True
    while run:
        clock.tick(FPS) # limit frame rate to 30 fps
        
        for event in pygame.event.get(): # check for quit event
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        if len(fishes) < 1: # if fishes dead
            
            global GEN; GEN += 1
            run = False
            break
            
        for x, fish in enumerate(fishes): # Check if fish is out of bounds, if so, remove it from the game
            
            gens[x].fitness += 0.1
            
            output = nets[x].activate((fish.y + (fish.img.get_height())/2, # FISH HEIGHT center
                                    abs(fish.y - sharks[0].y), #DISTANCE TO SHARK TOP
                                    #abs(fish.y - (sharks[0].y + sharks[0].img.get_height())), #DISTANCE TO SHARK BOTTOM
                                    abs(fish.y - sharks[1].y), #DISTANCE TO SHARK TOP
                                    #abs(fish.y - (sharks[1].y + sharks[0].img.get_height())), #DISTANCE TO SHARK BOTTOM
                                    abs(fish.y - (fishermen[0].y + fishermen[0].img.get_height())), #DISTANCE TO FISHERMAN BOTTOM
                                    abs(fish.y - (worms[0].y + worms[0].img.get_height()/2)) #DISTANCE TO WORM CENTER
                                    ))
            if output[0] > 0.5:
                ticksDown = 0
                ticksUp += 1
                fish.swimUp(ticksUp)
            else:
                ticksUp = 0
                ticksDown +=1
                fish.move(ticksDown)
        
            if fish.y + fish.img.get_height() < 0 or fish.y >= 480: # if fish is out of bounds, decrease fitness of fish, remove fish from game
                fishes.pop(x)
                nets.pop(x)
                gens.pop(x)

        for shark in sharks:
            for x, fish in enumerate(fishes): 
                
                #if not shark.passed and shark.x < fish.x:
                    #gens[x].fitness += 10
                
                if fish.collide(shark): # if fish collides with shark, decrease fitness of fish, remove fish from game
                    gens[x].fitness -= 15
                    fishes.pop(x) 
                    nets.pop(x)
                    gens.pop(x)
        moveObjects(Shark, sharks, toRemove)  # move objects perpetually, if object goes off screen, remove them and place a new one.
        
        for fisherman in fishermen:
            for x, fish in enumerate(fishes): 
                
                #if not fisherman.passed and fisherman.x < fish.x:
                    #gens[x].fitness += 10
                
                if fish.collide(fisherman): # if fish collides with fisherman, decrease fitness of fish, remove fish from game
                    gens[x].fitness -= 15
                    fishes.pop(x) 
                    nets.pop(x)
                    gens.pop(x)
        moveObjects(Fisherman, fishermen, toRemove) # move objects perpetually, if object goes off screen, remove them and place a new one.
        
        
        for worm in worms:
            for x, fish in enumerate(fishes): 
                if fish.collide(worm): # if fish collides with worm, increase fitness of fish, remove worm
                    gens[x].fitness += 15
                    toRemove.append(worm)
        moveObjects(Worm, worms, toRemove) # move objects perpetually, if object goes off screen, remove them and place a new one.
                            
        # determine max fitness of all fishes/genomes
        max_fit = 0
        for g in gens:
            if g.fitness > max_fit:
                max_fit = g.fitness
        
        stats['Score'] = max_fit # update score in stats dictionary
        stats['Gen'] = GEN # update generation count in stats dictionary
        stats['Fishes Alive'] = len(fishes) # update fish count in stats dictionary
        
        background.move() # move background perpetually
        # draw all objects perpetually, updating the screen with current positions / locations
        draw_gameWindow(win, background, fishes, sharks, fishermen, worms, stats)
        
# run NEAT 
def run(config_path):
    
    # Loads the config file
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    # Creates a population based off config & A Reporter Exctension.        
    mypop = neat.Population(config)
    mystats = neat.StatisticsReporter()
    
    #p.add_reporter(neat.StdOutReporter(True))
    mypop.add_reporter(mystats)
    mypop.add_reporter(MyReporter.myReporter(True)) #MyReporter is a Std.Out Reporter Extension in which we upload GenDatamodel to database.
    
    # Runs the game 150 times, and returns the winner of the game, can be stored.
    bestFit = mypop.run(gameAI,150)

# title screen
def titleScreen():

    # Initialize window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    draw_background(win, Background())
    
    # Initialize colors and variables used within title screen
    color = (255, 255, 255)
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)
    
    # Initialize fonts used in title screen
    small_font = pygame.font.SysFont('Verdana', 35)
    large_font = pygame.font.SysFont('Verdana', 69)
    
    # Initialize text used in title screen
    game_text = small_font.render('Play Game', True, color)
    demo_text = small_font.render(' AI Demo ', True, color)
    title_text = large_font.render('Swim, Fish, Swim!', True, color)
    
    # title screen loop
    runTitleScreen = True
    while runTitleScreen:
        # Initialize mouse
        mouse = pygame.mouse.get_pos()
        
        fishes = [Fish(WINDOW_WIDTH/3, WINDOW_HEIGHT/2), Fish(WINDOW_WIDTH/3, WINDOW_HEIGHT/2), Fish(WINDOW_WIDTH/3, WINDOW_HEIGHT/2), Fish(WINDOW_WIDTH/3, WINDOW_HEIGHT/2)]
        # Play Game button (1), changes color when mouse hovers over
        play_hovered = WINDOW_WIDTH/2-260 <= mouse[0] <= WINDOW_WIDTH/2-50 and WINDOW_HEIGHT/2 <= mouse[1] <= WINDOW_HEIGHT/2+50
        if play_hovered:
            pygame.draw.rect(win,color_light,[WINDOW_WIDTH/2-260,WINDOW_HEIGHT/2,210,50])
        else:
            pygame.draw.rect(win,color_dark,[WINDOW_WIDTH/2-260,WINDOW_HEIGHT/2,210,50])
            
        # View AI Demo Button (2), changes color when mouse hovers over
        demo_hovered = WINDOW_WIDTH/2+50 <= mouse[0] <= WINDOW_WIDTH/2+230 and WINDOW_HEIGHT/2 <= mouse[1] <= WINDOW_HEIGHT/2+50
        if demo_hovered:
            pygame.draw.rect(win,color_light,[WINDOW_WIDTH/2+50, WINDOW_HEIGHT/2, 180, 50])
        else:
            pygame.draw.rect(win,color_dark,[WINDOW_WIDTH/2+50, WINDOW_HEIGHT/2, 180, 50])
        
        # Place Text for all buttons and title
        win.blit(game_text , (WINDOW_WIDTH/2-250,WINDOW_HEIGHT/2))
        win.blit(demo_text , (WINDOW_WIDTH/2+50,WINDOW_HEIGHT/2))
        win.blit(fishes[0].img, (WINDOW_WIDTH/4.5, WINDOW_HEIGHT/2.75))
        
        for i in range(0,3):
            win.blit(fishes[i].img, ((WINDOW_WIDTH/2)+30+(75*i), WINDOW_HEIGHT/2.75))
        win.blit(title_text , (5,0))
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # if quit (RED X) button is clicked
                pygame.quit()
                quit()  
            if event.type == pygame.MOUSEBUTTONDOWN: #If mouse is clicked
                if play_hovered:    # if mouse is clicked on play game button
                    time.sleep(.5)
                    game() # run game
                    
                    runTitleScreen=False
                    break
                
                elif demo_hovered: # if mouse is clicked on view demo button
                    # load config file
                    local_dir = os.path.dirname(__file__)
                    config_path = os.path.join(local_dir, "config.txt")
                    time.sleep(.5)
                    run(config_path) # run NEAT AI Simulation
                    
                    runTitleScreen = False
                    break
                    
        #update display
        pygame.display.update()

def gameOverScreen():
    # Initialize window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    draw_background(win, Background())
    
    # Initialize colors and variables used within title screen
    color = (255, 255, 255)
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)
    
    # Initialize fonts used in title screen
    small_font = pygame.font.SysFont('Verdana', 35)
    large_font = pygame.font.SysFont('Verdana', 69)
    
    # Initialize text used in title screen
    game_text = small_font.render('Play Again', True, color)
    game_over_text = large_font.render('Game Over', True, color)
    score_text = small_font.render('Score: ' + str(round(stats['Score'], 3)), True, color)
    demo_text = small_font.render('     Quit   ', True, color)
    
    # title screen loop
    runGameOverScreen = True
    while runGameOverScreen:
        # Initialize mouse
        mouse = pygame.mouse.get_pos()
        
        # Play Game button (2), changes color when mouse hovers over
        play_hovered = WINDOW_WIDTH/2-260 <= mouse[0] <= WINDOW_WIDTH/2-60 and WINDOW_HEIGHT/2 <= mouse[1] <= WINDOW_HEIGHT/2+50
        if play_hovered:
            pygame.draw.rect(win,color_light,[WINDOW_WIDTH/2-260,WINDOW_HEIGHT/2,200,50])
        else:
            pygame.draw.rect(win,color_dark,[WINDOW_WIDTH/2-260,WINDOW_HEIGHT/2,200,50])
            
        # View AI Demo Button (2), changes color when mouse hovers over
        exit_hovered = WINDOW_WIDTH/2+100 <= mouse[0] <= WINDOW_WIDTH/2+195 and WINDOW_HEIGHT/2 <= mouse[1] <= WINDOW_HEIGHT/2+50
        if exit_hovered:
            pygame.draw.rect(win,color_light,[WINDOW_WIDTH/2+100,WINDOW_HEIGHT/2,95,50])
        else:
            pygame.draw.rect(win,color_dark,[WINDOW_WIDTH/2+100,WINDOW_HEIGHT/2,95,50])
        
        # Place Text for all buttons and title
        win.blit(game_over_text , (WINDOW_WIDTH/5,WINDOW_HEIGHT/6))
        win.blit(game_text , (WINDOW_WIDTH/2-250,WINDOW_HEIGHT/2))
        win.blit(demo_text , (WINDOW_WIDTH/2+50,WINDOW_HEIGHT/2))
        win.blit(score_text , (WINDOW_WIDTH/2-100,WINDOW_HEIGHT/3))
        
        
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: # if quit (RED X) button is clicked
                pygame.quit()
                quit()  
            if event.type == pygame.MOUSEBUTTONDOWN: #If mouse is clicked
                if play_hovered:    # if mouse is clicked on play game button
                    time.sleep(.5)
                    game() # run game
                    
                    runGameOverScreen=False
                    break
                
                elif exit_hovered: # if mouse is clicked on view demo button
                    runGameOverScreen = False
                    pygame.quit()
                    quit()
                    
        #update display
        pygame.display.update()


# "Main" function, calls game and tells game whether an AI is being used.
if __name__ == "__main__":
        
    # Return title screen
    titleScreen()
