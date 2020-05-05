import random
from arcade import Sprite, load_texture, check_for_collision_with_list
from activities import explore, backtrack, follow_the_food, find_the_food
from path import Path


class Ant(Sprite):
    def __init__(self, x, y, arena, colony, scale=1, activity="wander"):
        super().__init__(center_x=x, center_y=y, scale=scale)
        self.arena = arena
        self.colony = colony
        self.speed = 1
        self.textures = {
            "black": load_texture("graphics/ant_black.png"),
            "green": load_texture("graphics/ant_green.png"),
            "red": load_texture("graphics/ant_red.png"),
            "blue": load_texture("graphics/ant_blue.png"),
            "black_green": load_texture("graphics/ant_black_green.png"),
        }
        self.set_activity(explore)
        self.back_track_path = Path((x, y))
        self.food_search_timer = 0  # Used to get a limited number of turns to find food at end of promising path

    def move(self):
        if self.activity in (explore, find_the_food):
            # Ant is exploring the environment in search of food
            explore(self)
            if check_for_collision_with_list(self, self.arena.wall_list):
                # Hit a wall, backup
                backtrack(self)

            food_list = check_for_collision_with_list(self, self.arena.food_list)
            if food_list:
                # Food found! Take it and back to the colony
                self.arena.food_list.remove(food_list[0])
                # assert self.back_track_path.is_valid()
                self.colony.found_food(self.back_track_path)
                self.set_activity(backtrack)
                self.food_search_timer = 0

            elif self.food_search_timer:
                # Ant followed the path to food and is now at the end of it. Where is it?
                self.food_search_timer -= 1
                if not self.food_search_timer:
                    # Searched at the end of the path but no food in sight. Report and continue exploring
                    # assert self.path_to_food.is_valid()
                    self.colony.no_food_at(self.path_to_food)
                    self.set_activity(explore)
            elif random.random() < 0.001:
                self.set_activity(backtrack)
                self.texture = self.textures["black_green"]
        elif self.activity == backtrack:
            # Ant has found food and is tracing back it's steps to the colony
            if not backtrack(self):
                # No more backtracking left. We're back at the colony.
                self.colony.deliver_food()
                self.path_to_food = self.colony.get_path_to_follow()

                if self.path_to_food:
                    # assert self.path_to_food.is_valid()
                    # Colony has instructed this ant to follow a path to food
                    self.set_activity(follow_the_food)
                else:
                    # Colony has instructed this ant to go and find food
                    self.set_activity(explore)

        elif self.activity == follow_the_food:
            # Ant is following a path to where food should be
            if not follow_the_food(self):
                # End of the path, explore and get 10 turns to find the food
                self.back_track_path = self.path_to_food.reverse()
                # assert self.back_track_path.is_valid()
                # assert self.back_track_path.is_valid()
                self.food_search_timer = 10
                self.set_activity(explore)
                self.texture = self.textures["blue"]

        self.update()

    def set_activity(self, activity):
        self.activity = activity
        self.texture = self.textures[self.activity.color]
        # if activity == explore:
        #     self.texture = self.textures['black']
        # else:
        #      self.texture = self.textures['green']

    def move_to(self, coo):
        dx = coo[0] - self.center_x
        dy = coo[1] - self.center_y

        if dx < 0:
            self.angle = 90
        elif dx > 0:
            self.angle = 270
        elif dy > 0:
            self.angle = 0
        else:
            self.angle = 180
        self.speed = abs(dx) + abs(dy)
        self.center_x = coo[0]
        self.center_y = coo[1]
