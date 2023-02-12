import pygame
from GameModels import Fish, Fisherman, Shark, Worm, draw_window

pygame.font.init()
pygame.display.set_caption('NEAT is Neat')

def game():
    # set window size
    win = pygame.display.set_mode((640, 480))
    
    fishes = []
    sharks = []
    fishermen = []
    worms = []
    
    fishes = [Fish(15, 240)]
    sharks = [Shark(620, 120), Shark(620, 360)]
    fishermen = [Fisherman(620, -60)]
    worms = [Worm(620, 200)]
    
    clock=pygame.time.Clock()
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False

        for fish in fishes:
            fish.move()
        
        for shark in sharks:
            shark.move()
            
        for fisherman in fishermen:
            fisherman.move()
            
        for worm in worms:
            worm.move()
    
        draw_window(win, fishes, sharks, fishermen, worms)

if __name__ == "__main__":
    game()
    
