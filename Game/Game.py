from GameModels import Fish, Fisherman, Shark, Worm, Background
from GameUtil import TITLE, WINDOW_HEIGHT, WINDOW_WIDTH, draw_background, draw_gameWindow 
import MyReporter
import pygame
import neat
import pickle
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
            keys = pygame.key.get_pressed() #check if space key is being pressed
            if keys[pygame.K_SPACE]:
                ticksDown = 0
                ticksUp += 1
                
                fish.swimUp(ticksUp) # if space is being pressed, swim up
                
            else:
                ticksUp = 0
                ticksDown +=1
                fish.move(ticksDown) # if space is not being pressed, do nothing, fish swims down.
                
            if fish.y + fish.img.get_height() < 0 or fish.y >= 480: # if fish is out of bounds, end game
                run = False
                gameOverScreen() # display game over screen
                break

            for shark in sharks:
                shark.move()
                if fish.collide(shark): # if fish collides with shark, decrease fitness of fish, remove fish from game
                    run = False
                    gameOverScreen() # display game over screen
                    break
                
                if shark.x + shark.img.get_width() < 0: # if object is off screen (left), remove it 
                    toRemove.append(shark) # add object to list of objects to remove
                    
            for shark in toRemove:
                sharks.remove(shark) # remove object from list of objects 
                sharks.append(Shark()) # add new object to replace removed object (right)
            toRemove.clear() 
        
            for fisherman in fishermen:
                fisherman.move()
                
                if fish.collide(fisherman): # if fish collides with fisherman, decrease fitness of fish, remove fish from game
                    run = False
                    gameOverScreen() # display game over screen
                    break
                
                if fisherman.x + fisherman.img.get_width() < 0: # if object is off screen (left), remove it 
                    toRemove.append(fisherman) # add object to list of objects to remove
                    
            for fisherman in toRemove:
                fishermen.remove(fisherman) # remove object from list of objects 
                fishermen.append(Fisherman()) # add new object to replace removed object (right)
            toRemove.clear() 
        
            for worm in worms:
                worm.move()
                
                if fish.collide(worm): # if fish collides with worm, increase fitness of fish, remove worm
                    stats['Score'] += 15 # increase score by 1 every frame
                    toRemove.append(worm)
                    
                if worm.x + worm.img.get_width() < 0: # if object is off screen (left), remove it 
                    toRemove.append(worm) # add object to list of objects to remove
                    
            for worm in toRemove:
                worms.remove(worm) # remove object from list of objects 
                worms.append(Worm()) # add new object to replace removed object (right)
            toRemove.clear() 
                            
        stats['Gen'] = GEN # update generation count in stats dictionary
        stats['Fishes Alive'] = len(fishes) # update fish count in stats dictionary
        
        background.move() # move background perpetually
        # draw all objects perpetually, updating the screen with current positions / locations
        draw_gameWindow(win, background, fishes, sharks, fishermen, worms, stats)
        
