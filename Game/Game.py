from turtle import window_height
from GameModels import Fish, Fisherman, Shark, Worm, Background
from GameUtil import TITLE, WINDOW_HEIGHT, WINDOW_WIDTH, draw_background, draw_gameWindow
import MyReporter
import pygame
import neat
import visualize
import pickle
import time
import random as rnd
import os
import numpy as np


"""
    NEAT AI Implementation, allowing a user to start a game of Swim, Fish, Swim! to either play the game themselves or watch the AI play the game.
"""

pygame.display.set_caption(TITLE)

stats = {'Score':0}
stats = {'High Score':0}
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
    sharks = [Shark()]
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
        
        for fish in fishes:
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
            
            # if keys[pygame.K_LEFT]:
            #     sharks[0].SPEED = 0
            # if keys[pygame.K_RIGHT]:
            #     sharks[0].SPEED = 7.5
                
            if fish.y + fish.img.get_height() < 0 or (fish.y + fish.img.get_height()) >= WINDOW_HEIGHT: # if fish is out of bounds, end game
                run = False
                gameOverScreen() # display game over screen
                break

            for shark in sharks:
                shark.move()

                if fish.collide(shark): # if fish collides with shark
                    run = False
                    gameOverScreen() # display game over screen
                    break
                
                if not shark.passed and (shark.x + shark.img.get_width()) < fish.x:
                    stats['Score'] += 7.5 # increase score
                    shark.passed = True
                
                if shark.x + shark.img.get_width() < 0: # if object is off screen (left), remove it 
                    toRemove.append(shark) # add object to list of objects to remove
                    
            for shark in toRemove:
                sharks.remove(shark) # remove object from list of objects 
                sharks.append(Shark()) # add new object to replace removed object (right)
            toRemove.clear() 
        
            for fisherman in fishermen:
                fisherman.move()
                
                if fish.collide(fisherman): # if fish collides with fisherman
                    run = False
                    gameOverScreen() # display game over screen
                    break
                
                if not fisherman.passed and (fisherman.x + fisherman.img.get_width()) < fish.x:
                    stats['Score'] += 7.5 # increase score
                    fisherman.passed = True
                
                if fisherman.x + fisherman.img.get_width() < 0: # if object is off screen (left), remove it 
                    toRemove.append(fisherman) # add object to list of objects to remove
                    
            for fisherman in toRemove:
                fishermen.remove(fisherman) # remove object from list of objects 
                fishermen.append(Fisherman()) # add new object to replace removed object (right)
            toRemove.clear() 
        
            for worm in worms:
                worm.move()
                
                if fish.collide(worm): # if fish collides with worm, remove worm
                    stats['Score'] += 25 # increase score by 1 every frame
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
        
        
# main game loop. Used by AI
def gameAI(genomes, config):
    
    # Initialize window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # sets variables for use in determining frame rate
    clock=pygame.time.Clock()
    FPS = 120
    
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

        time = pygame.time.get_ticks()
        
        if len(fishes) < 1: # if fishes dead, end round
            global GEN; GEN += 1 # increase generation count  
            run = False # break current generation, start new generation
            break
            
        for x, fish in enumerate(fishes):
            
            #fish.animate()
            shark0val=0
            shark1val=0
            
            if fish.y + fish.img.get_height() < sharks[0].y:    #If Shark is below fish
                shark0val = ((sharks[0].y) - (fish.y + fish.img.get_height()))

            elif fish.y > sharks[0].y + sharks[0].img.get_height():  #If Shark is above fish
                shark0val = ((fish.y) - (sharks[0].y + sharks[0].img.get_height()))
            else:        
                                # if fish is partially inside shark (from top)
                if fish.y <= sharks[0].y <= fish.y + fish.img.get_height() and (fish.y + fish.img.get_height() < sharks[0].y + sharks[0].img.get_height()/2): 
                    shark0val = -99 #(sharks[0].y - (fish.y + fish.img.get_height()))
                                # if fish is partially inside shark (from bottom)
                if sharks[0].y <= fish.y <= sharks[0].y + sharks[0].img.get_height() and (fish.y > sharks[0].y + sharks[0].img.get_height()/2): 
                    shark0val = -99 #(fish.y - (sharks[0].y + sharks[0].img.get_height()))
                    
            if fish.y + fish.img.get_height() < sharks[1].y:    #If Shark is below fish
                shark1val = ((sharks[1].y) - (fish.y + fish.img.get_height()))
            elif fish.y > sharks[1].y + sharks[1].img.get_height():  #If Shark is above fish
                shark1val = ((fish.y) - (sharks[1].y + sharks[1].img.get_height()))
            else:        
                                # if fish is partially inside shark (from top)
                if fish.y <= sharks[1].y <= fish.y + fish.img.get_height() and (fish.y + fish.img.get_height() < sharks[1].y + sharks[1].img.get_height()/2): 
                    shark1val = -99 #(sharks[1].y - (fish.y + fish.img.get_height()))
                                # if fish is partially inside shark (from bottom)
                if sharks[1].y <= fish.y <= sharks[1].y + sharks[1].img.get_height() and (fish.y > sharks[1].y + sharks[1].img.get_height()/2): 
                    shark1val = -99 #(fish.y - (sharks[1].y + sharks[1].img.get_height()))
            
            # if fish.y < fishermen[0].y + fishermen[0].img.get_height(): # if fish is above fisherman
            #     fisherman0val = -99
            # else:
            #     fisherman0val = ((fish.y) - (fishermen[0].img.get_height()))

            # determine AI output through inputs
            output = nets[x].activate((
                                    #fish.SPEED, # FISH SPEED / POS - NEG
                                    abs(WINDOW_HEIGHT - fish.y),    # DISTANCE TO WINDOW BOTTOM
                                    
                                    # fish.y, # FISH HEIGHT
                                    # sharks[0].y + (sharks[0].img.get_height()/2), #SHARK HEIGHT center
                                    # sharks[1].y + (sharks[1].img.get_height()/2), #SHARK HEIGHT center
                                    # fishermen[0].y + fishermen[0].img.get_height(), #FISHERMAN HEIGHT center
                                    # worms[0].y + (worms[0].img.get_height()/2), #WORM HEIGHT center

                                    shark0val, #DISTANCE TO SHARK Y BASED ON POSITION OF FISH
                                    shark1val, #DISTANCE TO SHARK2 Y BASED ON POSITION OF FISH
                                    #sharks[0].passed, #FISH PASSED SHARK
                                    #sharks[1].passed, #FISH PASSED SHARK
                                    
                                    #fisherman0val, #DISTANCE TO FISHERMAN BOTTOM Y
                                    abs((fish.y + fish.img.get_height()/2) - (worms[0].y + worms[0].img.get_height()/2)), #DISTANCE TO WORM CENTER Y
                                    (sharks[0].x - (fish.x + fish.img.get_width())), #DISTANCE TO SHARK X
                                    (sharks[1].x - (fish.x + fish.img.get_width())), #DISTANCE TO SHARK X
                                    #(fishermen[0].x - fish.x ), #DISTANCE TO FISHERMAN X
                                    #(worms[0].x - fish.x), #DISTANCE TO WORM CENTER X
                                    ))
        
            # if output is greater than 0, swim up
            if output[0] > 0:
                #if not (fish.y < 1):
                    ticksDown = 0
                    ticksUp += 1
                    fish.swimUp(ticksUp)
            else: # if output is less than other output, gravity causes swim down.
                #if not (fish.y + fish.img.get_height() > WINDOW_HEIGHT -1):
                    ticksUp = 0
                    ticksDown +=1
                    fish.move(ticksDown)
                
            # Update Last Position
            if time % 100 == 0:
                fish.lastPos = fish.y
                
            # if any fish haven't moved more than 3 pixels, increase lastTime
            if abs(fish.lastPos - fish.y) < 4:
                fish.lastTime += 100
            else:
                fish.lastTime = 0
                
            # if fish hasn't moved more than 3 pixels in 10 seconds, remove fish from game
            if abs(fish.lastPos - fish.y) < 4 and fish.lastTime > 7500:
                gens[x].fitness -= 1
                
            # if fish is out of bounds, decrease fitness of fish, remove fish from game
            if fish.y <= 0 or (fish.y + fish.img.get_height()) >= WINDOW_HEIGHT: 
                gens[x].fitness = 0
                nets.pop(x)
                gens.pop(x)
                fishes.pop(x)
            
        for shark in sharks:
            shark.move()
            #shark.animate()
            
            for x, fish in enumerate(fishes): 
                
                                                                        #IF ALL OF FISH IS INSIDE SHARK Y
                if (shark.y <= (fish.y) <= shark.y + shark.img.get_height()) and (shark.y <= (fish.y + fish.img.get_height()) <= shark.y + shark.img.get_height()):
                    gens[x].fitness -= .2
                    pass
                                                                        #IF SOME OF FISH IS INSIDE SHARK Y 
                elif (shark.y <= (fish.y) <= shark.y + shark.img.get_height()) or (shark.y <= (fish.y + fish.img.get_height()) <= shark.y + shark.img.get_height()):
                    #gens[x].fitness -= .1
                    pass
                else:                                                   #IF NONE OF FISH IS INSIDE SHARK Y
                    gens[x].fitness +=.3
                
                if fish.collide(shark): # if fish collides with shark, decrease fitness of fish, remove fish from game
                    nets.pop(x)
                    gens.pop(x)
                    fishes.pop(x)

            if shark.x + shark.img.get_width() < 0: # if object is off screen (left), remove it 
                toRemove.append(shark) # add object to list of objects to remove
        for shark in toRemove:
            sharks.append(Shark()) # add new object to replace removed object (right)
            sharks.remove(shark) # remove object from list of objects 
            
        toRemove.clear()  
            
        for fisherman in fishermen:
            fisherman.move()
            
            for x, fish in enumerate(fishes): 
                
                # if (fish.y  <= fisherman.img.get_height()):
                #     gens[x].fitness -= .2
                
                if fish.collide(fisherman): # if fish collides with fisherman, decrease fitness of fish, remove fish from game
                    gens[x].fitness -= 50
                    nets.pop(x)
                    gens.pop(x)
                    fishes.pop(x)
            
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
                    gens[x].fitness += 50
                    worm.collected = True
                    toRemove.append(worm)
            
            if worm.x + worm.img.get_width() < 0: # if object is off screen (left), remove it 
                toRemove.append(worm) # add object to list of objects to remove
        for worm in toRemove:
            worms.remove(worm) # remove object from list of objects
            worms.append(Worm()) # add new object to replace removed object (right)
        toRemove.clear()    
        
        max_fit = 0
        for g in gens:
            if g.fitness > max_fit:
                max_fit = g.fitness
                
        if max_fit > stats['High Score']:
            stats['High Score'] = max_fit
        
        stats['Score'] = max_fit # update score in stats dictionary
        stats['Gen'] = GEN # update generation count in stats dictionary
        stats['Fishes Alive'] = len(fishes) # update fish count in stats dictionary
        
        background.move() # move background perpetually
        # draw all objects perpetually, updating the screen with current positions / locations
        draw_gameWindow(win, background, fishes, sharks, fishermen, worms, stats)

