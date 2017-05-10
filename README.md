Final Project Description:

Team Members: Marykate Williams, Yaoxian Qu

Game Description:

This game is a scrolling shooter arcade game that can be controlled by either
a single player or multiplayer. The player controls a plane which could shoot out 
bullets and have a certain amount of hitpoints allotted. Enemies are randomly generated,
the player's objective is to shoot as many enemies as possible before the hitpoint is
exhausted. The game ends when the player dies. 

Modes:

First, the player has the option to select single player mode or multiplayer mode. 
For single player mode the player simply choose single player mode and the game starts. Multiplayer mode supports gameplay for two players, one player opens host.py and the other client.py.
For multiplayer mode the host has to first select multiplayer option and then the client
selects multiplayer option. The specific machine and port for multiplayer can be changed when necessary, which is explained in the comments of our code. The default is that both the client and the host runs on local machine. (If want to run client on some other machine, simply change the HOST variable in client.py to ash.campus.nd.edu or whichever the host machine is). 

Controls:

The player controls the movement of the plane by w (up), s (down), a (left), d (right). Plane can shoot out bullets when the left mouse button is pressed. 

The hitpoint values for each player is displayed. And the score that the player has gained is also displayed. The player has a initial hp of 100. And each enemy can cause 20 points of hitpoint reduction to the player. 
