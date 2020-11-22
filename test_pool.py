"""Tests"""
import unittest
import unittest.mock
import pool
import fishes


class TestPool(unittest.TestCase):
    """Test pool class"""
    def setUp(self) -> None:
        """Test method"""
        self.pool = pool.Pool()

    def test_pool(self):
        """Test method"""
        self.assertEqual(self.pool.get_size(),
                         (10, 10),
                         "Pool size doesn't equal 10x10")

    def test_fill_predators(self):
        """Test method"""
        predators_quantity = 3
        length = len(self.pool.get_fishes())
        self.pool.fill(fishes.Predator, predators_quantity)
        self.assertEqual(len(self.pool.get_fishes()),
                         length + predators_quantity)

    @unittest.mock.patch('random.randint')
    def test_fill_predators_random(self, mock):
        """Test method"""
        mock.side_effect = 0, 1
        self.pool.fill(fishes.Predator, 1)
        self.assertEqual(self.pool.get_fishes()[0].get_pos(), [0, 1])

    @unittest.mock.patch('random.randint')
    def test_nearest_victim(self, mock):
        """Test method"""
        mock.side_effect = 1, 1, 5, 5, 9, 0
        self.pool.fill(fishes.Victim, 3)
        self.assertEqual(self.pool.get_nearest_victim(2, 2), (1, 1))
        self.assertEqual(self.pool.get_nearest_victim(8, 1), (9, 0))

    @unittest.mock.patch('random.randint')
    def test_get_victim(self, mock):
        """Test method"""
        mock.side_effect = 1, 1
        self.pool.fill(fishes.Victim, 1)
        self.assertEqual(self.pool.get_victim([1, 1]),
                         [self.pool.get_fishes()[0]])

    def tearDown(self) -> None:
        """Test method"""


class TestFish(unittest.TestCase):
    """Test fish class"""
    def test_fish_is_in_bounds1(self):
        """Test method"""
        some_value = fishes.Fish(-1, -1)
        some_value.place_in_bounds(pool.Pool())
        self.assertEqual(some_value.get_pos(), [0, 0])

    def test_fish_is_in_bounds2(self):
        """Test method"""
        some_value = fishes.Fish(10, 10)
        some_value.place_in_bounds(pool.Pool())
        self.assertEqual(some_value.get_pos(), [9, 9])


class TestPredator(unittest.TestCase):
    """Test  predator class"""
    def test_predator(self):
        """Test method"""
        predator = fishes.Predator(2, 3)
        self.assertEqual(repr(predator), 'P')

    def test_predator_pos(self):
        """Test method"""
        predator = fishes.Predator(2, 3)
        self.assertEqual(predator.get_pos(), [2, 3])

    @unittest.mock.patch('random.randint')
    def test_predator_move(self, mock):
        """Test method"""
        pool_instance = pool.Pool()
        mock.side_effect = 1, 1, 5, 5
        pool_instance.fill(fishes.Victim, 1)
        pool_instance.fill(fishes.Predator, 1)
        pool_instance.get_fishes()[1].move(pool_instance)
        self.assertEqual(pool_instance.get_fishes()[1].get_pos(), [3, 3])

    @unittest.mock.patch('random.randint')
    def test_predator_eating(self, mock):
        """Test method"""
        pool_instance = pool.Pool()
        mock.side_effect = 1, 1, 1, 1
        pool_instance.fill(fishes.Predator, 1)
        pool_instance.fill(fishes.Victim, 1)
        pool_instance.get_fishes()[0].eat(pool_instance)
        self.assertEqual(len(pool_instance.get_fishes()), 1)


class TestVictim(unittest.TestCase):
    """Test victim class"""
    def test_victim(self):
        """Test method"""
        victim = fishes.Victim(2, 3)
        self.assertEqual(repr(victim), 'V')

    def test_victim_pos(self):
        """Test method"""
        victim = fishes.Victim(2, 3)
        self.assertEqual(victim.get_pos(), [2, 3])

    @unittest.mock.patch('random.randint')
    def test_victim_correct_move(self, mock):
        """Test method"""
        victim = fishes.Victim(2, 3)
        mock.side_effect = 1, 1
        victim.move(pool.Pool())
        self.assertEqual(victim.get_pos(), [3, 4])
