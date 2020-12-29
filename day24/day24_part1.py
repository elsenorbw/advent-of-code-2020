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
        print(
            f"from {x},{y} applied {this_instruction} moving to {new_x}, {new_y} (remaining:{s})"
        )
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

