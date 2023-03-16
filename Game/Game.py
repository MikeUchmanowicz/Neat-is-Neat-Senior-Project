from GameModels import Fish, Fisherman, Shark, Worm, Background, draw_background, draw_gameWindow
import MyReporter
import pygame
import neat
import time
import random as rnd
import os

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
    color = (255, 255, 255)
    color_light = (170, 170, 170)
    color_dark = (100, 100, 100)
    
    # Initialize fonts used in title screen
    tiny_font = pygame.font.SysFont('Verdana', 20)
    small_font = pygame.font.SysFont('Verdana', 35)
    large_font = pygame.font.SysFont('Verdana', 69)
    
    # Initialize text used in title screen
    game_text = small_font.render('Play Game', True, color)
    demo_text = small_font.render(' AI DEMO ', True, color)
    not_ready_text = tiny_font.render('Not Ready Yet', True, color)
    title_text = large_font.render('Swim, Fish, Swim!', True, color)
    
    # title screen loop
    runtitle = True
    while runtitle:
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
                    time.sleep(.5)
                    game()
                    runtitle=False
                    
                    
                elif demo_hovered: # if mouse is clicked on view demo button
                    # Current directory of file
                    local_dir = os.path.dirname(__file__)
                    # Path to config file
                    config_path = os.path.join(local_dir, "config.txt")
                    time.sleep(.5)
                    run(config_path)
                    
                    runtitle = False
                    break
                    
        #update display
        pygame.display.update()

stats = {}
GEN = 0   

# main game loop. Used by player
def game():
    
    # Initialize window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    #Put the background to the screen, and sleep for half a second to allow the user to be ready for the game start
    draw_background(win, Background())
    
    # sets variables for use in determining frame rate
    clock=pygame.time.Clock()
    FPS = 30
    stats['score'] = 0
    
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
                
        # move all objects
        background.move()
        for fish in fishes:
        
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                fishes[0].swimUp()
            fish.move()
            
        
        toRemove=[] #list of objects to remove (if they go off screen)
        
        # move shark perpetually, if shark goes off screen, add them to a remove list
        for shark in sharks:
            shark.move()   
            
            if shark.collide(fishes[0]):
                    print("You got SHARKBAITED!")
            
            # if shark leaves the screen, add to removelist   
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
            
            if fisherman.collide(fishes[0]):
                    print("You got HOOKED!")
            
            # if fisherman leaves the screen, add to removelist    
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
            
            if worm.collide(fishes[0]):
                    print("You got a worm!")
            
            # if worm leaves the screen, add to removelist 
            if worm.x + worm.img.get_width() < 0:
                toRemove.append(worm)
            
        # if worm is in remove List, remove it from current worms, and append a new one to "spawn" it again
        for worm in toRemove:
            worms.remove(worm)
            worms.append(Worm())
            
        toRemove.clear()
    
        # draw all objects perpetually, updating the screen with current positions / locations
        draw_gameWindow(win, background, fishes, sharks, fishermen, worms, stats)
        
