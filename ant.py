import random
from arcade import Sprite, load_texture, check_for_collision_with_list
from activities import explore, backtrack
from path import Path

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        load_texture(filename),
        load_texture(filename, mirrored=True)
    ]

class Ant(Sprite):

    def __init__(self, x, y, arena, scale=1, activity='wander'):
        super().__init__(center_x=x, center_y=y, scale=scale)
        self.arena = arena
        self.speed = 1
        self.textures = {'black':load_texture_pair('graphics/ant_black.png'),
                         'green': load_texture_pair('graphics/ant_green.png')}
        self.cur_texture = 0
        self.cur_texture_set = 'black'
        self.activity = explore
        self.age = 0
        self.path = Path((x,y))
        self.path.testmode = False

    def move(self):
        self.cur_texture = 1-self.cur_texture
        self.texture = self.textures[self.cur_texture_set][self.cur_texture]

        if self.activity == explore:

            explore( self )
            if check_for_collision_with_list(self, self.arena.wall_list):
                backtrack(self)

            self.age +=1
            #if self.age == 300:
            #    self.activity = backtrack
            #    print( 'backtrack', len(self.path))
            food_list = check_for_collision_with_list(self, self.arena.food_list)
            if food_list:
                self.arena.food_list.remove( food_list[0])
                self.activity = backtrack
                self.cur_texture_set = 'green'

        elif self.activity == backtrack:
            if not backtrack(self):
                self.age = 0
                self.activity = explore
                self.cur_texture_set = 'black'

        self.update()

