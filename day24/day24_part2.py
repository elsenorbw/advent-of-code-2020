# --- Day 24: Lobby Layout ---
# Your raft makes it to the tropical island; it turns out that the small crab was an excellent navigator. You make your way to the resort.
#
# As you enter the lobby, you discover a small problem: the floor is being renovated. You can't even reach the check-in desk until they've finished installing the new tile floor.
#
# The tiles are all hexagonal; they need to be arranged in a hex grid with a very specific color pattern. Not in the mood to wait, you offer to help figure out the pattern.
#
# The tiles are all white on one side and black on the other. They start with the white side facing up. The lobby is large enough to fit whatever pattern might need to appear there.
#
# A member of the renovation crew gives you a list of the tiles that need to be flipped over (your puzzle input).
# Each line in the list identifies a single tile that needs to be flipped by giving a series of steps starting from a reference tile in the very center of the room. (Every line starts from the same reference tile.)
#
# Because the tiles are hexagonal, every tile has six neighbors: east, southeast, southwest, west, northwest, and northeast.
# These directions are given in your list, respectively, as e, se, sw, w, nw, and ne.
# A tile is identified by a series of these directions with no delimiters; for example, esenee identifies the tile you land on if
# you start at the reference tile and then move one tile east, one tile southeast, one tile northeast, and one tile east.
#
# Each time a tile is identified, it flips from white to black or from black to white. Tiles might be flipped more than once.
# For example, a line like esew flips a tile immediately adjacent to the reference tile, and a line like nwwswee flips the reference tile itself.
#
# Here is a larger example:
#
# sesenwnenenewseeswwswswwnenewsewsw
# neeenesenwnwwswnenewnwwsewnenwseswesw
# seswneswswsenwwnwse
# nwnwneseeswswnenewneswwnewseswneseene
# swweswneswnenwsewnwneneseenw
# eesenwseswswnenwswnwnwsewwnwsene
# sewnenenenesenwsewnenwwwse
# wenwwweseeeweswwwnwwe
# wsweesenenewnwwnwsenewsenwwsesesenwne
# neeswseenwwswnwswswnw
# nenwswwsewswnenenewsenwsenwnesesenew
# enewnwewneswsewnwswenweswnenwsenwsw
# sweneswneswneneenwnewenewwneswswnese
# swwesenesewenwneswnwwneseswwne
# enesenwswwswneneswsenwnewswseenwsese
# wnwnesenesenenwwnenwsewesewsesesew
# nenewswnwewswnenesenwnesewesw
# eneswnwswnwsenenwnwnwwseeswneewsenese
# neswnwewnwnwseenwseesewsenwsweewe
# wseweeenwnesenwwwswnew
# In the above example, 10 tiles are flipped once (to black), and 5 more are flipped twice (to black, then back to white). After all of these instructions have been followed, a total of 10 tiles are black.
#
# Go through the renovation crew's list and determine which tiles they need to flip. After all of the instructions have been followed, how many tiles are left with the black side up?
#


class HexConway:
    def __init__(self, starting_hexes):
        """
        initialise a conway machine with the current states
        """
        self.grid = starting_hexes

    def calculate_necessary_iteration_range(self):
        """
        Return a tuple of min_x, max_x, min_y, max_y which includes all the possible locations that could have a tile or a tile's neighbour in them
        this is effectively the +/-2 in the horizontal and +/-1 in the vertical
        """
        min_x = None
        max_x = None
        min_y = None
        max_y = None
        for this_x, this_y in self.grid:
            if min_x is None or this_x < min_x:
                min_x = this_x
            if max_x is None or this_x > max_x:
                max_x = this_x
            if min_y is None or this_y < min_y:
                min_y = this_y
            if max_y is None or this_y > max_y:
                max_y = this_y

        # add the buffer..
        if min_x is not None:
            min_x -= 2
            max_x += 2
            min_y -= 1
            max_y += 1

        return min_x, max_x, min_y, max_y

    def count_neighbours(self, x, y):
        """
        return how many neighbours to this tile are black
        """
        n_locations = set(
            [
                (-2, 0),
                (2, 0),
                (1, 1),
                (-1, 1),
                (1, -1),
                (-1, -1),
            ]
        )
        result = 0

        for x_offset, y_offset in n_locations:
            if self.is_black(x + x_offset, y + y_offset):
                result += 1

        return result

    def is_black(self, x, y):
        """
        only the tiles in the list are black (set)
        """
        return (x, y) in self.grid

    def is_white(self, x, y):
        return not self.is_black(x, y)

    def step(self):
        # apply the conway rules to generate the next grid..
        next_grid = set()
        # and iterate..
        x_min, x_max, y_min, y_max = self.calculate_necessary_iteration_range()
        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 2):
                neighbour_count = self.count_neighbours(x, y)
                black = self.is_black(x, y)
                # Any black tile with zero or more than 2 black tiles immediately adjacent to it is flipped to white.
                # Any white tile with exactly 2 black tiles immediately adjacent to it is flipped to black.
                # we are only filling in black tiles in the target layer so...
                if black:
                    if neighbour_count in [1, 2]:
                        next_grid.add((x, y))
                else:
                    if neighbour_count == 2:
                        next_grid.add((x, y))
        # and we're done.. we have a new grid
        self.grid = next_grid

    def score(self):
        return len(self.grid)


def line_to_location(s: str):
    """
    return an x,y location for given set of moves
    w,e move 2 in the specified direction
    the others move 1,1 in their directions..
    """
    moves = {
        "w": (-2, 0),
        "e": (2, 0),
        "se": (1, 1),
        "sw": (-1, 1),
        "ne": (1, -1),
        "nw": (-1, -1),
    }

    # while we still have instructions, follow the next move
    x = 0
    y = 0
    while len(s) > 0:
        # get this instruction
        if s.startswith("w") or s.startswith("e"):
            instruction_length = 1
        else:
            instruction_length = 2
        this_instruction = s[:instruction_length]
        s = s[instruction_length:]
        # and apply the move
        x_offset, y_offset = moves[this_instruction]
        new_x = x + x_offset
        new_y = y + y_offset
        # print(            f"from {x},{y} applied {this_instruction} moving to {new_x}, {new_y} (remaining:{s})"        )
        x = new_x
        y = new_y

    return x, y


def load_tile_pattern(filename):
    """
    Load the file mentioned, parsing each line as we go
    return the set of co-ordinates where tiles remain flipped
    """
    result = set()

    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                # got a line to handle..
                location = line_to_location(this_line)
                if location in result:
                    print(f"unflipping {location}")
                    result.remove(location)
                else:
                    print(f"flipping {location}")
                    result.add(location)

    return result


# main
filename = "input.txt"
# expecting 10 black tiles..
floor = load_tile_pattern(filename)

print(floor)
print(f"We have {len(floor)} flipped tiles remaining")

hc = HexConway(floor)

for day in range(1, 101):
    hc.step()
    print(f"Day {day}: {hc.score()}")
