import arcade
import random
import math
import os

SPRITE_SCALING_PLAYER = 0.1
SPRITE_SCALING_COIN = 0.5
SPRITE_SCALING_WALL = 0.5
SPRITE_SCALING_BULLET = 0.8
SPRITE_SCALING_ENEMY = 0.8
SCREEN_WIDTH = 805
SCREEN_HEIGHT = 700
MOVEMENT_SPEED = 6
BULLET_SPEED = 8

INSTRUCTIONS_PAGE_0 = 0
INSTRUCTIONS_PAGE_1 = 1
GAME_RUNNING = 2
GAME_OVER = 3


#Need a class for walls, player, enemies, lasers, coins/upgrades
class Walls(arcade.Sprite):
    def __init__(self):
        """Creates the wall Sprite"""
        super().__init__("ArcadeImages/box.png", SPRITE_SCALING_WALL)

class Enemies(arcade.Sprite):
    def __init__(self, enemySpeed):
        """Creates the enemy Sprite"""
        super().__init__("ArcadeImages/slimeWalk1.png", SPRITE_SCALING_ENEMY)
        self.enemySpeed = enemySpeed
    
    def follow_sprite(self, player_sprite, enemySpeed):
        """
        This function will move the current sprite towards whatever
        other sprite is specified as a parameter.

        We use the 'min' function here to get the sprite to line up with
        the target sprite, and not jump around if the sprite is not off
        an exact multiple of SPRITE_SPEED.
        """

        self.center_x += self.change_x
        self.center_y += self.change_y
        start_x = self.center_x
        start_y = self.center_y

        # Get the destination location for the bullet
        dest_x = player_sprite.center_x
        dest_y = player_sprite.center_y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        self.change_x = math.cos(angle) * enemySpeed
        self.change_y = math.sin(angle) * enemySpeed

class Bullet(arcade.Sprite):
    """Creates Bullet sprite"""
    def __init__(self):
        """creates the wall Sprite"""
        super().__init__("ArcadeImages/arrow_01c.png", SPRITE_SCALING_BULLET)

class Player(arcade.Sprite):
    def __init__(self):
        """Creates the player Sprite"""
        super().__init__("ArcadeImages/pikachu.png", SPRITE_SCALING_PLAYER)
        self.center_x = SCREEN_HEIGHT//2
        self.center_y = SCREEN_WIDTH//2

    def update(self):
        """Updates the player Sprite"""
        if self.center_x < 50:   #if the player is out of bounds, keep them in the boundary specified so that they don't run into the walls
            self.center_x = 50
        if self.center_x > 750:
            self.center_x = 750
        if self.center_y <50:
            self.center_y = 50
        if self.center_y > 650:
            self.center_y = 650
        else:       #(self.center_x >= 50 or self.center_x <= 750) and (self.center_y >= 50 or self.center_y <=650)
            #if player is not out of bounds, update their position based on their keyboard and mouse movements
            self.center_x += self.change_x
            self.center_y += self.change_y

