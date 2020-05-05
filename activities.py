import random

from arcade import (
    check_for_collision_with_list,
    get_closest_sprite,
    get_distance_between_sprites,
)

from settings import settings


def explore(ant):
    # Check for screen boundaries
    if ant.center_x >= settings.SCREEN_WIDTH:
        ant.angle = 90
    elif ant.center_x < 0:
        ant.angle = 270
    elif ant.center_y >= settings.SCREEN_HEIGHT:
        ant.angle = 180
    elif ant.center_y < 8:
        ant.angle = 0
    else:
        if ant.food_search_timer:
            food_direction = check_for_food(ant)
        else:  # Liever altijd check maar dat is te langzaam
            food_direction = -1

        if food_direction != -1:
            ant.angle = food_direction
        else:
            ant.angle += random.choice(settings.RANDOM_DIRECTIONS)
        ant.angle %= 360

    ant.speed = min(3, max(1, ant.speed + random.choice(settings.RANDOM_SPEEDCHANGE)))
    if ant.angle == 0:
        ant.center_y += ant.speed * ant.scale
    elif ant.angle == 270:
        ant.center_x += ant.speed * ant.scale
    elif ant.angle == 180:
        ant.center_y -= ant.speed * ant.scale
    elif ant.angle == 90:
        ant.center_x -= ant.speed * ant.scale
    else:
        pass
    ant.back_track_path.add((ant.center_x, ant.center_y))

    return (ant.center_x, ant.center_y)


def check_for_food(ant):
    res = get_closest_sprite(ant, ant.arena.food_list)
    if not res:
        return -1
    food, dist = res
    if dist > 10 * settings.SCALE:
        return -1
    dx = food.center_x - ant.center_x
    dy = food.center_y - ant.center_y
    if dy > abs(dx):
        return 0
    if dx > abs(dy):
        return -90
    if -dx > abs(dy):
        return 90
    return -1

    #
    #
    #
    # old_hit_box = ant.hit_box
    #
    # # look forward
    # ant._point_list_cache = None
    # ant.hit_box = [(-SCALE, 0), (-SCALE, SCALE*3), (SCALE, SCALE*3), (SCALE, 0)]
    # if check_for_collision_with_list(ant, ant.arena.food_list):
    #     food_dir = 0
    # else:
    #     # look left
    #     a = ant.get_adjusted_hit_box()
    #     ant._point_list_cache = None
    #     ant.hit_box = [(-SCALE*3, -SCALE), (-SCALE*3, SCALE), (0, SCALE), (0, -SCALE)]
    #     b = ant.get_adjusted_hit_box()
    #     if check_for_collision_with_list(ant, ant.arena.food_list):
    #         food_dir = 270
    #     else:
    #         # look right
    #         ant._point_list_cache = None
    #         ant.hit_box = [(0, -SCALE), (0, SCALE), (SCALE*3, SCALE), (SCALE*3, -SCALE)]
    #         if check_for_collision_with_list(ant, ant.arena.food_list):
    #             food_dir = 90
    #         else:
    #             food_dir = -1
    # ant.hit_box = old_hit_box
    # return food_dir


def backtrack(ant):
    to_delete = ant.back_track_path.backtrack()
    if to_delete == ant.back_track_path.NONE_VALUE:
        return False

    ant.move_to(to_delete)
    return True


def follow_the_food(ant):
    pos = (ant.center_x, ant.center_y)
    try:
        next = ant.path_to_food.path[pos]
    except:
        assert True
    if next == ant.back_track_path.NONE_VALUE:
        return False
    else:
        ant.move_to(next)
        return True


def find_the_food():
    pass


def follow_path(ant, path):
    to_delete = path.backtrack()
    if to_delete == ant.back_track_path.NONE_VALUE:
        return False

    ant.move_to(to_delete)
    return True


backtrack.color = "green"
explore.color = "black"
follow_the_food.color = "red"
find_the_food.color = "blue"
