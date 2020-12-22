# --- Day 20: Jurassic Jigsaw ---
# The high-speed train leaves the forest and quickly carries you south. You can even see a desert in the distance! Since you have some spare time, you
# might as well see if there was anything interesting in the image the Mythical Information Bureau satellite captured.
#
# After decoding the satellite messages, you discover that the data actually contains many small images created by the satellite's camera array. #
# The camera array consists of many cameras; rather than produce a single square image, they produce many smaller square image tiles that need to be reassembled back into a single image.
#
# Each camera in the camera array returns a single monochrome image tile with a random unique ID number. The tiles (your puzzle input) arrived in a random order.
#
# Worse yet, the camera array appears to be malfunctioning: each image tile has been rotated and flipped to a random orientation. Your first task is to reassemble the original image by orienting the tiles so they fit together.
#
# To show how the tiles should be reassembled, each tile's image data includes a border that should line up exactly with its adjacent tiles. All tiles have this border, and
# the border lines up exactly when the tiles are both oriented correctly. Tiles at the edge of the image also have this border, but the outermost edges won't line up with any other tiles.
#
# For example, suppose you have the following nine tiles:
#
# Tile 2311:
# ..##.#..#.
# ##..#.....
# #...##..#.
# ####.#...#
# ##.##.###.
# ##...#.###
# .#.#.#..##
# ..#....#..
# ###...#.#.
# ..###..###
#
# Tile 1951:
# #.##...##.
# #.####...#
# .....#..##
# #...######
# .##.#....#
# .###.#####
# ###.##.##.
# .###....#.
# ..#.#..#.#
# #...##.#..
#
# Tile 1171:
# ####...##.
# #..##.#..#
# ##.#..#.#.
# .###.####.
# ..###.####
# .##....##.
# .#...####.
# #.##.####.
# ####..#...
# .....##...
#
# Tile 1427:
# ###.##.#..
# .#..#.##..
# .#.##.#..#
# #.#.#.##.#
# ....#...##
# ...##..##.
# ...#.#####
# .#.####.#.
# ..#..###.#
# ..##.#..#.
#
# Tile 1489:
# ##.#.#....
# ..##...#..
# .##..##...
# ..#...#...
# #####...#.
# #..#.#.#.#
# ...#.#.#..
# ##.#...##.
# ..##.##.##
# ###.##.#..
#
# Tile 2473:
# #....####.
# #..#.##...
# #.##..#...
# ######.#.#
# .#...#.#.#
# .#########
# .###.#..#.
# ########.#
# ##...##.#.
# ..###.#.#.
#
# Tile 2971:
# ..#.#....#
# #...###...
# #.#.###...
# ##.##..#..
# .#####..##
# .#..####.#
# #..#.#..#.
# ..####.###
# ..#.#.###.
# ...#.#.#.#
#
# Tile 2729:
# ...#.#.#.#
# ####.#....
# ..#.#.....
# ....#..#.#
# .##..##.#.
# .#.####...
# ####.#.#..
# ##.####...
# ##..#.##..
# #.##...##.
#
# Tile 3079:
# #.#.#####.
# .#..######
# ..#.......
# ######....
# ####.#..#.
# .#...#.##.
# #.#####.##
# ..#.###...
# ..#.......
# ..#.###...
# By rotating, flipping, and rearranging them, you can find a square arrangement that causes all adjacent borders to line up:
#
# #...##.#.. ..###..### #.#.#####.
# ..#.#..#.# ###...#.#. .#..######
# .###....#. ..#....#.. ..#.......
# ###.##.##. .#.#.#..## ######....
# .###.##### ##...#.### ####.#..#.
# .##.#....# ##.##.###. .#...#.##.
# #...###### ####.#...# #.#####.##
# .....#..## #...##..#. ..#.###...
# #.####...# ##..#..... ..#.......
# #.##...##. ..##.#..#. ..#.###...
#
# #.##...##. ..##.#..#. ..#.###...
# ##..#.##.. ..#..###.# ##.##....#
# ##.####... .#.####.#. ..#.###..#
# ####.#.#.. ...#.##### ###.#..###
# .#.####... ...##..##. .######.##
# .##..##.#. ....#...## #.#.#.#...
# ....#..#.# #.#.#.##.# #.###.###.
# ..#.#..... .#.##.#..# #.###.##..
# ####.#.... .#..#.##.. .######...
# ...#.#.#.# ###.##.#.. .##...####
#
# ...#.#.#.# ###.##.#.. .##...####
# ..#.#.###. ..##.##.## #..#.##..#
# ..####.### ##.#...##. .#.#..#.##
# #..#.#..#. ...#.#.#.. .####.###.
# .#..####.# #..#.#.#.# ####.###..
# .#####..## #####...#. .##....##.
# ##.##..#.. ..#...#... .####...#.
# #.#.###... .##..##... .####.##.#
# #...###... ..##...#.. ...#..####
# ..#.#....# ##.#.#.... ...##.....
# For reference, the IDs of the above tiles are:
#
# 1951    2311    3079
# 2729    1427    2473
# 2971    1489    1171
# To check that you've assembled the image correctly, multiply the IDs of the four corner tiles together. If you do this with the assembled tiles from the example above, you get 1951 * 3079 * 2971 * 1171 = 20899048083289.
#
# Assemble the tiles into an image. What do you get if you multiply together the IDs of the four corner tiles?
#
# To begin, get your puzzle input.


