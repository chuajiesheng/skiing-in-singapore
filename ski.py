import unittest


def longest_path(size, grid, current_pos):
    max_x, max_y = size
    x, y = current_pos
    current_level = grid[x][y]

    possible_movement = []

    # move up
    if (x - 1) > -1:
        possible_movement.append((x-1, y))

    # move right
    if (y + 1) < max_y:
        possible_movement.append((x, y+1))

    # move down
    if (x + 1) < max_x:
        possible_movement.append((x+1, y))

    # move left
    if (y - 1) > -1:
        possible_movement.append((x, y-1))

    possible_movement_down = []
    for next_pos in possible_movement:
        next_x, next_y = next_pos
        next_level = grid[next_x][next_y]
        if next_level < current_level:
            possible_movement_down.append(next_pos)

    max_path_length = 1
    for next_pos in possible_movement_down:
        max_possible = 1 + longest_path(size, grid, next_pos)
        if max_possible > max_path_length:
            max_path_length = max_possible

    return max_path_length


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


if __name__ == '__main__':
    unittest.main()

