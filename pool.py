"""Pool module"""
import random

import math

import config


POOL_WIDTH = int(config.CONFIG['Pool']['Width'])
POOL_HEIGHT = int(config.CONFIG['Pool']['Height'])


class Pool:
    """Pool class description"""
    def __init__(self):
        self._width = POOL_WIDTH
        self._height = POOL_HEIGHT
        self._fishes = []

    def get_size(self):
        """get size metho"""
        return self._width, self._height

    def get_fishes(self):
        """return fiches array"""
        return self._fishes

    def fill(self, fish_type, number: int):
        """fill metho"""
        self._fishes += [
            fish_type(
                random.randint(0, self._width - 1),
                random.randint(0, self._height - 1)
            ) for _ in range(number)]

    def __str__(self):
        size = '+' + '-'*self._width + '+\n'
        position = [[' ']*self._width for _ in range(self._height)]
        for fish in self._fishes:
            position[fish.get_pos()[0]][fish.get_pos()[1]] = repr(fish)
        for row in position:
            size += '|' + ''.join(row) + '|\n'
        size += '+' + '-'*self._width + '+\n'
        return size

    def tick(self):
        """Tick method"""
        for fish in self._fishes:
            fish.move(self)
            fish.eat(self)

        for fish in self._fishes.copy():
            if not fish.is_alive():
                self.kill(fish)
            else:
                for fish_copy in self._fishes.copy():
                    fish_copy.born(self)

    def get_nearest_victim(self, x_pos, y_pos):
        """get_nearest_victim method"""
        nearest_victims = [fish.get_pos() for fish in self._fishes
                           if fish.is_victim()]
        if not nearest_victims:
            return (0, 0)
        return tuple(min(nearest_victims,
                         key=lambda f: math.hypot(f[0] - x_pos, f[1] - y_pos)))

    def get_victim(self, pos):
        """get_victim method"""
        return [fish for fish in self._fishes
                if fish.get_pos() == pos and fish.is_victim()]

    def kill(self, victim):
        """kill method"""
        self._fishes.remove(victim)
