# paradigms_final_project

sample project with twisted: https://github.com/bdevorem/tanks
sample game: https://github.com/patrick333/typical-python-games

Player:
	-move function takes in key that user has pressed to move the player in different directions
	-update function checks through list of enemies --> if enemy collision, remove enemy and decrease hit point;
	also check fire attribute --> if true, generate bullet
	-fire attribute is set to true when user left clicks and set to false when user releases

Enemy:
	-update function continuously moves object downward with random speed
	-speed attribute that is set in init() function
	-hit point attribute which is decreased when hit by player bullet; once it reaches 0, remove enemy
	-check through list of bullets to see if it collides with self; if it collides, remove bullet from list of bullets
	-once enemy y-value exceeds that of the screen, remove enemy from the game

Bullet:
	-update its position on every tick (continuously moving upwards)

Gampespace (in host and client):

	-initialize game objects:
		    list of enemies (only host generates enemies)
		    list of bullets
		    players 1 and 2
		    add_enemy_rate
		    enemy_count

	-start up event loop:
	       if event.type == KEYDOWN, then call player.move() function
	       if event.type == MOUSEDOWN, then set player.fire = true
	       if event.type == MOUSEUP, then set player.fire = false

	       ** IN HOST **
	       if enemy_count == add_enemy_rate, generate new enemy with random speed

	-call update function for all sprite objects