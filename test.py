from activities import backtrack, follow_the_food
from settings import settings
from main import Arena
import arcade


def update_settings():
    settings.SCREEN_TITLE = "Antology TEST"
    settings.SCREEN_WIDTH = 300
    settings.SCREEN_HEIGHT = 300

    settings.DRAW_BASE = False
    settings.NUM_WALLS = 0
    settings.NUM_ANTS = 1
    settings.NUM_FOOD_BLOBS = 0
    settings.FOOD_BLOB_SIZE = 2
    settings.SCALE = 6
    settings.MAX_FPS = 4

    settings.RANDOM_DIRECTIONS = [0]
    settings.RANDOM_SPEEDCHANGE = [0]
    settings.EXPLORATION_FRACTION = 0

    settings.WALL_MIN = 10 * settings.SCALE
    settings.WALL_MAX = 50 * settings.SCALE
    settings.WALL_THICKNESS = 6 * settings.SCALE


def check_state(generation, arena):
    ant = arena.ant_list[0]
    x = ant.center_x
    y = ant.center_y
    angle = ant.angle
    activity = ant.activity
    if arena.food_list:
        food = arena.food_list[0]
        food_x = food.center_x
        food_y = food.center_y
        dx = food_x - x
        dy = food_y - y
    if generation == 3:
        assert x == 150
        ant.angle = 90  #!
    elif generation == 4:
        assert angle == 90
    elif generation == 5:
        assert angle == 90
    elif generation == 6:
        ant.angle = 0
    elif generation in range(7, 15):
        assert len(ant.back_track_path) + generation == 15
        assert activity == backtrack
    elif generation in range(15, 21):
        assert activity == follow_the_food
        assert len(ant.path_to_food) == 8
    elif generation == 19:
        assert True
    elif generation == 20:
        assert True
        assert ant.food_search_timer == 10
    elif generation == 21:

        assert True
    elif generation == 22:
        assert activity == follow_the_food
    elif generation == 23:
        assert True
    elif generation == 24:
        assert activity == backtrack
        assert ant.food_search_timer == 0
        assert len(ant.back_track_path) == 9
    elif generation == 25:
        assert True
    elif generation == 26:
        assert True
    elif generation == 27:
        assert True
    elif generation == 28:
        assert True


if __name__ == "__main__":
    update_settings()

    window = Arena(
        settings.SCREEN_WIDTH,
        settings.SCREEN_HEIGHT,
        settings.SCREEN_TITLE,
        generation_callback=check_state,
    )
    window.setup()
    window.set_location(1140, 400)
    window.create_food_blob(size=settings.FOOD_BLOB_SIZE, start_coo=(110, 40))
    arcade.run()