# main game loop. Used by player
def gameAI(genomes, config, trainedAI=False):
    
    # Initialize window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # sets variables for use in determining frame rate
    clock=pygame.time.Clock()
    FPS = 60
    
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

        if len(fishes) < 1: # if fishes dead, end round
            global GEN; GEN += 1 # increase generation count    
            run = False 
            break
            
        for x, fish in enumerate(fishes):
            fish.animate()
            gens[x].fitness += 0.1 # increase fitness of each fish by .1 every frame (distance moved)

            output = nets[x].activate((
                                    fish.SPEED , # FISH SPEED
                                    fish.y + (fish.img.get_height()/2), # FISH HEIGHT center
                                    sharks[0].y + (sharks[0].img.get_height()/2), #SHARK HEIGHT center
                                    sharks[1].y + (sharks[1].img.get_height()/2), #SHARK HEIGHT center
                                    fishermen[0].y + fishermen[0].img.get_height(), #FISHERMAN HEIGHT center
                                    worms[0].y + (worms[0].img.get_height()/2), #FISHERMAN HEIGHT center
                                    (fish.y - (sharks[0].y + sharks[0].img.get_height()/2)), #DISTANCE TO SHARK CENTER Y
                                    (fish.y - (sharks[1].y + sharks[1].img.get_height()/2)), #DISTANCE TO SHARK CENTER Y
                                    (fish.y - (fishermen[0].y + fishermen[0].img.get_height())), #DISTANCE TO FISHERMAN BOTTOM Y
                                    (fish.y -(worms[0].y + worms[0].img.get_height()/2)), #DISTANCE TO WORM CENTER Y
                                    (fish.x - sharks[0].x), #DISTANCE TO SHARK X
                                    (fish.x - sharks[1].x), #DISTANCE TO SHARK X
                                    (fish.x - fishermen[0].x), #DISTANCE TO FISHERMAN X
                                    (fish.x - worms[0].x) #DISTANCE TO WORM CENTER X
                                    ))
            
            # if output is greater than .5, swim up
            if output[0] > 0:
                ticksDown = 0
                ticksUp += 1
                fish.swimUp(ticksUp)
            else: # if output is less than .5, do nothing, gravity causes swim down.
                ticksUp = 0
                ticksDown +=1
                fish.move(ticksDown)
        
            if fish.y + fish.img.get_height() <= 5 or fish.y >= 470: # if fish is out of bounds, decrease fitness of fish, remove fish from game
                gens[x].fitness -= 25
                fishes.pop(x)
                nets.pop(x)
                gens.pop(x)

        for shark in sharks:
            shark.move()
            for x, fish in enumerate(fishes): 
                
                if not shark.passed and (shark.x + shark.img.get_width()) < fish.x:
                    for g in gens:
                        g.fitness += 13
                    shark.passed = True
                
                if fish.collide(shark): # if fish collides with shark, decrease fitness of fish, remove fish from game
                    gens[x].fitness -= 25
                    fishes.pop(x) 
                    nets.pop(x)
                    gens.pop(x)

            if shark.x + shark.img.get_width() < 0: # if object is off screen (left), remove it 
                toRemove.append(shark) # add object to list of objects to remove
        for shark in toRemove:
            sharks.remove(shark) # remove object from list of objects 
            sharks.append(Shark()) # add new object to replace removed object (right)
        toRemove.clear()  
            
        for fisherman in fishermen:
            fisherman.move()
            
            for x, fish in enumerate(fishes): 
                
                if not fisherman.passed and (fisherman.x + fisherman.img.get_width()) < fish.x:
                    for g in gens:
                        g.fitness += 13
                    fisherman.passed = True
                
                if fish.collide(fisherman): # if fish collides with fisherman, decrease fitness of fish, remove fish from game
                    gens[x].fitness -= 25
                    fishes.pop(x) 
                    nets.pop(x)
                    gens.pop(x)
            
            if fisherman.x + fisherman.img.get_width() < 0: # if object is off screen (left), remove it 
                toRemove.append(fisherman) # add object to list of objects to remove
        for fisherman in toRemove:
            fishermen.remove(fisherman) # remove object from list of objects
            fishermen.append(Fisherman()) # add new object to replace removed object (right)
        toRemove.clear()  
        
        for worm in worms:
            worm.move()
            
            for x, fish in enumerate(fishes): 
                if not worm.collected and fish.collide(worm): # if fish collides with worm, increase fitness of fish, remove worm
                    gens[x].fitness += 25
                    worm.collected = True
                    toRemove.append(worm)
            
            if worm.x + worm.img.get_width() < 0: # if object is off screen (left), remove it 
                toRemove.append(worm) # add object to list of objects to remove
        for worm in toRemove:
            worms.remove(worm) # remove object from list of objects
            worms.append(Worm()) # add new object to replace removed object (right)
        toRemove.clear()    
        
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
def run(config_path, trainedAI=False):
    
    # Loads the config file
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
        
    if not trainedAI:
        # Creates a population based off config & A Reporter Exctension.        
        mypop = neat.Population(config)
        mystats = neat.StatisticsReporter()
        
        #p.add_reporter(neat.StdOutReporter(True))
        mypop.add_reporter(mystats)
        mypop.add_reporter(MyReporter.myReporter(True, True)) #MyReporter is a Std.Out Reporter Extension in which we upload GenDatamodel to database.
        
        # Create a save / checkpoint file every 100 generations
        checkpoint = neat.Checkpointer(generation_interval=50, filename_prefix='neat-checkpoint-')
        mypop.add_reporter(checkpoint)
        
        # Runs the game 150 times, and returns the winner of the game, can be stored.
        bestFit = mypop.run(gameAI,5000)
        
        with open('trainedModel.pkl', 'wb') as f:
            pickle.dump(bestFit, f)
            f.close()
        
    else:
        #with open('trainedModel.pkl', 'rb') as f:
            #genome = pickle.load(f)
            #f.close()
        
        # Convert loaded genome into required data structure
        #genomes = [(1, genome)]
        
        # Load the population from a checkpoint file
        checkpoint_file = 'neat-checkpoint-693'
        mypop = neat.Checkpointer.restore_checkpoint(checkpoint_file)
        mystats = neat.StatisticsReporter()
        
        # Create a save / checkpoint file every 100 generations
        checkpoint = neat.Checkpointer(generation_interval=50, filename_prefix='neat-checkpoint-')
        mypop.add_reporter(checkpoint)
        
        #p.add_reporter(neat.StdOutReporter(True))
        mypop.add_reporter(MyReporter.myReporter(True, False)) #MyReporter is a Std.Out Reporter Extension in which we upload GenDatamodel to database.
        mypop.add_reporter(mystats)
        #gameAI(genomes, config)
        bestFit = mypop.run(gameAI, 5000)