# well this is a little more complicated..
# as a start, each one of the tiles is 10x10
# this gives us a 10-bit number for each edge of the tile
#  - let's take that number as Left-Right and Top-Bottom
#
#  We can rotate and flip the tiles, meaning:
#
#  - Flipping X (Left hand side now on the right) -> new top+bottom values, L+R values switch
#  - Flipping Y (top row now at the bottom) -> Top+bottom switch, new L+R values
#  - Rotating (always clockwise):
#    - 90 - all new values RHS should be same as previous Top
#    - 180.. new
#    - 270.. again new
#
#  So effectively each piece has 4 starting configurations : unflipped, x-flipped, y-flipped, xy-flipped
#  each of those configurations has 4 rotations : 0, 90, 180, 270
#  so each tile can really offer us 16 different combinations of edges
#
#  Depending on the size of the square (sample is 3x3, input is 144 boxes so 12x12)
#  we will have:
#  4 corner pieces (only 2 sides need to match)
#  4 x (side_length - 2) edge pieces (3 sides matching)
#  remainder middle pieces (all 4 sides need to match)
#
#  So, can we brute-force it ? 144 ^ 16 combinations, lots of short circuit but still..
#  probably not. There may be a shortcut by finding edges that don't match any other edge
#  but that's in no way a guarantee. Just because it's a corner piece doesn't mean that the outside edges won't fit anywhere
#
#  Can we try a most-matches plan ? If you can manipulate a block until it has all 4 sides matching then that's a decent start ?
#  Let's get it loaded and investigate the problem a bit..
#

# actually, having thought about it a bit more, it would probably be more useful to consider each side ignoring rotation, so effectively if you have :
#    B
#  A # C
#    D
#
#  then side B always has the same value regardless of rotation, meaning that we need to calculate the lhs bottom to top, rhs top to bottom and bottom side right to left
#  now flipping will change the layouts so that would give us a second set of left,right,top,bottom
#  so now we are down to eight sides, because we can ignore rotation, there's some messy matching to get the only-x and only-y flipped versions but that's about it
#  the other good news is that each face can match at most 2 different other faces, and we can pre-calculate those values as they're the inverse of the side
#  going to add that logic and see how we get on
#
import math


TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3


def opposite_direction(direction):
    answer = {TOP: BOTTOM, RIGHT: LEFT, BOTTOM: TOP, LEFT: RIGHT}
    return answer[direction]


