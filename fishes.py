"""Fish module describes fish behavior"""
import random
import json

import pool

X, Y = 0, 1


class Fish:
    """
    Fish class.
    Methods descriptions goes here
    """
    def __init__(self, x, y):
        """Fish init method description"""
        self._pos = [x, y]
        self._life_counter = 10
        self._born_rate = 0
        self._born_num = 0
        self._is_not_hungry = 0

    def get_pos(self):
        """get fish position function"""
        return self._pos

    def move(self, pool_var: pool.Pool) -> None:
        """Move method"""
        self._life_counter -= 1
        self._move(pool_var)
        self.place_in_bounds(pool_var)

    def is_alive(self):
        """Fish method description"""
        return self._life_counter > 0

    def _move(self, pool_var: pool.Pool):
        """Fish method description"""

    @staticmethod
    def is_victim() -> bool:
        """Fish method description"""
        return False

    def place_in_bounds(self, pool_var: pool.Pool):
        """Fish method description"""
        try:
            self._pos[X] = min(max(self._pos[X], 0),
                               pool_var.get_size()[X] - 1)
            self._pos[Y] = min(max(self._pos[Y], 0),
                               pool_var.get_size()[Y] - 1)
        except ValueError:
            print("Oooops!")

    def eat(self, pool_var: pool.Pool):
        """Fish method description"""

    def born(self, pool_var: pool.Pool):
        """Fish method description"""
        if random.randint(1, 10) < self._born_rate:
            pool_var.fill(self.__class__, self._born_num)


class Predator(Fish):
    """Predator class with methods"""
    with open("predator.json", 'rt') as f:
        state = json.load(f)

    with open('predator.json', 'rt') as f:
        predator_state = json.load(f)

    def __init__(self, x, y):
        super().__init__(x, y)
        self.__dict__.update(self.state)

    def _move(self, pool_var: pool.Pool):
        self._is_not_hungry -= 1
        victim = pool_var.get_nearest_victim(*self._pos)
        self._pos[X] += 2 if victim[X] > self._pos[X] else -2
        self._pos[Y] += 2 if victim[Y] > self._pos[Y] else -2

    def eat(self, pool_var: pool.Pool) -> None:
        """
        Eat method description
        """
        victims = pool_var.get_victim(self.get_pos())
        if victims:
            self._is_not_hungry += 3
            for victim in victims:
                pool_var.kill(victim)

    def __repr__(self):
        return "P"

    def is_alive(self):
        return super().is_alive() and self._is_not_hungry > 0


class Victim(Fish):
    """Victim class with methods"""
    with open("victim.json", 'rt') as f:
        state = json.load(f)

    def __init__(self, x, y):
        super().__init__(x, y)
        self.__dict__.update(self.state)

    def _move(self, pool_var: pool.Pool):
        self._pos[X] += random.randint(-1, 1)
        self._pos[Y] += random.randint(-1, 1)

    def __repr__(self):
        return "V"

    def is_victim(self):
        return True