# title screen, allows user to start game, or watch AI play game
def titleScreen():

    # Initialize window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    draw_background(win, Background())
    
    # Initialize colors and variables used within title screen
    color_white = (255, 255, 255)
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)
    
    # Initialize fonts used in title screen
    small_font = pygame.font.SysFont('Verdana', 35)
    large_font = pygame.font.SysFont('Verdana', 69)
    
    # Initialize text used in title screen
    game_text = small_font.render('Play Game', True, color_white)
    demo_text = small_font.render('AI Learning Demo', True, color_white)
    trainedDemo_text = small_font.render('AI Trained Demo', True, color_white)
    title_text = large_font.render('Swim, Fish, Swim!', True, color_white)
    
    # title screen loop
    runTitleScreen = True
    while runTitleScreen:
        # Initialize mouse
        mouse = pygame.mouse.get_pos()
        
        #create fish for images in background
        fish = Fish(WINDOW_WIDTH/3, WINDOW_HEIGHT/2)
        
        # Play Game button (1), changes color when mouse hovers over
        play_hovered = WINDOW_WIDTH/2-285 <= mouse[0] <= WINDOW_WIDTH/2-75 and WINDOW_HEIGHT/2 <= mouse[1] <= WINDOW_HEIGHT/2+50
        if play_hovered:
            pygame.draw.rect(win,color_light,[WINDOW_WIDTH/2-285,WINDOW_HEIGHT/2,210,50])
        else:
            pygame.draw.rect(win,color_dark,[WINDOW_WIDTH/2-285,WINDOW_HEIGHT/2,210,50])
            
        # View AI Demo Button (2), changes color when mouse hovers over
        demo_hovered = WINDOW_WIDTH/2-45 <= mouse[0] <= WINDOW_WIDTH/2+295 and WINDOW_HEIGHT/2 <= mouse[1] <= WINDOW_HEIGHT/2+50
        if demo_hovered:
            pygame.draw.rect(win,color_light,[WINDOW_WIDTH/2-45, WINDOW_HEIGHT/2, 340, 50])
        else:
            pygame.draw.rect(win,color_dark,[WINDOW_WIDTH/2-45, WINDOW_HEIGHT/2, 340, 50])
            
        # View AI Demo Button (2), changes color when mouse hovers over
        trained_demo_hovered = WINDOW_WIDTH/2-20 <= mouse[0] <= WINDOW_WIDTH/2+295 and WINDOW_HEIGHT/2+125 <= mouse[1] <= WINDOW_HEIGHT/2+175
        if trained_demo_hovered:
            pygame.draw.rect(win,color_light,[WINDOW_WIDTH/2-20, WINDOW_HEIGHT/2+125, 315, 50])
        else:
            pygame.draw.rect(win,color_dark,[WINDOW_WIDTH/2-20, WINDOW_HEIGHT/2+125, 315, 50])
        
        
        # Place Text for all buttons and title
        win.blit(game_text , (WINDOW_WIDTH/2-275,WINDOW_HEIGHT/2))
        win.blit(demo_text , (WINDOW_WIDTH/2-35,WINDOW_HEIGHT/2))
        win.blit(trainedDemo_text , (WINDOW_WIDTH/2-10,WINDOW_HEIGHT/2+125))
        win.blit(fish.IMGS[2], (WINDOW_WIDTH/6, WINDOW_HEIGHT/2.75))
        win.blit(fish.IMGS[2], ((WINDOW_WIDTH/1.5) -10, (WINDOW_HEIGHT/1.5)-10 ))
        
        for i in range(0,5):
            if i < 3:
                win.blit(fish.IMGS[i], ((WINDOW_WIDTH/2)-50+(75*i), WINDOW_HEIGHT/2.75))
            else:
                win.blit(fish.IMGS[i-2], ((WINDOW_WIDTH/2)-50+(75*i), WINDOW_HEIGHT/2.75))
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
                
                elif trained_demo_hovered:
                    # load config file
                    local_dir = os.path.dirname(__file__)
                    config_path = os.path.join(local_dir, "configTrained.txt")
                    time.sleep(.5)
                    
                    run(config_path, trainedAI=True) # run NEAT AI Simulation
                    runTitleScreen = False
                    break
                    
        #update display
        pygame.display.update()