def dir_name(direction):
    answer = {TOP: "top", RIGHT: "right", LEFT: "left", BOTTOM: "bottom"}
    return answer[direction]


def offsets_for_direction(direction):
    answer = {TOP: (0, -1), RIGHT: (1, 0), BOTTOM: (0, 1), LEFT: (-1, 0)}
    return answer[direction]


class Tile:
    def __init__(self, tile_no: int, tile_size=10):
        self.tile_no = tile_no
        self.raw_image = dict()
        self.tile_size = tile_size
        # we use this all over the place
        self.tile_max = tile_size - 1

    def _get_side_score(
        self, edge: int, rotation: int, x_flipped: bool, y_flipped: bool, reverse: bool
    ):
        """
        Produce the score provided by the edge specified (TOP, RIGHT, BOTTOM, LEFT)
        """
        if TOP == edge:
            result = self._calculate_one_side(
                0, self.tile_max, 0, 0, x_flipped, y_flipped, rotation, reverse
            )
        elif RIGHT == edge:
            result = self._calculate_one_side(
                self.tile_max,
                self.tile_max,
                0,
                self.tile_max,
                x_flipped,
                y_flipped,
                rotation,
                reverse,
            )
        elif BOTTOM == edge:
            result = self._calculate_one_side(
                self.tile_max,
                0,
                self.tile_max,
                self.tile_max,
                x_flipped,
                y_flipped,
                rotation,
                reverse,
            )
        elif LEFT == edge:
            result = self._calculate_one_side(
                0, 0, self.tile_max, 0, x_flipped, y_flipped, rotation, reverse
            )

        return result

    def get_side_score(
        self, edge: int, rotation: int, x_flipped: bool, y_flipped: bool
    ):
        return self._get_side_score(edge, rotation, x_flipped, y_flipped, False)

    def get_side_accepts(
        self, edge: int, rotation: int, x_flipped: bool, y_flipped: bool
    ):
        return self._get_side_score(edge, rotation, x_flipped, y_flipped, True)

    def _calculate_one_side(
        self,
        start_x: int,
        end_x: int,
        start_y: int,
        end_y: int,
        x_flipped: bool,
        y_flipped: bool,
        rotation: int,
        reverse: bool = False,
    ):
        """
        Create a number using the specified range as binary digits
        """
        if reverse:
            start_x, end_x = end_x, start_x
            start_y, end_y = end_y, start_y
        # figure out the step
        x_step = 1 if start_x <= end_x else -1
        y_step = 1 if start_y <= end_y else -1

        # and adjust the end location..
        end_x += x_step
        end_y += y_step

        # and loop doing the addition
        result = 0
        for y in range(start_y, end_y, y_step):
            for x in range(start_x, end_x, x_step):
                # shift and add
                result *= 2
                if self.is_populated(x, y, x_flipped, y_flipped, rotation):
                    result += 1
        return result

    def is_populated(
        self, x: int, y: int, x_flipped: bool, y_flipped: bool, rotation: int
    ):
        #
        #  Apply the rotation and flip logic, see if that spot is occupied
        #

        #
        #  basically we're just going to tweak the x/y read loaction based on flip and rotation
        #

        # flip first, simple enough
        if x_flipped:
            x = self.tile_max - x
        if y_flipped:
            y = self.tile_max - y

        #
        #  And now the rotationy stuff
        #
        # 90 degrees clockwise, so top left (x=2, y=1) -> (x=8,y=2)  (so y=x, x=max-y)
        # but that's the logic for moving a point, so we need to be thinking about where on the original pattern the source would be
        # so, the thing that would show at
        # a block at 0,8 needs to appear at 1, 0
        # so when we read 1, 0, we actually need to read 0,8
        # so target_x = y
        # target_y = max - x
        if 90 <= rotation:
            x, y = y, self.tile_max - x
        if 180 <= rotation:
            x, y = y, self.tile_max - x
        if 270 <= rotation:
            x, y = y, self.tile_max - x

        # and get the actual value
        return (x, y) in self.raw_image

    def set_populated(self, x: int, y: int):
        """
        Store a raw x,y value for a hit.
        Rotation and flip is ignored for this as this is intended for loading the initial data
        """
        self.raw_image[(x, y)] = True

    def print(self, rotation=0, x_flipped=False, y_flipped=False):
        """
        output just this tile
        """
        print(
            f"Tile {self.tile_no} (rotation={rotation}, flip_x={x_flipped}, flip_y={y_flipped})"
        )
        for y in range(self.tile_size):
            s = ""
            for x in range(self.tile_size):
                if self.is_populated(x, y, x_flipped, y_flipped, rotation):
                    s += "#"
                else:
                    s += "."
            print(f"{s}")
        print(
            f"Side values are: top={self.get_side_score(TOP, rotation, x_flipped, y_flipped)}, right={self.get_side_score(RIGHT, rotation, x_flipped, y_flipped)}, bot={self.get_side_score(BOTTOM, rotation, x_flipped, y_flipped)}, left={self.get_side_score(LEFT, rotation, x_flipped, y_flipped)}"
        )
        print("")


