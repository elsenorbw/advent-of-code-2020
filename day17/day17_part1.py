# --- Day 17: Conway Cubes ---
# As your flight slowly drifts through the sky, the Elves at the Mythical Information Bureau at the North Pole contact you.
# They'd like some help debugging a malfunctioning experimental energy source aboard one of their super-secret imaging satellites.
#
# The experimental energy source is based on cutting-edge technology: a set of Conway Cubes contained in a pocket dimension!
# When you hear it's having problems, you can't help but agree to take a look.
#
# The pocket dimension contains an infinite 3-dimensional grid. At every integer 3-dimensional coordinate (x,y,z), there exists a single cube which is either active or inactive.
#
# In the initial state of the pocket dimension, almost all cubes start inactive. The only exception to this is a small flat region of cubes (your puzzle input);
# the cubes in this region start in the specified active (#) or inactive (.) state.
#
# The energy source then proceeds to boot up by executing six cycles.
#
# Each cube only ever considers its neighbors: any of the 26 other cubes where any of their coordinates differ by at most 1. For example, given the cube at x=1,y=2,z=3,
# its neighbors include the cube at x=2,y=2,z=2, the cube at x=0,y=2,z=3, and so on.
#
# During a cycle, all cubes simultaneously change their state according to the following rules:
#
# If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
# If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
# The engineers responsible for this experimental energy source would like you to simulate the pocket dimension and determine what the configuration of cubes should be at the end of the six-cycle boot process.
#
# For example, consider the following initial state:
#
# .#.
# ..#
# ###
# Even though the pocket dimension is 3-dimensional, this initial state represents a small 2-dimensional slice of it. (In particular, this initial state defines a 3x3x1 region of the 3-dimensional space.)
#
# Simulating a few cycles from this initial state produces the following configurations, where the result of each cycle is shown layer-by-layer at each given z coordinate (and the frame of view follows the active cells in each cycle):
#
# Before any cycles:
#
# z=0
# .#.
# ..#
# ###
#
#
# After 1 cycle:
#
# z=-1
# #..
# ..#
# .#.
#
# z=0
# #.#
# .##
# .#.
#
# z=1
# #..
# ..#
# .#.
#
#
# After 2 cycles:
#
# z=-2
# .....
# .....
# ..#..
# .....
# .....
#
# z=-1
# ..#..
# .#..#
# ....#
# .#...
# .....
#
# z=0
# ##...
# ##...
# #....
# ....#
# .###.
#
# z=1
# ..#..
# .#..#
# ....#
# .#...
# .....
#
# z=2
# .....
# .....
# ..#..
# .....
# .....
#
#
# After 3 cycles:
#
# z=-2
# .......
# .......
# ..##...
# ..###..
# .......
# .......
# .......
#
# z=-1
# ..#....
# ...#...
# #......
# .....##
# .#...#.
# ..#.#..
# ...#...
#
# z=0
# ...#...
# .......
# #......
# .......
# .....##
# .##.#..
# ...#...
#
# z=1
# ..#....
# ...#...
# #......
# .....##
# .#...#.
# ..#.#..
# ...#...
#
# z=2
# .......
# .......
# ..##...
# ..###..
# .......
# .......
# .......
# After the full six-cycle boot process completes, 112 cubes are left in the active state.
#
# Starting with your given initial configuration, simulate six cycles. How many cubes are left in the active state after the sixth cycle?
#
# To begin, get your puzzle input.
#


# so Conway in Space!


