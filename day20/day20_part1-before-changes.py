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


class Tile:
    def __init__(self, tile_no: int, tile_size=10):
        self.tile_no = tile_no
        self.raw_image = dict()
        self.rotation = 0
        self.flip_x = False
        self.flip_y = False
        self.tile_size = tile_size
        # we use this all over the place
        self.tile_max = tile_size - 1

    def _calculate_one_side(
        self,
        start_x: int,
        end_x: int,
        start_y: int,
        end_y: int,
        reverse=False,
        x_flipped=False,
        y_flipped=False,
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
                if self._is_populated(x, y, x_flipped, y_flipped, 0):
                    result += 1
        return result

    def _calculate_one_matching_configuration(self, x_flipped, y_flipped):
        """
        Return the two lists of sides=[top,rhs,bottom,lhs], sides_accept=[top,rhs,bottom,lhs]
        """
        top = self._calculate_one_side(
            0, self.tile_max, 0, 0, x_flipped=x_flipped, y_flipped=y_flipped
        )
        top_accepts = self._calculate_one_side(
            0,
            self.tile_max,
            0,
            0,
            reverse=True,
            x_flipped=x_flipped,
            y_flipped=y_flipped,
        )

        rhs = self._calculate_one_side(
            self.tile_max,
            self.tile_max,
            0,
            self.tile_max,
            x_flipped=x_flipped,
            y_flipped=y_flipped,
        )
        rhs_accepts = self._calculate_one_side(
            self.tile_max,
            self.tile_max,
            0,
            self.tile_max,
            reverse=True,
            x_flipped=x_flipped,
            y_flipped=y_flipped,
        )

        bottom = self._calculate_one_side(
            self.tile_max,
            0,
            self.tile_max,
            self.tile_max,
            x_flipped=x_flipped,
            y_flipped=y_flipped,
        )
        bottom_accepts = self._calculate_one_side(
            self.tile_max,
            0,
            self.tile_max,
            self.tile_max,
            reverse=True,
            x_flipped=x_flipped,
            y_flipped=y_flipped,
        )

        lhs = self._calculate_one_side(
            0, 0, self.tile_max, 0, x_flipped=x_flipped, y_flipped=y_flipped
        )
        lhs_accepts = self._calculate_one_side(
            0,
            0,
            self.tile_max,
            0,
            reverse=True,
            x_flipped=x_flipped,
            y_flipped=y_flipped,
        )
        return (top, rhs, bottom, lhs), (
            top_accepts,
            rhs_accepts,
            bottom_accepts,
            lhs_accepts,
        )

    def _calculate_matching(self):
        """
        Do the maths logic for generating the list of sides values and their potential matching sides
        """
        self.unflipped = self._calculate_one_matching_configuration(False, False)
        self.xflipped = self._calculate_one_matching_configuration(True, False)
        self.yflipped = self._calculate_one_matching_configuration(False, True)
        self.flipped = self._calculate_one_matching_configuration(True, True)
        # and get ourselves a set of all the sides we have, for later use..
        self.available_sides = set(self.unflipped[0])
        self.available_sides.update(self.xflipped[0])
        self.available_sides.update(self.yflipped[0])
        self.available_sides.update(self.flipped[0])

    def flip(self, x: bool = False, y: bool = False):
        """
        flip along the indicated indices
        """
        if x:
            self._flip_x()
        if y:
            self._flip_y()

    def _flip_x(self):
        self.flip_x = not self.flip_x

    def _flip_y(self):
        self.flip_y = not self.flip_y

    def set_rotation(self, new_rotation: int):
        self.rotation = new_rotation

    def rotate(self, additional_clockwise_rotation: int):
        new_angle = self.rotation + additional_clockwise_rotation
        self.rotation = new_angle % 360

    def _is_populated(self, x: int, y: int, x_flip: bool, y_flip: bool, rotation: int):
        #
        #  Apply the rotation and flip logic, see if that spot is occupied
        #

        #
        #  basically we're just going to tweak the x/y read loaction based on flip and rotation
        #

        # flip first, simple enough
        if x_flip:
            x = self.tile_max - x
        if y_flip:
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

    def is_populated(self, x: int, y: int) -> bool:
        """
        Given the current rotation and flipping, is location x,y populated ?
        """
        return self._is_populated(x, y, self.flip_x, self.flip_y, self.rotation)

    def set_populated(self, x: int, y: int):
        """
        Store a raw x,y value for a hit.
        Rotation and flip is ignored for this as this is intended for loading the initial data
        """
        self.raw_image[(x, y)] = True
        self._calculate_matching()

    def print(self):
        """
        output just this tile
        """
        print(
            f"Tile {self.tile_no} (rotation={self.rotation}, flip_x={self.flip_x}, flip_y={self.flip_y})"
        )
        for y in range(self.tile_size):
            s = ""
            for x in range(self.tile_size):
                if self.is_populated(x, y):
                    s += "#"
                else:
                    s += "."
            print(f"{s}")
        print(f"un: {self.unflipped}")
        print(f" x: {self.xflipped}")
        print(f" y: {self.yflipped}")
        print(f"xy: {self.flipped}")
        print(f"available: {self.available_sides}")

        print("")

    def has_edge_matching(self, edge_value_to_match):
        """
        returning True if this tile could match the mentioned edge in any configuration
        """
        return edge_value_to_match in self.available_sides

    def evaluate_pairing(self, tilebag):
        """
        Given a bag including all the tiles, decide which options we have for each of our sides
        """
        # working an example for the unflipped options
        for this_side_accepts in self.unflipped[1]:
            # we are looking for any tile that can give us what we want (and isn't this tile)
            for this_tile_id in tilebag:
                if this_tile_id != self.tile_no:
                    # can this tile support our craving ?
                    this_tile = tilebag[this_tile_id]
                    if this_tile.has_edge_matching(this_side_accepts):
                        # we found a match !
                        print(
                            f"Tile {self.tile_no}: I have found I can match with tile {this_tile_id}"
                        )
                        self.print()
                        this_tile.print()
                        exit(1)


t = Tile(1234)
t.set_populated(1, 0)
t.set_populated(3, 0)
t.set_populated(9, 2)
t.set_populated(6, 9)
t.set_populated(0, 5)


t.print()


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


# so let's get that data in here..
filename = "sample.txt"
# filename = "input.txt"
tilebag = load_tiles_from_file(filename)
for this_tile in tilebag.values():
    this_tile.evaluate_pairing(tilebag)



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
        
    

class TileBoard:
    def __init__(self, tilebag: dict):
        self.board = dict()
        self.remaining_tiles = list(tilebag.keys())
        self.tilebag = tilebag
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None

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
        
    def print(self):




