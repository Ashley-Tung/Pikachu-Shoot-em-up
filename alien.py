"""BASIC GAME OUTLINE"""

import random
import arcade

# -----CONSTANTS-----
# Original Values:
# SPRITE_SCALING_PLAYER = 0.5
# SPRITE_SCALING_ALIEN = 0.1
# SPRITE_SCALING_WALL = 1.2

SPRITE_SCALING_PLAYER = 0.2
SPRITE_SCALING_ALIEN = 0.1
SPRITE_SCALING_WALL = 1.2

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

INSTRUCTIONS = 0
GAME = 1
GAME_OVER = 2

NUMBER_ALIENS = 1

MOVEMENT_SPEED = 4

WALL_WIDTH = 20

class Alien(arcade.Sprite):

    def __init__(self):
        """creates the Alien Sprite"""
        super().__init__("Images/alien2.png", SPRITE_SCALING_ALIEN)
        self.change_x = random.choice([-1, 1])
        self.change_y = random.choice([-1, 1])

    def update(self):
        """updates the alien Sprite"""
        if random.randrange(150) == 10:
            self.center_x = random.randint(WALL_WIDTH, SCREEN_WIDTH - WALL_WIDTH)
            self.center_y = random.randint(WALL_WIDTH, SCREEN_HEIGHT - WALL_WIDTH)

        self.center_x += self.change_x
        self.center_y += self.change_y

class Player(arcade.Sprite):

    def __init__(self):
        """Creates the character Sprite"""
        super().__init__("Images/pikachu.png", SPRITE_SCALING_PLAYER) #No chipBlue image was provided so I used my own image
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        

class Wall(arcade.Sprite):
    """def __init__(self, orientation):
        creates the wall Sprite
        if orientation == "horizontal":
            super().__init__("Images/box.png", SPRITE_SCALING_WALL) #As with these, I used my own image, as I do not have these
        elif orientation == "vertical":
            super().__init__("Images/boxAlt.png", SPRITE_SCALING_WALL)"""
    def __init__(self):    
        super().__init__("Images/box.png", SPRITE_SCALING_WALL)