# game over screen, displays score and allows user to play again or quit game once game is over
def gameOverScreen():
    # Initialize window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    draw_background(win, Background())
    
    # Initialize colors and variables used within title screen
    color_white = (255, 255, 255)
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)
    
    # Initialize fonts used in title screen
    small_font = pygame.font.SysFont('Verdana', 35)
    large_font = pygame.font.SysFont('Verdana', 69)
    
    # Initialize text used in title screen
    play_game_text = small_font.render('Play Again', True, color_white)
    game_over_text = large_font.render('Game Over', True, color_white)
    menu_text = small_font.render('Menu', True, color_white)
    score_text = small_font.render('Score: ' + str(round(stats['Score'], 3)), True, color_white)
    quit_text = small_font.render('Quit', True, color_white)
    
    # title screen loop
    runGameOverScreen = True
    while runGameOverScreen:
        # Initialize mouse
        mouse = pygame.mouse.get_pos()
        
        # Play Game button (1), changes color when mouse hovers over
        play_hovered = WINDOW_WIDTH/3 <= mouse[0] <= WINDOW_WIDTH/3+200 and WINDOW_HEIGHT/2 <= mouse[1] <= WINDOW_HEIGHT/2+50
        if play_hovered:
            pygame.draw.rect(win,color_light,[WINDOW_WIDTH/3,WINDOW_HEIGHT/2,200,50])
        else:
            pygame.draw.rect(win,color_dark,[WINDOW_WIDTH/3,WINDOW_HEIGHT/2,200,50])
        
        # Menu Screen Button (2), changes color when mouse hovers over
        menu_hovered = WINDOW_WIDTH/3+40 <= mouse[0] <= WINDOW_WIDTH/3+155 and WINDOW_HEIGHT/2+75 <= mouse[1] <= WINDOW_HEIGHT/2+125
        if menu_hovered:
            pygame.draw.rect(win,color_light,[WINDOW_WIDTH/3+40,WINDOW_HEIGHT/2+75,115,50])
        else:
            pygame.draw.rect(win,color_dark,[WINDOW_WIDTH/3+40,WINDOW_HEIGHT/2+75,115,50])
            
        # View AI Demo Button (3), changes color when mouse hovers over
        quit_hovered = WINDOW_WIDTH/3+50 <= mouse[0] <= WINDOW_WIDTH/3+145 and WINDOW_HEIGHT/2+150 <= mouse[1] <= WINDOW_HEIGHT/2+200
        if quit_hovered:
            pygame.draw.rect(win,color_light,[WINDOW_WIDTH/3+50,WINDOW_HEIGHT/2+150,95,50])
        else:
            pygame.draw.rect(win,color_dark,[WINDOW_WIDTH/3+50,WINDOW_HEIGHT/2+150,95,50])
            

        # Place Text for all buttons and title
        win.blit(game_over_text , (WINDOW_WIDTH/5,WINDOW_HEIGHT/6))
        win.blit(play_game_text , (WINDOW_WIDTH/3+10,WINDOW_HEIGHT/2))
        win.blit(menu_text , (WINDOW_WIDTH/3+50,WINDOW_HEIGHT/2+75))
        win.blit(quit_text , (WINDOW_WIDTH/3+60,WINDOW_HEIGHT/2+150))
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
                
                elif quit_hovered: # if mouse is clicked on view demo button
                    runGameOverScreen = False
                    pygame.quit()
                    quit()
                    
                elif menu_hovered: # if mouse is clicked on view demo button
                    runGameOverScreen = False
                    titleScreen()
                    
                    pygame.quit()
                    quit()
                    
        #update display
        pygame.display.update()

# "Main" function, calls game and tells game whether an AI is being used.
if __name__ == "__main__":
        
    # Return title screen
    titleScreen()