def leaky_relu(x):
    return np.maximum(0.01*x, x)

# run NEAT 
def run():
    
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    
    # Loads the config file
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    # Loads self-defined activation function
    config.genome_config.add_activation('leaky_relu', leaky_relu)  

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
    best_genome = mypop.run(gameAI, 3000)

    # Save the best genome
    with open('trainedModel.pkl', 'wb') as f:
        pickle.dump(best_genome, f)
        f.close()
        
    print("Model Saved")
        
def trainWithCheckpoint():
    
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    
    # Loads the config file
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    # Loads self-defined activation function
    config.genome_config.add_activation('leaky_relu', leaky_relu)  
    
    # Load the population from a checkpoint file
    checkpoint_file = 'best-checkpoint-464'
    mypop = neat.Checkpointer.restore_checkpoint(checkpoint_file)
    
    # Creates a population based off config & A Reporter Extension.        
    mypop = neat.Population(config)
    #mypop.best_genome = best_genome
    mystats = neat.StatisticsReporter()
    
    #p.add_reporter(neat.StdOutReporter(True))
    mypop.add_reporter(MyReporter.myReporter(True, False)) #MyReporter is a Std.Out Reporter Extension in which we upload GenDatamodel to database.
    mypop.add_reporter(mystats)
    #gameAI(genomes, config)
    winner = mypop.run(gameAI, 2000)
    
    # Save the best genome
    with open('trainedModel2.pkl', 'wb') as f:
        pickle.dump(winner, f)
        f.close()
        
    print("Model Saved")

