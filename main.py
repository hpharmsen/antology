import random
import arcade
from ant import Ant

SCALE = 2
SCREEN_WIDTH = 580 * SCALE
SCREEN_HEIGHT = 420 * SCALE
SCREEN_TITLE = "Simple Ant"

NUM_WALLS = 60
WALL_MIN = 10 * SCALE
WALL_MAX = 50 * SCALE
WALL_THICKNESS = 6 * SCALE
WALL_COLOR = '#777'
BASE_COLOR = '#222'
FOOD_COLOR = arcade.color.APPLE_GREEN
NUM_FOOD_BLOBS = 30
FIELD_COLOR = arcade.color.DARK_VANILLA
NUM_ANTS = 30
FOOD_BLOB_SIZE = 8


class Arena(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.wall_list = arcade.SpriteList()
        self.food_list = arcade.SpriteList()
        self.ant_list = arcade.SpriteList()
        self.physics_engine = None

    def setup(self):

        self.create_base()
        # # -- Set up the walls
        # # Create a row of boxes
        for _ in range( NUM_WALLS ):
            self.create_wall()

        for _ in range( NUM_FOOD_BLOBS):
            self.create_food_blob(FOOD_BLOB_SIZE)

        for _ in range( NUM_ANTS ):
            ant = Ant(SCREEN_WIDTH/2,0, self, scale=SCALE)
            self.ant_list.append(ant)

        arcade.set_background_color(FIELD_COLOR)

    def create_base(self):
        x = SCREEN_WIDTH / 2
        for y in range( 0, round(20*SCALE), WALL_THICKNESS):
            block = arcade.SpriteSolidColor(WALL_THICKNESS, WALL_THICKNESS, BASE_COLOR)
            block.center_x = x-8*SCALE
            block.center_y = y
            self.wall_list.append(block)
            block = arcade.SpriteSolidColor(WALL_THICKNESS, WALL_THICKNESS, BASE_COLOR)
            block.center_x = x+8*SCALE
            block.center_y = y
            self.wall_list.append(block)

    def create_wall(self):
        def block_at( x, y ):
            block = arcade.SpriteSolidColor(WALL_THICKNESS, WALL_THICKNESS, WALL_COLOR )
            block.center_x = x
            block.center_y = y
            wally.append(block)

        while True:
            wally = []
            length = random.randint( WALL_MIN, WALL_MAX )
            if random.random() < .5:
                # Horizontal
                start_x = random.randint( 0, SCREEN_WIDTH-length )
                y = random.randint( 0, SCREEN_HEIGHT )
                for x in range( start_x, start_x+length, WALL_THICKNESS):
                    block_at( x, y)
            else:
                # Vertical
                start_y = random.randint( 0, SCREEN_HEIGHT-length )
                x = random.randint( 0, SCREEN_WIDTH )
                for y in range( start_y, start_y+length, WALL_THICKNESS):
                    block_at( x, y)
            for block in wally:
                if arcade.check_for_collision_with_list(block, self.wall_list):
                    break # Oops, break it off, try a new wall
            else:
                for block in wally:
                    self.wall_list.append( block )
                return

    def create_food_blob(self, size=10):
        start_x = random.randint( 0, SCREEN_WIDTH-size*SCALE)
        start_y = random.randint( 0, SCREEN_HEIGHT-size*SCALE)
        for x in range( start_x, start_x+size*SCALE, SCALE):
            for y in range(start_y, start_y + size*SCALE, SCALE):
                block = arcade.SpriteSolidColor(SCALE, SCALE, FOOD_COLOR )
                block.center_x = x
                block.center_y = y
                if not arcade.check_for_collision_with_list(block, self.wall_list):
                    self.food_list.append( block )


    def on_draw(self):
        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.wall_list.draw()
        self.food_list.draw()
        for ant in self.ant_list:
            ant.draw()

    # def on_key_press(self, key, modifiers):
    #     """Called whenever a key is pressed. """
    #
    #     if key == arcade.key.UP:
    #         self.player_sprite.change_y = MOVEMENT_SPEED
    #     elif key == arcade.key.DOWN:
    #         self.player_sprite.change_y = -MOVEMENT_SPEED
    #     elif key == arcade.key.LEFT:
    #         self.player_sprite.change_x = -MOVEMENT_SPEED
    #     elif key == arcade.key.RIGHT:
    #         self.player_sprite.change_x = MOVEMENT_SPEED
    #
    # def on_key_release(self, key, modifiers):
    #     """Called when the user releases a key. """
    #
    #     if key == arcade.key.UP or key == arcade.key.DOWN:
    #         self.player_sprite.change_y = 0
    #     elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
    #         self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        arcade.start_render()
        for ant in self.ant_list:
            ant.move()
        #self.physics_engine.update()

        # Generate a list of all sprites that collided with the player.
        #coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

def main():
    """ Main method """
    window = Arena(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()