# create a tilebag from the tiles in a file..
def load_tiles_from_file(filename: str):
    result = dict()
    current_tile_no = None
    y = None

    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                print(f"Processing: {this_line}")
                if this_line.startswith("Tile "):
                    # format is Tile 1234:
                    number_part = this_line[5:-1]
                    current_tile_no = int(number_part)
                    print(f"loading tile {current_tile_no}")
                    if current_tile_no in result:
                        raise RuntimeError(f"Duplicate tile number {current_tile_no}")
                    result[current_tile_no] = Tile(current_tile_no)
                    y = 0
                else:
                    # this is a tile information line
                    for x, this_char in enumerate(this_line):
                        if "#" == this_char:
                            result[current_tile_no].set_populated(x, y)
                    y += 1

    return result


#
# ok, new plan, we can start placing things on the board, one at a time and solve this recursively perhaps ?
# each round would need a copy of the board, a list of remaining tiles to be placed
# unsure if it's smarter to try and place the next tile given all the available edges or to try and find a tile for a given edge
# probably not very important. Any given board, since the pieces have been placed and certain edges have been consumed, should be able to calculate the available edges for placement
# slightly complicated one, let's see how we go..
#

# a tile which has been added to the board, it has a fixed rotation and flip setting
class PlacedTile:
    def __init__(self, base_tile, rotation, x_flipped, y_flipped):
        self.base_tile = base_tile
        self.rotation = rotation
        self.x_flipped = x_flipped
        self.y_flipped = y_flipped

    def print(self):
        self.base_tile.print(
            rotation=self.rotation, x_flipped=self.x_flipped, y_flipped=self.y_flipped
        )

    def get_required_edge_value(self, edge: int):
        """
        Return the value that a tile would require to fit at the mentioned edge
        """
        return self.base_tile.get_side_accepts(
            edge, self.rotation, self.x_flipped, self.y_flipped
        )

    def tile_no(self):
        return self.base_tile.tile_no


def all_possible_tile_configurations():
    """
    return all the possible tuples of rotation, x_flip, y_flip
    """
    result = []
    for rotation in [0, 90, 180, 270]:
        for x_flip in [False, True]:
            for y_flip in [False, True]:
                result.append((rotation, x_flip, y_flip))

    return result


