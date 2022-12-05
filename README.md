# Neat-is-Neat-Senior-Project
*Python, Pygame, Django, NEAT AI*

## ABSTRACT

The “NEAT is Neat” project will consist of a main application containing a game and an Artificial Intelligence bot paired with a secondary web application to fetch/display data from the main application. The project is intended to further one’s understanding of how an Artificial Intelligence bot evolves to play games proficiently through the creation of an AI that plays games proficiently.

Within the main application, the user will be able to select whether they’d like to see a visual demonstration of the AI evolving and playing the game as it evolves or whether they’d like to play the game on their own. The game will be fairly simple, having a couple of objectives in which the player (and/or AI) will be expected to play indefinitely, trying to reach as far in the level as possible while collecting items like worms. Score will be determined by the distance that the player (and/or AI) achieves within the game and by the number of worms collected within that distance. The player (and/or AI) will play until the game is considered over; this is when the player (and/or AI) dies/ collides with an obstacle. There will only be one stage/level, which will have randomized worms to pick up and randomized obstacles to dodge. The AI will need to be taught through configuration of which actions are preferred and which actions are undesirable. The game will be looped until the AI evolves enough to play proficiently. With each iteration of the game, the AI should get progressively better by increasing its score through completing preferred actions like gaining worms or getting farther in the stage. At some point down the iteration line, the AI should be able to play the game as well as, if not better than, a human player.

The scores, distances travelled, coins collected, AI details/characteristics, and other information will be recorded and posted to a database. The before-mentioned web application will then fetch and display this data for observation purposes in addition to providing general information on the technology used to achieve this.

Reference-style: 
![alt text][/Documentation/BLOCK]
