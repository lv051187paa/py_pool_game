"""Config module"""
import configparser


CONFIG = configparser.ConfigParser()
CONFIG.read('pool.ini')


def get_ticks():
    """Return tick"""
    return int(CONFIG['App']['Ticks'])