class TileBoard:
    def __init__(self, tilebag: dict):
        self.board = dict()
        self.remaining_tiles = list(tilebag.keys())
        self.tilebag = tilebag
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None
        self.max_dimension = int(math.sqrt(len(tilebag)))

    def copy(self):
        """
        Return a duplicate of this board..
        """
        t = TileBoard(self.tilebag)
        t.board = self.board.copy()
        t.remaining_tiles = self.remaining_tiles.copy()
        t.min_x = self.min_x
        t.max_x = self.max_x
        t.min_y = self.min_y
        t.max_y = self.max_y
        t.max_dimension = self.max_dimension
        return t

    def print(self):
        print(
            f"Tileboard: ({len(self.remaining_tiles)} left to place) (max dimension: {self.max_dimension}x{self.max_dimension})"
        )
        if self.min_x is not None and self.min_y is not None:
            print(
                f"Current grid is {self.max_x - self.min_x + 1} x {self.max_y - self.min_y + 1}"
            )
            # and now print the actual grid.. could be fun and messy
            # first the tile ids..
            for y in range(self.min_y, self.max_y + 1):
                s = ""
                for x in range(self.min_x, self.max_x + 1):
                    this_tile = "...."
                    if self.is_populated(x, y):
                        this_tile = str(self.get_tile(x, y).tile_no())
                    s += this_tile + " "
                print(s)
        print("")

    def place_tile(
        self, the_tile, x: int, y: int, rotation: int, x_flipped: bool, y_flipped: bool
    ):
        """
        put one tile in a position, no logic to see if this is safe/correct, assuming you've done that
        """
        self.board[(x, y)] = PlacedTile(the_tile, rotation, x_flipped, y_flipped)
        if self.min_x is None or x < self.min_x:
            self.min_x = x
        if self.max_x is None or x > self.max_x:
            self.max_x = x
        if self.min_y is None or y < self.min_y:
            self.min_y = y
        if self.max_y is None or y > self.max_y:
            self.max_y = y

    def is_populated(self, x: int, y: int):
        return self.get_tile(x, y) is not None

    def get_tile(self, x: int, y: int):
        result = None
        if (x, y) in self.board:
            result = self.board[(x, y)]
        return result

    def neighbour_count(self, x: int, y: int, direction: int):
        """
        Return the number of neighbours in any given direction
        """
        result = 0

        x_offset, y_offset = offsets_for_direction(direction)
        x += x_offset
        y += y_offset
        while self.is_populated(x, y):
            result += 1
            x += x_offset
            y += y_offset

        return result

    def remove_remaining_tile(self, tile_no: int):
        """
        Take this tile out of the tile list..
        """
        s = set(self.remaining_tiles)
        s.remove(tile_no)
        self.remaining_tiles = list(s)

    def answer_part1(self):
        """
        Get the four corner pieces and multiply their ids
        """
        result = 1

        for x, y in [
            (self.min_x, self.min_y),
            (self.max_x, self.min_y),
            (self.min_x, self.max_y),
            (self.max_x, self.max_y),
        ]:
            tile = self.get_tile(x, y)
            tile_no = tile.tile_no()
            print(f"Adding tile {tile_no}")
            result *= tile_no

        print(f"answer_part1 returns {result}")
        return result

    def solve(self):
        # place the remaining pieces in a way that works
        # plan is to place a single piece and work from there..
        if self.min_x is None:
            # nothing so far, going to pick the first piece and see what happens..
            this_tile = self.remaining_tiles[0]
            self.remaining_tiles = self.remaining_tiles[1:]
            # and place this tile one of the 4 possible ways, rotation is irrelevant on the first piece
            starting_flips = (
                (False, False),
                (True, False),
                (False, True),
                (True, True),
            )
            for this_x_flip, this_y_flip in starting_flips:
                self.place_tile(
                    self.tilebag[this_tile], 0, 0, 0, this_x_flip, this_y_flip
                )
                # now make a copy and see if we can solve it this way..
                this_attempt = self.copy()
                this_attempt.print()
                solved_board = this_attempt.solve()
                if solved_board is not None:
                    print(f"WooHoo - found a winner!")
                    return solved_board
        else:

            # Victory condition, we have placed everything...
            if 0 == len(self.remaining_tiles):
                print(f"This is SPAARTAAAA!")
                self.print()
                return self

            # ok, we have a board and we need to place a piece..
            # for all the pieces we have already placed, check each un-used edge and see whether we can place a tile there..
            for this_placed_tile in self.board:
                the_tile = self.board[this_placed_tile]
                x, y = this_placed_tile
                print(f"evaluating the tile at {x},{y}")
                # can we find a match for any of the edges here ?
                edges = [TOP, RIGHT, BOTTOM, LEFT]
                for target_edge in edges:
                    x_offset, y_offset = offsets_for_direction(target_edge)
                    target_x = x + x_offset
                    target_y = y + y_offset
                    candidate_edge = opposite_direction(target_edge)

                    # see whether that space is already filled..
                    if not self.is_populated(target_x, target_y):

                        # check that this line is not already too long to add in this direction..
                        opposite_edge_neighbours = self.neighbour_count(
                            x, y, opposite_direction(target_edge)
                        )
                        if self.max_dimension > 1 + opposite_edge_neighbours:
                            # ok, we can actually try to add something here, it won't make the line too long and there's a gap

                            # get the value that this edge requires..
                            required_value_for_edge = the_tile.get_required_edge_value(
                                target_edge
                            )

                            print(
                                f"base tile at {x},{y}: trying to place at location {target_x},{target_y} ({dir_name(target_edge)}) which requires {required_value_for_edge}"
                            )

                            # now run through every possible tile in every possible combination and see if it is possible
                            for candidate_tile_no in self.remaining_tiles:
                                print(f"considering tile {candidate_tile_no}")
                                # there's definitely some optimisation to be had here, but we'll come back if it's too slow
                                # try the target tile every which way..
                                candidate_tile = self.tilebag[candidate_tile_no]
                                for (
                                    this_tile_configuration
                                ) in all_possible_tile_configurations():
                                    (
                                        candidate_rotation,
                                        candidate_x_flip,
                                        candidate_y_flip,
                                    ) = this_tile_configuration
                                    if (
                                        candidate_tile.get_side_score(
                                            candidate_edge,
                                            candidate_rotation,
                                            candidate_x_flip,
                                            candidate_y_flip,
                                        )
                                        == required_value_for_edge
                                    ):
                                        print(
                                            f"Found a potential match: {this_placed_tile} on edge {dir_name(target_edge)} matches with {candidate_tile_no} ({candidate_rotation, candidate_x_flip, candidate_y_flip})"
                                        )
                                        the_tile.print()
                                        candidate_tile.print(
                                            candidate_rotation,
                                            candidate_x_flip,
                                            candidate_y_flip,
                                        )
                                        # try this match as a final solution
                                        # now make a copy and see if we can solve it this way..
                                        this_attempt = self.copy()
                                        this_attempt.place_tile(
                                            candidate_tile,
                                            target_x,
                                            target_y,
                                            candidate_rotation,
                                            candidate_x_flip,
                                            candidate_y_flip,
                                        )
                                        this_attempt.remove_remaining_tile(
                                            candidate_tile_no
                                        )
                                        this_attempt.print()
                                        solved_board = this_attempt.solve()
                                        if solved_board is not None:
                                            print(f"WooHoo - found a winner!")
                                            return solved_board

        return None


# tile basic testing..
if False:
    t = Tile(1234)
    t.set_populated(1, 0)
    t.set_populated(3, 0)
    t.set_populated(9, 2)
    t.set_populated(6, 9)
    t.set_populated(0, 5)

    t.print(rotation=0)
    t.print(rotation=90)

    p1 = PlacedTile(t, 0, False, False)
    p1.print()

    p2 = PlacedTile(t, 0, True, False)
    p2.print()

    p3 = PlacedTile(t, 0, False, True)
    p3.print()

    exit(1)


# main program
# so let's get that data in here..
filename = "sample.txt"
filename = "input.txt"
tilebag = load_tiles_from_file(filename)
# and create a board to solve..
board = TileBoard(tilebag)
board.print()
solved = board.solve()

solved.answer_part1()
