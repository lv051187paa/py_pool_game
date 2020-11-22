"""Main module"""
import pool
import fishes

import config

if __name__ == '__main__':
    POOL = pool.Pool()
    POOL.fill(fishes.Predator, int(config.CONFIG['App']['Predators']))
    POOL.fill(fishes.Victim, int(config.CONFIG['App']['Victims']))
    for i in range(config.get_ticks()):
        print(POOL)
        POOL.tick()
