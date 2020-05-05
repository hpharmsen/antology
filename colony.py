import random
from settings import settings


class Colony:
    def __init__(self):
        self.food_paths = []
        self.energy = 0
        self.age = 0

    def found_food(self, path):
        # path is the path back to the colony to follow it, reverse it
        path = path.reverse()
        self.food_paths += [path]

    def no_food_at(self, path):
        # Ant detected that there's no food at this path's end. Remove it.
        try:
            self.food_paths.remove(path)
        except:
            print("path cannot be removed")

    def get_path_to_follow(self):
        if not self.food_paths or random.random() < settings.EXPLORATION_FRACTION:
            return
        return random.choice(self.food_paths)

    def deliver_food(self, amount=1):
        self.energy += amount

    def tick(self):
        self.age += 1

    def food_per_turn(self):
        return self.energy / self.age
