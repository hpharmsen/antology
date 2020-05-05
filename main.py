import random
import arcade
from ant import Ant
from colony import Colony

# TODO
# - Food blobs 2x zo groot
# - Food blobs droppen met muis
# - Food blob coo is altijd centrale coo
# - Lijn tekenen bij backtrack
from settings import settings


class Arena(arcade.Window):
    def __init__(self, width, height, title, generation_callback=None):
        super().__init__(width, height, title)

        self.wall_list = arcade.SpriteList(is_static=True, use_spatial_hash=True)
        self.food_list = arcade.SpriteList(is_static=True, use_spatial_hash=True)
        self.ant_list = arcade.SpriteList(use_spatial_hash=False)
        self.physics_engine = None
        if settings.MAX_FPS:
            self.set_update_rate(1 / settings.MAX_FPS)
        self.actual_fps = settings.MAX_FPS  # Initializse to something

        self.generation = 0
        self.generation_callback = generation_callback  # For testing purposes

    def setup(self):

        if settings.DRAW_BASE:
            self.create_base()

        for _ in range(settings.NUM_WALLS):
            self.create_wall()

        for _ in range(settings.NUM_FOOD_BLOBS):
            self.create_food_blob(settings.FOOD_BLOB_SIZE)

        self.colony = Colony()

        for _ in range(settings.NUM_ANTS):
            ant = Ant(
                settings.SCREEN_WIDTH / 2, 0, self, self.colony, scale=settings.SCALE
            )
            self.ant_list.append(ant)

        arcade.set_background_color(settings.FIELD_COLOR)

        if self.generation_callback:
            self.generation_callback(self.generation, self)

    def create_base(self):
        x = settings.SCREEN_WIDTH / 2
        for y in range(0, round(20 * settings.SCALE), settings.WALL_THICKNESS()):
            block = arcade.SpriteSolidColor(
                settings.WALL_THICKNESS(),
                settings.WALL_THICKNESS(),
                settings.BASE_COLOR,
            )
            block.center_x = x - 8 * settings.SCALE
            block.center_y = y
            self.wall_list.append(block)
            block = arcade.SpriteSolidColor(
                settings.WALL_THICKNESS(),
                settings.WALL_THICKNESS(),
                settings.BASE_COLOR,
            )
            block.center_x = x + 8 * settings.SCALE
            block.center_y = y
            self.wall_list.append(block)

    def create_wall(self):
        def block_at(x, y):
            block = arcade.SpriteSolidColor(
                settings.WALL_THICKNESS(),
                settings.WALL_THICKNESS(),
                settings.WALL_COLOR,
            )
            block.center_x = x
            block.center_y = y
            wally.append(block)

        while True:
            wally = []
            length = random.randint(settings.WALL_MIN(), settings.WALL_MAX())
            if random.random() < 0.5:
                # Horizontal
                start_x = random.randint(0, settings.SCREEN_WIDTH - length)
                y = random.randint(0, settings.SCREEN_HEIGHT)
                for x in range(start_x, start_x + length, settings.WALL_THICKNESS()):
                    block_at(x, y)
            else:
                # Vertical
                start_y = random.randint(0, settings.SCREEN_HEIGHT - length)
                x = random.randint(0, settings.SCREEN_WIDTH)
                for y in range(start_y, start_y + length, settings.WALL_THICKNESS()):
                    block_at(x, y)
            for block in wally:
                if arcade.check_for_collision_with_list(block, self.wall_list):
                    break  # Oops, break it off, try a new wall
            else:
                for block in wally:
                    self.wall_list.append(block)
                return

    def create_food_blob(self, size=10, start_coo=None):
        scale = settings.SCALE * 3
        if start_coo:
            start_x, start_y = start_coo
        else:
            start_x = random.randint(0, settings.SCREEN_WIDTH - size * scale)
            start_y = random.randint(0, settings.SCREEN_HEIGHT - size * scale)

        for x in range(start_x, start_x + size * scale, scale):
            for y in range(start_y, start_y + size * scale, scale):
                block = arcade.SpriteSolidColor(scale, scale, settings.FOOD_COLOR)
                block.center_x = x
                block.center_y = y
                if not arcade.check_for_collision_with_list(block, self.wall_list):
                    self.food_list.append(block)

    def on_draw(self):
        # This command has to happen before we start drawing
        arcade.start_render()

        # Draw all the sprites.
        self.wall_list.draw()
        self.food_list.draw()
        for ant in self.ant_list:
            ant.draw()
            # ant.draw_hit_box((255,0,0))

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
        self.colony.tick()
        self.actual_fps = (99 * self.actual_fps + 1 / delta_time) / 100
        food_per_100_turns = self.colony.food_per_turn() * 100
        self.set_caption(
            f"{settings.SCREEN_TITLE} - {self.actual_fps:0.0f} fps, {food_per_100_turns:0.0f} food per 100 turns - {self.generation}"
        )
        arcade.start_render()
        for ant in self.ant_list:
            ant.move()
        self.generation += 1  #!! Dubbel naast colony.tick()
        if self.generation_callback:
            self.generation_callback(self.generation, self)


if __name__ == "__main__":
    window = Arena(settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, settings.SCREEN_TITLE)
    window.setup()
    arcade.run()
