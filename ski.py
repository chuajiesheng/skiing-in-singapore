import unittest


def longest_path(size, grid, current_pos):
    x, y = current_pos
    max_x, max_y = size

    possible_movement = next_possible_movement(max_x, max_y, x, y)
    possible_movement_down = valid_next_movement(current_pos, grid, possible_movement)

    max_path_length = 1
    for next_pos in possible_movement_down:
        max_possible = 1 + longest_path(size, grid, next_pos)
        if max_possible > max_path_length:
            max_path_length = max_possible

    return max_path_length


def valid_next_movement(current_pos, grid, possible_movement):
    x, y = current_pos
    current_level = grid[x][y]

    possible_movement_down = []

    for next_pos in possible_movement:
        next_x, next_y = next_pos
        next_level = grid[next_x][next_y]
        if next_level < current_level:
            possible_movement_down.append(next_pos)

    return possible_movement_down


def next_possible_movement(max_x, max_y, x, y):
    possible_movement = []
    # move up
    if (x - 1) > -1:
        possible_movement.append((x - 1, y))

    # move right
    if (y + 1) < max_y:
        possible_movement.append((x, y + 1))

    # move down
    if (x + 1) < max_x:
        possible_movement.append((x + 1, y))

    # move left
    if (y - 1) > -1:
        possible_movement.append((x, y - 1))
    return possible_movement


class SkiTest(unittest.TestCase):
    def test_longest_path(self):
        size = (1, 1)
        grid = [[1]]
        current_pos = (0, 0)
        res = longest_path(size, grid, current_pos)
        self.assertEqual(res, 1)

    def test_longest_path_2_by_2(self):
        # 4 3
        # 2 1
        size = (2, 2)
        grid = [[4, 3], [2, 1]]
        current_pos = (0, 0)
        res = longest_path(size, grid, current_pos)
        self.assertEqual(res, 3)

    def test_next_possible_movement(self):
        max_x = max_y = 2
        x = y = 0
        res = next_possible_movement(max_x, max_y, x, y)
        self.assertEqual(len(res), 2)
        self.assertTrue((0, 1) in res)
        self.assertTrue((1, 0) in res)

    def test_next_possible_movement_3_by_3(self):
        max_x = max_y = 3
        x = y = 1
        res = next_possible_movement(max_x, max_y, x, y)
        self.assertEqual(len(res), 4)
        self.assertTrue((0, 1) in res)
        self.assertTrue((1, 0) in res)
        self.assertTrue((1, 2) in res)
        self.assertTrue((2, 1) in res)

    def test_valid_next_movement(self):
        grid = [[4, 3], [2, 1]]
        current_pos = (0, 0)
        possible_movement = [(0, 1), (1, 0)]
        res = valid_next_movement(current_pos, grid, possible_movement)
        self.assertEqual(len(res), 2)
        self.assertTrue((0, 1) in res)
        self.assertTrue((1, 0) in res)

    def test_valid_next_movement_3_by_3(self):
        # 6 7 8
        # 5 4 3
        # 3 1 2
        grid = [[6, 7, 8], [5, 4, 3], [3, 1, 2]]
        current_pos = (1, 1)
        possible_movement = [(0, 1), (1, 0), (1, 2), (2, 1)]
        res = valid_next_movement(current_pos, grid, possible_movement)
        self.assertEqual(len(res), 2)
        self.assertTrue((1, 2) in res)
        self.assertTrue((2, 1) in res)


if __name__ == '__main__':
    unittest.main()