class MyGame(arcade.Window):
    """Our custom Window class"""
    def __init__(self):
        """initializer"""
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Pikachu Chase (Arcade Starter)")
        self.set_mouse_visible(False)

        # Variables that will hold sprite lists
        self.player_list = None
        self.alien_list = None
        self.wall_list = None

        # Set up player info
        self.player_sprite = None

        # Set up walls info
        self.leftWall = None
        self.topWall = None
        self.rightWall = None
        self.bottomWall = None

        self.level = INSTRUCTIONS
        self.end_message = "To infinity and beyond!"

        # Set background
        arcade.set_background_color((0, 0, 0))

    def draw_instructions(self):
        """draws the instructions screen"""
        arcade.draw_text("Use arrow keys to help Pikachu hit the alien \n Press any key to continue",
                        SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, arcade.color.WHITE, 30, align="center", anchor_x="center",
                        anchor_y="center")

    def draw_game(self):
        """draws the main game"""
        self.player_list.draw()
        self.alien_list.draw()
        self.wall_list.draw()

        # Add other drawing code here

    def draw_game_over(self):
        """Draws the game over screen"""
        #We will go from GAME OVER back to instructions
        self.draw_game()
        arcade.draw_text(self.end_message + "\n Press any key to play again", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                        arcade.color.WHITE, 20, align="center", anchor_x="center", anchor_y="center")
        self.setup()
        self.draw_instructions()

    def setup(self):
        """Set up the game and initialize the variables"""

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.alien_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        self.level = INSTRUCTIONS

        # Set up the player
        self.player_sprite = Player()
        self.player_list.append(self.player_sprite)

        # Create the aliens
        # This code assumes you make multiple aliens. This shows you how you can do so
        for i in range(NUMBER_ALIENS):
            alien = Alien()

            # Position the alien randomly
            alien.center_x = random.randrange(WALL_WIDTH, SCREEN_WIDTH - WALL_WIDTH)
            alien.center_y = random.randrange(WALL_WIDTH, SCREEN_HEIGHT - WALL_WIDTH)

            # Add the alien to the alien list
            self.alien_list.append(alien)

        """# Create the walls
        self.leftWall = Wall("vertical")
        self.leftWall.center_x = 0
        self.leftWall.center_y = SCREEN_HEIGHT // 2
        self.wall_list.append(self.leftWall)

        self.topWall = Wall("horizontal")
        self.topWall.center_x = SCREEN_WIDTH // 2
        self.topWall.center_y = SCREEN_HEIGHT
        self.wall_list.append(self.topWall)

        self.rightWall = Wall("vertical")
        self.rightWall.center_x = SCREEN_WIDTH 
        self.rightWall.center_y = SCREEN_HEIGHT // 2
        self.wall_list.append(self.rightWall)

        self.bottomWall = Wall("horizontal")
        self.bottomWall.center_x = SCREEN_WIDTH // 2
        self.bottomWall.center_y = 100
        self.wall_list.append(self.bottomWall)"""

        # Create a top row of boxes
        for x in range(0, SCREEN_WIDTH, 35):
            self.topWall = Wall()
            self.topWall.center_x = x
            self.topWall.center_y = SCREEN_HEIGHT-10
            if x == 350 or x == 385 or x == 420 or x == 455:
                self.topWall.kill()
            else:
                self.wall_list.append(self.topWall)
            
         # Create a bottom row of boxes
        for x in range(0, SCREEN_WIDTH, 35):
            self.bottomWall = Wall()
            self.bottomWall.center_x = x
            self.bottomWall.center_y = 15
            if x== 350 or x == 385 or x == 420 or x == 455:
                self.bottomWall.kill()
            else: 
                self.wall_list.append(self.bottomWall)

        # Create a right column of boxes
        for y in range(0, SCREEN_HEIGHT+1, 35):
            self.rightWall = Wall()
            self.rightWall.center_x = SCREEN_WIDTH-10
            self.rightWall.center_y = y
            if y == 280 or y == 315 or y == 350 or y == 385:
                self.rightWall.kill()
            else:
                self.wall_list.append(self.rightWall)

        # Create a left column of boxes
        for y in range(0, SCREEN_HEIGHT, 35):
            self.leftWall = Wall()
            self.leftWall.center_x = 15
            self.leftWall.center_y = y
            if y == 280 or y == 315 or y == 350 or y == 385:
                self.leftWall.kill()
            else:
                self.wall_list.append(self.leftWall)

    def on_draw(self):
        """Draw everything"""
        arcade.start_render()

        if self.level == INSTRUCTIONS:
            self.draw_instructions()

        elif self.level == GAME:
            self.draw_game()

        elif self.level == GAME_OVER:
            self.draw_game_over()


    def update(self, delta_time):
        """Movement and game logic"""
        # Call update on all sprites
        # This moves the sprites based on each of their update functions (either the default or one you wrote)
        self.player_list.update()
        self.alien_list.update()
        self.wall_list.update()

        # Add any other game logic here

        # ----------COLLISIONS CODE-----------

        # Check for collisions with all walls
        if arcade.check_for_collision(self.player_sprite, self.leftWall):
            self.player_sprite.change_x *= 0
        
        if arcade.check_for_collision(self.player_sprite, self.topWall):
            self.player_sprite.change_y *= 0
        
        if arcade.check_for_collision(self.player_sprite, self.rightWall):
            self.player_sprite.change_x *= 0
        
        if arcade.check_for_collision(self.player_sprite, self.bottomWall):
            self.player_sprite.change_y *= 0


        # check if any of the aliens have collided with a wall
        for alien in self.alien_list:
            if arcade.check_for_collision(alien, self.leftWall):
                alien.change_x *= -1
            
            if arcade.check_for_collision(alien, self.topWall):
                alien.change_y *= -1

            if arcade.check_for_collision(alien, self.rightWall):
                alien.change_x *= -1

            if arcade.check_for_collision(alien, self.bottomWall):
                alien.change_y *= -1

        alien_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.alien_list)
        if len(alien_hit_list) > 0:
            self.level = GAME_OVER

        # ---------END OF COLLISIONS CODE-----------

    def on_key_press(self, key, modifiers):
        """Called when a key is pressed"""
        if self.level == INSTRUCTIONS:
            self.level = GAME

        elif self.level == GAME:
            if key == arcade.key.UP:
                self.player_sprite.change_y += MOVEMENT_SPEED
            if key == arcade.key.LEFT:
                self.player_sprite.change_x -= MOVEMENT_SPEED
            if key == arcade.key.DOWN:
                self.player_sprite.change_y -= MOVEMENT_SPEED
            if key == arcade.key.RIGHT:
                self.player_sprite.change_x += MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when a key is released"""
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_mouse_press(self, x, y, button, modifiers):
        """Called when a mouse button is pressed"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player_sprite.center_x = x
            self.player_sprite.center_y = y

    def on_mouse_release(self, x, y, button, modifiers):
        """Called when a mouse button is released"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player_sprite.center_x = SCREEN_HEIGHT//2
            self.player_sprite.center_y = SCREEN_WIDTH//2

    def on_mouse_motion(self, x, y, dx, dy):
        """Called when the mouse is moved"""
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

def main():
    """Main method"""
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()

