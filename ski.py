import unittest
from itertools import product


def read_file(filename):
    with open(filename) as f:
        content = f.readlines()

    size = map(lambda x: int(x), content[0].strip().split(' '))

    grid = []
    for line in content[1:]:
        elements = map(lambda x: int(x), line.strip().split(' '))
        assert len(elements) == int(size[1])
        grid.append(elements)

    assert len(grid) == size[0]
    return (size[0], size[1]), grid


def grid_search(size, grid):
    max_elements = []
    max_x, max_y = size
    for x, y in product(range(max_x), range(max_y)):
        elements = longest_path(size, grid, (x, y))

        if len(elements) > len(max_elements):
            max_elements = elements
        elif len(elements) == len(max_elements):
            max_elements_drop = max_elements[0] - max_elements[-1]
            elements_drop = elements[0] - elements[-1]
            if elements_drop > max_elements_drop:
                max_elements = elements

    return max_elements


def longest_path(size, grid, current_pos):
    x, y = current_pos
    current_level = grid[x][y]

    possible_movement = next_possible_movement(size, current_pos)
    possible_movement_down = valid_next_movement(current_pos, grid, possible_movement)

    max_elements = []

    for next_pos in possible_movement_down:
        found, elements = get_path_with_max_drop(grid, max_elements, next_pos, size)
        if found:
            max_elements = elements

    return [current_level] + max_elements


def get_path_with_max_drop(grid, max_elements, next_pos, size):
    len_max_elements = len(max_elements)

    max_possible = longest_path(size, grid, next_pos)
    len_max_possible = len(max_possible)

    result = (False, [])

    if len_max_possible > len_max_elements:
        result = (True, max_possible)
    elif len_max_possible == len_max_elements:
        last_of_max_element = max_elements[-1]
        last_of_max_possible = max_possible[-1]
        result = (last_of_max_possible < last_of_max_element, max_possible)

    return result


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


def next_possible_movement(size, current_pos):
    x, y = current_pos
    max_x, max_y = size

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
        self.assertEqual(res, [1])

    def test_longest_path_2_by_2(self):
        # 4 3
        # 2 1
        size = (2, 2)
        grid = [[4, 3], [2, 1]]
        current_pos = (0, 0)
        res = longest_path(size, grid, current_pos)
        self.assertEqual(res, [4, 3, 1])

    def test_next_possible_movement(self):
        size = (2, 2)
        current_pos = (0, 0)
        res = next_possible_movement(size, current_pos)
        self.assertEqual(len(res), 2)
        self.assertTrue((0, 1) in res)
        self.assertTrue((1, 0) in res)

    def test_next_possible_movement_3_by_3(self):
        size = (3, 3)
        current_pos = (1, 1)
        res = next_possible_movement(size, current_pos)
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

    def test_longest_path_4_by_4(self):
        size = (4, 4)
        grid = [[4, 8, 7, 3], [2, 5, 9, 3], [6, 3, 2, 5], [4, 4, 1, 6]]
        current_pos = (1, 2)
        res = longest_path(size, grid, current_pos)
        self.assertEqual(res, [9, 5, 3, 2, 1])

    def test_longest_path_with_choice(self):
        # 9 9 9
        # 9 3 2
        # 9 1 9
        size = (3, 3)
        grid = [[9, 9, 9], [9, 3, 2], [9, 1, 9]]
        current_pos = (1, 1)
        res = longest_path(size, grid, current_pos)
        self.assertEqual(res, [3, 1])

    def test_get_path_with_max_drop(self):
        size = (3, 3)
        grid = [[9, 9, 9], [9, 3, 2], [9, 1, 9]]
        max_elements = [2]
        next_pos = (2, 1)
        res = get_path_with_max_drop(grid, max_elements, next_pos, size)
        self.assertEqual(res, (True, [1]))

    def test_get_path_with_max_drop_without_result(self):
        size = (3, 3)
        grid = [[9, 9, 9], [9, 3, 2], [9, 1, 9]]
        max_elements = [1]
        next_pos = (1, 2)
        res = get_path_with_max_drop(grid, max_elements, next_pos, size)
        self.assertEqual(res, (False, [2]))

    def test_grid_search(self):
        size = (4, 4)
        grid = [[4, 8, 7, 3], [2, 5, 9, 3], [6, 3, 2, 5], [4, 4, 1, 6]]
        res = grid_search(size, grid)
        self.assertEqual(res, [9, 5, 3, 2, 1])

    def test_read_file(self):
        filename = 'small-map.txt'
        res = read_file(filename)
        self.assertEqual(res[0], (4, 4))
        self.assertEqual(res[1], [[4, 8, 7, 3], [2, 5, 9, 3], [6, 3, 2, 5], [4, 4, 1, 6]])

if __name__ == '__main__':
    unittest.main()
