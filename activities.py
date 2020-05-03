import random

def explore(ant):
    ant.speed = min(3, max(1, ant.speed + random.choice([-1, 0, 0, 1])))
    if ant.center_x >= 800:
        ant.angle = 270
    elif ant.center_x < 0:
        ant.angle = 90
    elif ant.center_y >= 600:
        ant.angle = 180
    elif ant.center_y < 8:
        ant.angle = 0
    else:
        ant.angle += random.choice([-90, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 90])
        ant.angle %= 360

    if ant.angle == 0:
        ant.center_y += ant.speed * ant.scale
    elif ant.angle == 90:
        ant.center_x += ant.speed * ant.scale
    elif ant.angle == 180:
        ant.center_y -= ant.speed * ant.scale
    elif ant.angle == 270:
        ant.center_x -= ant.speed * ant.scale
    else:
        pass
    ant.path.add((ant.center_x, ant.center_y))

    return (ant.center_x, ant.center_y)


def backtrack(ant):
    to_delete = ant.path.backtrack()
    if to_delete == ant.path.NONE_VALUE:
        return False

    dx = ant.center_x - to_delete[0]
    dy = ant.center_y - to_delete[1]

    if dx < 0:
        ant.angle = 270
    elif dx > 0:
        ant.angle = 90
    elif dy > 0:
        ant.angle = 0
    else:
        ant.angle = 180
    ant.speed = abs( dx ) + abs( dy )
    ant.center_x = to_delete[0]
    ant.center_y = to_delete[1]
    return True