class MyGame(arcade.Window):
    """Main application class."""
    def __init__(self, width, height):
        """Initializer"""
        super().__init__(width, height, "Pikachu Rough 'em Up!")
        #Makes Mouse disappear when on screen
        self.set_mouse_visible(False)

        #Variables that hold the sprite list
        self.player_list = None
        self.wall_list = None
        self.bullet_list = None
        self.enemy_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0
        self.game_over = False

    
        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Set up walls info
        self.leftWall = None
        self.topWall = None
        self.rightWall = None
        self.bottomWall = None

        #Set up enemies infor
        self.topEnemy = None
        self.bottomEnemy = None
        self.rightEnemy = None
        self.leftEnemy = None

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)


    def setup(self):
        """ Set up the game and initialize the variables. """
        self.score = 0
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.current_state = INSTRUCTIONS_PAGE_0

        #Set up the player
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        #Set up top enemy
        self.topEnemy = Enemies(1)
        self.topEnemy.center_x = 420
        self.topEnemy.center_y = SCREEN_HEIGHT - self.topEnemy.height
        self.enemy_list.append(self.topEnemy)

        #Set up bottom enemy
        self.bottomEnemy = Enemies(1)
        self.bottomEnemy.center_x = 420
        self.bottomEnemy.center_y = self.bottomEnemy.height
        self.enemy_list.append(self.bottomEnemy)

        #Set up right enemy
        self.rightEnemy = Enemies(1)
        self.rightEnemy.center_x = 0
        self.rightEnemy.center_y = SCREEN_HEIGHT//2
        self.enemy_list.append(self.rightEnemy)

        #Set up left enemy
        self.leftEnemy = Enemies(1)
        self.leftEnemy.center_x = SCREEN_WIDTH - self.leftEnemy.width
        self.leftEnemy.center_y = SCREEN_HEIGHT//2
        self.enemy_list.append(self.leftEnemy)

        # Create a top row of boxes
        for x in range(0, SCREEN_WIDTH, 35):
            self.topWall = Walls()
            self.topWall.center_x = x
            self.topWall.center_y = SCREEN_HEIGHT-10
            if x == 350 or x == 385 or x == 420 or x == 455:
                self.topWall.kill()
            else:
                self.wall_list.append(self.topWall)

        # Create a bottom row of boxes
        for x in range(0, SCREEN_WIDTH, 35):
            self.bottomWall = Walls()
            self.bottomWall.center_x = x
            self.bottomWall.center_y = 15
            if x== 350 or x == 385 or x == 420 or x == 455:
                self.bottomWall.kill()
            else: 
                self.wall_list.append(self.bottomWall)

        # Create a right column of boxes
        for y in range(0, SCREEN_HEIGHT+1, 35):
            self.rightWall = Walls()
            self.rightWall.center_x = SCREEN_WIDTH-10
            self.rightWall.center_y = y
            if y == 280 or y == 315 or y == 350 or y == 385:
                self.rightWall.kill()
            else:
                self.wall_list.append(self.rightWall)

        # Create a left column of boxes
        for y in range(0, SCREEN_HEIGHT, 35):
            self.leftWall = Walls()
            self.leftWall.center_x = 15
            self.leftWall.center_y = y
            if y == 280 or y == 315 or y == 350 or y == 385:
                self.leftWall.kill()
            else:
                self.wall_list.append(self.leftWall)

        arcade.set_background_color(arcade.color.AMAZON)

        #Set up instructions
        self.instructions = []
        texture = arcade.load_texture("ArcadeImages/textfx.png",)
        self.instructions.append(texture)

        texture = arcade.load_texture("ArcadeImages/textfx.png")
        self.instructions.append(texture)

    def draw_instructions(self, page_number):
        #Draws the instructions screen
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

    def draw_game(self):
        #Draws the main game
        self.player_list.draw()
        self.enemy_list.draw()
        self.wall_list.draw()
        self.bullet_list.draw()

    def draw_game_over(self):
        """Draw "Game over" across the screen."""
        output = "Game Over"
        arcade.draw_text(output, 240, 400, arcade.color.WHITE, 54)

        output = "Your score is" + " " + str(self.score)
        arcade.draw_text(output, 300, 300, arcade.color.WHITE, 24)

        output = "Click to restart"
        arcade.draw_text(output, 310, 100, arcade.color.WHITE, 24)


    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        arcade.start_render()
        if self.current_state == INSTRUCTIONS_PAGE_0:
            self.draw_instructions(0)
        elif self.current_state == INSTRUCTIONS_PAGE_1:
            self.draw_instructions(1)
        elif self.current_state == GAME_RUNNING:
            self.draw_game()
        else:
            self.draw_game()
            self.draw_game_over()


    
    def draw_game(self):
        """Render the screen."""
        arcade.start_render()

        # Draw all the sprites.
        self.player_list.draw()
        self.enemy_list.draw()
        self.wall_list.draw()
        self.bullet_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        bullet = Bullet()
        # Change states as needed.
        if self.current_state == INSTRUCTIONS_PAGE_0:
            # Next page of instructions.
            self.current_state = INSTRUCTIONS_PAGE_1
        elif self.current_state == INSTRUCTIONS_PAGE_1:
            # Start the game
            self.setup()
            self.current_state = GAME_RUNNING
        elif self.current_state == GAME_OVER:
            # Restart the game.
            self.setup()
            self.current_state = GAME_RUNNING



        if self.current_state == INSTRUCTIONS_PAGE_0:
            # Next page of instructions.
            self.current_state = INSTRUCTIONS_PAGE_1
        elif self.current_state == INSTRUCTIONS_PAGE_1:
            # Start the game
            self.setup()
            self.current_state = GAME_RUNNING
        elif self.current_state == GAME_OVER:
            # Restart the game.
            self.setup()
            self.current_state = GAME_RUNNING
        
        #Movement of character
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True
        
        #Shoot bullets
        elif key == arcade.key.W:
            # Position the bullet at the player's current location
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            bullet.center_x = start_x
            bullet.center_y = start_y
            #Shoot up
            bullet.change_y = BULLET_SPEED
        elif key == arcade.key.S:
             # Position the bullet at the player's current location
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            bullet.center_x = start_x
            bullet.center_y = start_y
            #Shoot up
            bullet.change_y = -BULLET_SPEED
        elif key == arcade.key.A:
            # Position the bullet at the player's current location
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            bullet.center_x = start_x
            bullet.center_y = start_y
            #Shoot up
            bullet.change_x = -BULLET_SPEED
        elif key == arcade.key.D:
            # Position the bullet at the player's current location
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            bullet.center_x = start_x
            bullet.center_y = start_y
            #Shoot up
            bullet.change_x = BULLET_SPEED

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    """def on_mouse_motion(self,x,y,dx,dy):
        #We originally planned on moving the character with the arrow keys but
        #Since our game plan was originally intended to be used with the keyboard
        #We docstringed out this method. We have implemented it and it does work once the docstrings are removed
        #But we believe the game would be best experienced without the use of the mouse.
        #We believe that for the project in the following years, students should be given the choice
        #As to whether or not they wish to use the mouse for their game
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y"""
    
   
    def update(self, delta_time):
        """Update game changes from user/in game"""

        # Only move and do things if the game is running.
        if self.current_state == GAME_RUNNING:
            # Call update on all sprites (The sprites don't do much in this
            # example though.)
            self.player_list.update()

        # Calculate speed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        #Enemy follow player
        for enemy in self.enemy_list:
            enemy.follow_sprite(self.player_sprite, enemy.enemySpeed)
       
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED

        self.player_list.update()
        self.enemy_list.update()
        self.bullet_list.update()

        # Loop through each bullet
        for bullet in self.bullet_list:
            # Check this bullet to see if it hit a enemy
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            # If it did, get rid of the bullet
            if len(hit_list) > 0:
                bullet.kill()
            # For every enemy we hit, add to the score and remove the coin
            for enemy in hit_list:
                if enemy == self.topEnemy:
                    self.topEnemy = Enemies(enemy.enemySpeed*1.1)
                    self.topEnemy.center_x = 420
                    self.topEnemy.center_y = SCREEN_HEIGHT - self.topEnemy.height
                    enemy.kill()
                    self.score += 1
                    self.enemy_list.append(self.topEnemy)
                if enemy == self.bottomEnemy:
                    self.bottomEnemy = Enemies(enemy.enemySpeed*1.1)
                    self.bottomEnemy.center_x = 420
                    self.bottomEnemy.center_y = self.bottomEnemy.height
                    enemy.kill()
                    self.score += 1
                    self.enemy_list.append(self.bottomEnemy)
                if enemy == self.rightEnemy:
                    self.rightEnemy = Enemies(enemy.enemySpeed*1.1)
                    self.rightEnemy.center_x = 0
                    self.rightEnemy.center_y = SCREEN_HEIGHT//2
                    enemy.kill()
                    self.score += 1
                    self.enemy_list.append(self.rightEnemy)
                if enemy == self.leftEnemy:
                    self.leftEnemy = Enemies(enemy.enemySpeed*1.1)
                    self.leftEnemy.center_x = SCREEN_WIDTH - self.leftEnemy.width
                    self.leftEnemy.center_y = SCREEN_HEIGHT//2
                    enemy.kill()
                    self.score += 1
                    self.enemy_list.append(self.leftEnemy)

            # If the bullet flies off-screen, remove it.
            if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                bullet.kill()

        # Generate a list of all sprites that collided with the player.

        enemy_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
        if len(enemy_hit_list) > 0:
            self.current_state = GAME_OVER

        


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()


"""     if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1"""