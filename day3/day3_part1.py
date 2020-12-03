# --- Day 3: Toboggan Trajectory ---
# With the toboggan login problems resolved, you set off toward the airport.
# While travel by toboggan might be easy, it's certainly not safe: there's
# very minimal steering and the area is covered in trees. You'll need to see
# which angles will take you near the fewest trees.
#
# Due to the local geology, trees in this area only grow on exact integer
# coordinates in a grid. You make a map (your puzzle input) of the open
# squares (.) and trees (#) you can see. For example:
#
# ..##.......
# #...#...#..
# .#....#..#.
# ..#.#...#.#
# .#...##..#.
# ..#.##.....
# .#.#.#....#
# .#........#
# #.##...#...
# #...##....#
# .#..#...#.#
# These aren't the only trees, though; due to something you read about once
# involving arboreal genetics and biome stability, the same pattern repeats
# to the right many times:
#
# ..##.........##.........##.........##.........##.........##.......  --->
# #...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
# .#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
# ..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
# .#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
# ..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....  --->
# .#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
# .#........#.#........#.#........#.#........#.#........#.#........#
# #.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
# #...##....##...##....##...##....##...##....##...##....##...##....#
# .#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
# You start on the open square (.) in the top-left corner and need to reach
# the bottom (below the bottom-most row on your map).
#
# The toboggan can only follow a few specific slopes (you opted for a cheaper
# model that prefers rational numbers); start by counting all the trees you
# would encounter for the slope right 3, down 1:
#
# From your starting position at the top-left, check the position that is
# right 3 and down 1. Then, check the position that is right 3 and down 1
# from there, and so on until you go past the bottom of the map.
#
# The locations you'd check in the above example are marked here with O where
# there was an open square and X where there was a tree:
#
# ..##.........##.........##.........##.........##.........##.......  --->
# #..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
# .#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
# ..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
# .#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
# ..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
# .#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
# .#........#.#........X.#........#.#........#.#........#.#........#
# #.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
# #...##....##...##....##...#X....##...##....##...##....##...##....#
# .#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->
# In this example, traversing the map using this slope would cause you to
# encounter 7 trees.
#
# Starting at the top-left corner of your map and following a slope
# of right 3 and down 1, how many trees would you encounter?
#
#


class Forest:
    def __init__(self):
        self.rows = 0
        self.width = 0
        self.tree_locations = {}

    def height(self):
        return self.rows

    def add_tree(self, x: int, y: int):
        """
        Record the location of one tree
        """
        self.tree_locations[(x, y)] = True
        self.rows = max(self.rows, y + 1)
        self.width = max(self.width, x + 1)

    def add_space(self, x: int, y: int):
        """
        Record the location of one non-tree
        """
        self.rows = max(self.rows, y + 1)
        self.width = max(self.width, x + 1)

    def is_tree(self, x: int, y: int) -> bool:
        """
        Return if this location should be a tree
        """
        x = x % self.width
        result = (x, y) in self.tree_locations
        return result

    def print(self, wide_copies=1):
        for y in range(self.rows):
            this_row = ""
            for x in range(self.width * wide_copies):
                if self.is_tree(x, y):
                    this_row += "T"
                else:
                    this_row += "."
            print(this_row)
        print("")


def load_forest(filename: str) -> Forest:
    """
    Load a forest from a given file
    """
    result = Forest()
    with open(filename, "r") as f:
        current_y = 0
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                # add the values in this line
                for x in range(len(this_line)):
                    this_char = this_line[x]
                    if "#" == this_char:
                        result.add_tree(x, current_y)
                    elif "." == this_char:
                        result.add_space(x, current_y)
                    else:
                        raise ValueError(
                            f"Unexpected character in map : {this_char} at {x}, {current_y}"
                        )
                # and moving on..
                current_y += 1
    return result


def count_trees_on_journey(
    forest: Forest, start_x: int, start_y: int, x_increment: int, y_increment: int
) -> int:
    """
    Count the number of trees which would be hit on any given path through the forest
    """
    tree_count = 0
    x = start_x
    y = start_y
    while y < forest.height():
        # is this a tree ?
        if forest.is_tree(x, y):
            tree_count += 1
        # next location
        y += y_increment
        x += x_increment
    return tree_count


# main code..

filename = "input.txt"

forest = load_forest(filename)
forest.print()

tree_count = count_trees_on_journey(forest, 0, 0, 3, 1)
print(f"we hit {tree_count} trees!")
