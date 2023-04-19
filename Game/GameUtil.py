import pygame
import os
import graphviz
import neat

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
    
# draw background, used by title screen and game over screen
def draw_background(win:pygame.display, background):
    # draw background
    background.draw(win)
    # update the display
    pygame.display.update()

def draw_net(config, genome, view=False, filename=None):
    # Load the configuration file
    node_names = { -1:'x', -2:'y', 0:'output' }
    for i in range(len(config.genome_config.input_keys)):
        node_names[i] = 'input{}'.format(i)
    # Create a Graphviz graph
    g = graphviz.Digraph(format='png')
    # Add nodes for each neuron
    for node in genome.nodes:
        if node in node_names:
            label = node_names[node]
        else:
            label = str(node)
        color = 'blue' if node < 0 else 'black'
        g.node(str(node), label=label, style='filled', fillcolor=color)
    # Add edges for each connection
    for edge in genome.connections.values():
        if edge.enabled:
            color = 'green' if edge.weight > 0 else 'red'
            g.edge(str(edge.in_node), str(edge.out_node), label='{:.1f}'.format(edge.weight), color=color)
    # View or save the graph
    if view:
        g.view()
    if filename:
        g.render(filename, directory=os.path.join(os.getcwd(), 'graphs'), cleanup=True)