# main game loop. Used by player
def gameAI(genomes, config):
    
    fishes = []
    nets=[]
    gens=[]
    stats['Score'] = 0
    stats['Fishes Alive'] = 0
    
    # Initialize window
    win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    #Put the background to the screen, and sleep for half a second to allow the user to be ready for the game start
    draw_background(win, Background())
    
    # sets variables for use in determining frame rate
    clock=pygame.time.Clock()
    FPS = 30

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
    sharks = [Shark()]
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

        shark_idx = 0 # index of shark
        if len(fishes) > 0: # if fishes alive
            if len(sharks) > 1: # if there is more than one shark
                if fishes[0].x > sharks[0].x + sharks[0].img.get_width(): # if any fish is past the first shark
                    shark_idx = 1 # set shark index to 1
                    
        else:
            global GEN; GEN += 1
            run = False
            break
        
        for x, fish in enumerate(fishes): # Check if fish is out of bounds, if so, remove it from the game
            fish.move()
            gens[x].fitness += 0.1
        
            output = nets[x].activate((fish.y, abs(fish.y - sharks[shark_idx].y), abs(fish.y - sharks[shark_idx].y), abs(fish.y - fishermen[0].y), abs(fish.y - worms[0].y),))
        
            if output[0] > 0.5:
                fish.swimUp()
                #gens[x].fitness += .1
        
            if fish.y + fish.img.get_height() < 0 or fish.y >= 630:
                fishes.pop(x)
                nets.pop(x)
                gens.pop(x)

        for shark in sharks:
            shark.move() # move shark perpetually, if shark goes off screen, add them to a remove list
            
            for x, fish in enumerate(fishes):
                if shark.collide(fish):
                    fishes.pop(x)
                    nets.pop(x)
                    gens.pop(x)
                    
                if not shark.passed and shark.x < fish.x:
                    shark.passed = True
                    
            
            if shark.x + shark.img.get_width() < 0: # if shark leaves the screen, add to removelist
                toRemove.append(shark)
                
        # if shark is in remove List, remove it from current sharks, and append a new one to "spawn" it again
        for shark in toRemove:
            try:
                sharks.remove(shark)
            except:
                pass
            sharks.append(Shark()) 
            
        toRemove.clear() # clear remove list
        
        # move fisherman perpetually, if fisherman goes off screen, add them to a remove list
        for fisherman in fishermen:
            fisherman.move()
            
            for x, fish in enumerate(fishes):
                if fisherman.collide(fish):
                    fishes.pop(x)
                    nets.pop(x)
                    gens.pop(x)
                    
                if not fisherman.passed and fisherman.x < fish.x:
                    fisherman.passed = True
                    

            # if fisherman leaves the screen, add to removelist 
            if fisherman.x + fisherman.img.get_width() < 0:
                toRemove.append(fisherman)
            
        # if fisherman is in remove List, remove it from current fishermen, and append a new one to "spawn" it again
        for fisherman in toRemove:
            try:
                fishermen.remove(fisherman)
            except:
                pass
            fishermen.append(Fisherman())
        
        toRemove.clear()    
        
        # move worm perpetually, if worm goes off screen, add them to a remove list
        for worm in worms:
            worm.move()
            
            for x, fish in enumerate(fishes):
                if worm.collide(fish):
                    gens[x].fitness += 15
                    
                    toRemove.append(worm)
                    
                if not worm.passed and worm.x < fish.x:
                    worm.passed = True

            # if fisherman leaves the screen, add to removelist 
            if worm.x + worm.img.get_width() < 0:
                toRemove.append(worm)
            
        # if fisherman is in remove List, remove it from current fishermen, and append a new one to "spawn" it again
        for worm in toRemove:
            try:
                worms.remove(worm)
            except:
                pass
            worms.append(Worm())
        
        toRemove.clear()    
        
        max_fit = 0
        for g in gens:
            if g.fitness > max_fit:
                max_fit = g.fitness
        stats['Score'] = max_fit
        stats['Gen'] = GEN
        stats['Fishes Alive'] = len(fishes) # update fish count in stats dictionary
        background.move() # move background perpetually
        # draw all objects perpetually, updating the screen with current positions / locations
        draw_gameWindow(win, background, fishes, sharks, fishermen, worms, stats)
        
# run NEAT      
def run(config_path):
    
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    # Creates a population based off config & A Reporter Exctension.        
    mypop = neat.Population(config)
    mystats = neat.StatisticsReporter()
    
    #p.add_reporter(neat.StdOutReporter(True))
    mypop.add_reporter(mystats)
    mypop.add_reporter(MyReporter.myReporter(True)) #MyReporter is a Std.Out Reporter Extension in which we upload GenDatamodel to database.
    
    # Runs the game 150 times, and returns the winner of the game, can be stored.
    bestFit = mypop.run(gameAI,150)

# "Main" function, calls game and tells game whether an AI is being used.
if __name__ == "__main__":
        
    # Return title screen
    title_screen()
    

    
    
    
    
