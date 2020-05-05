import arcade
from dataclasses import dataclass


@dataclass()
class Settings:
    SCALE = 1
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700
    SCREEN_TITLE = "Antology"
    DRAW_BASE = True
    NUM_WALLS = 60  # 60
    WALL_COLOR = "#777"
    BASE_COLOR = "#222"
    FOOD_COLOR = arcade.color.APPLE_GREEN
    NUM_FOOD_BLOBS = 5  # 30
    FIELD_COLOR = arcade.color.DARK_VANILLA
    NUM_ANTS = 100
    FOOD_BLOB_SIZE = 10
    MAX_FPS = 33
    RANDOM_DIRECTIONS = [-90, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 90]
    RANDOM_SPEEDCHANGE = [0]  # [-1, 0, 0, 1]

    EXPLORATION_FRACTION = (
        0.25  # Fraction of ants that is sent to explore even when known food exists
    )

    def WALL_MIN(self):
        return 10 * self.SCALE

    def WALL_MAX(self):
        return 50 * self.SCALE

    def WALL_THICKNESS(self):
        return 6 * self.SCALE


settings = Settings()
