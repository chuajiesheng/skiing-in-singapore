import unittest


def longest_path(grid, current_pos):
    return 1


class SkiTest(unittest.TestCase):
    def test_longest_path(self):
        grid = [[1]]
        current_pos = (0, 0)
        res = longest_path(grid, current_pos)
        self.assertEqual(res, 1)


if __name__ == '__main__':
    unittest.main()