class SpaceMap:
    def __init__(self):
        self.clear()
        self.neighbour_offset_mapping = set()
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    self.neighbour_offset_mapping.add((x, y, z))
        # and remove ourselves..
        self.neighbour_offset_mapping.remove((0, 0, 0))

    def clear(self):
        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None
        self.min_z = None
        self.max_z = None
        self.state = dict()

    def ensure_boundary_includes(self, x, y, z):
        """
        Make sure that min/max values are updated..
        """
        if self.min_x is None or x < self.min_x:
            self.min_x = x
        if self.max_x is None or x > self.max_x:
            self.max_x = x
        if self.min_y is None or y < self.min_y:
            self.min_y = y
        if self.max_y is None or y > self.max_y:
            self.max_y = y
        if self.min_z is None or z < self.min_z:
            self.min_z = z
        if self.max_z is None or z > self.max_z:
            self.max_z = z

    def set_active(self, x, y, z):
        self.state[(x, y, z)] = True
        self.ensure_boundary_includes(x, y, z)

    def is_active(self, x, y, z):
        return (x, y, z) in self.state

    def count_neighbours(self, x, y, z, stop_after=4):
        """
        Return how many neighbours are active within the 1 block cube around the point given
        """
        result = 0

        # generate all the acceptable offsets.. we should probably only do this once.. so moving this out of here..
        for x_off, y_off, z_off in self.neighbour_offset_mapping:
            # if this one is populated then add one..
            if self.is_active(x + x_off, y + y_off, z + z_off):
                result += 1
                if result >= stop_after:
                    break

        return result

    def x_range(self):
        """
        Return the range of values that need to be considered for iterating
        """
        return range(self.min_x - 1, self.max_x + 2)

    def y_range(self):
        """
        Return the range of values that need to be considered for iterating
        """
        return range(self.min_y - 1, self.max_y + 2)

    def z_range(self):
        """
        Return the range of values that need to be considered for iterating
        """
        return range(self.min_z - 1, self.max_z + 2)

    def print(self):
        """
        Output each layer
        """
        for z in range(self.min_z, self.max_z + 1):
            print(f"Layer z={z}")
            # and print the actual layer
            for y in range(self.min_y, self.max_y + 1):
                s = ""
                for x in range(self.min_x, self.max_x + 1):
                    if (x, y, z) in self.state:
                        s += "#"
                    else:
                        s += "."
                print(f" {s}")
            print("")

    def total_active(self):
        """
        Return the number of active cubes in the map
        """
        return len(self.state.keys())


class SpaceConway:
    def __init__(self):
        self.clear()

    def clear(self):
        self.cycle = 0
        self.map = SpaceMap()

    def step(self):
        """
        Move to the next state
        """
        next_map = SpaceMap()
        for x in self.map.x_range():
            for y in self.map.y_range():
                for z in self.map.z_range():
                    # run the rules for this new x,y,z
                    neighbour_count = self.map.count_neighbours(x, y, z)
                    currently_active = self.map.is_active(x, y, z)
                    # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
                    # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.
                    if currently_active:
                        if neighbour_count in (2, 3):
                            # anything else will not feature in the next state as active
                            next_map.set_active(x, y, z)
                    else:
                        if neighbour_count == 3:
                            next_map.set_active(x, y, z)
        # and store the result..
        self.map = next_map
        self.cycle += 1

    def print(self, diagram=True):
        """
        Output each layer
        """
        print(
            f"SpaceConway: {self.map.total_active()} active cubes after {self.cycle} cycles -> x: {self.map.min_x}..{self.map.max_x}, y: {self.map.min_y}..{self.map.max_y}, z:{self.map.min_z}..{self.map.max_z}"
        )
        if diagram:
            self.map.print()

    def load_initial_state(self, filename):
        """
        Read an input file for z=0,
        # characters are occupied, other characters are not
        """
        with open(filename, "r") as f:
            z = 0
            y = 0
            for this_line in f:
                this_line = this_line.strip()
                if "" != this_line:
                    # process this row
                    for x, the_val in enumerate(this_line):
                        if "#" == the_val:
                            self.map.set_active(x, y, z)
                    # next row
                    y += 1


# main
filename = "input.txt"
machine = SpaceConway()
machine.load_initial_state(filename)
machine.print()
for iterations in range(6):
    machine.step()
    machine.print()