def runTrained():
    
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "configTrained.txt")

    # load the best genome
    with open('trainedModel.pkl', 'rb') as f:
        best_genome = pickle.load(f)
        f.close()
        
    print("Model Loaded")
    
    # Convert loaded genome into list of genome tuples
    genomes = [(1, best_genome)]
    
    # Loads the config file
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Loads self-defined activation function
    config.genome_config.add_activation('leaky_relu', leaky_relu) 

    # Load the population from a checkpoint file
    # checkpoint_file = 'latest-checkpoint-4776'
    # mypop = neat.Checkpointer.restore_checkpoint(checkpoint_file)
    
    # Creates a population based off config & A Reporter Extension.        
    mypop = neat.Population(config)
    #mypop.best_genome = best_genome
    mystats = neat.StatisticsReporter()
    
    #p.add_reporter(neat.StdOutReporter(True))
    mypop.add_reporter(MyReporter.myReporter(True, False)) #MyReporter is a Std.Out Reporter Extension in which we upload GenDatamodel to database.
    mypop.add_reporter(mystats)
    #gameAI(genomes, config)
    gameAI(genomes, config)


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
            
        # View AI Learned Demo Button (3), changes color when mouse hovers over
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
                    time.sleep(.5)
                    
                    run() # run NEAT AI Simulation
                    runTitleScreen = False
                    break
                
                elif trained_demo_hovered:
                    time.sleep(.5)
                    
                    runTrained() # run NEAT AI Simulation
                    runTitleScreen = False
                    break
                
            keys = pygame.key.get_pressed() #check if space key is being pressed
            if keys[pygame.K_SPACE]:
                trainWithCheckpoint()
                
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
