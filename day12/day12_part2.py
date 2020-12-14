# --- Day 12: Rain Risk ---
# Your ferry made decent progress toward the island, but the storm came in faster than anyone expected. The ferry needs to take evasive actions!
#
# Unfortunately, the ship's navigation computer seems to be malfunctioning; rather than giving a route directly to safety, it produced extremely circuitous instructions. When the captain uses the PA system to ask if anyone can help, you quickly volunteer.
#
# The navigation instructions (your puzzle input) consists of a sequence of single-character actions paired with integer input values. After staring at them for a few minutes, you work out what they probably mean:
#
# Action N means to move north by the given value.
# Action S means to move south by the given value.
# Action E means to move east by the given value.
# Action W means to move west by the given value.
# Action L means to turn left the given number of degrees.
# Action R means to turn right the given number of degrees.
# Action F means to move forward by the given value in the direction the ship is currently facing.
# The ship starts by facing east. Only the L and R actions change the direction the ship is facing. (That is, if the ship is facing east and the next instruction is N10, the ship would move north 10 units, but would still move east if the following action were F.)
#
# For example:
#
# F10
# N3
# F7
# R90
# F11
# These instructions would be handled as follows:
#
# F10 would move the ship 10 units east (because the ship starts by facing east) to east 10, north 0.
# N3 would move the ship 3 units north to east 10, north 3.
# F7 would move the ship another 7 units east (because the ship is still facing east) to east 17, north 3.
# R90 would cause the ship to turn right by 90 degrees and face south; it remains at east 17, north 3.
# F11 would move the ship 11 units south to east 17, south 8.
# At the end of these instructions, the ship's Manhattan distance (sum of the absolute values of its east/west position and its north/south position) from its starting position is 17 + 8 = 25.
#
# Figure out where the navigation instructions lead. What is the Manhattan distance between that location and the ship's starting position?
#
# To begin, get your puzzle input.
#

# Your puzzle answer was 820.
#
# The first half of this puzzle is complete! It provides one gold star: *
#
# --- Part Two ---
# Before you can give the destination to the captain, you realize that the actual action meanings were printed on the back of the instructions the whole time.
#
# Almost all of the actions indicate how to move a waypoint which is relative to the ship's position:
#
# Action N means to move the waypoint north by the given value.
# Action S means to move the waypoint south by the given value.
# Action E means to move the waypoint east by the given value.
# Action W means to move the waypoint west by the given value.
# Action L means to rotate the waypoint around the ship left (counter-clockwise) the given number of degrees.
# Action R means to rotate the waypoint around the ship right (clockwise) the given number of degrees.
# Action F means to move forward to the waypoint a number of times equal to the given value.
# The waypoint starts 10 units east and 1 unit north relative to the ship. The waypoint is relative to the ship; that is, if the ship moves, the waypoint moves with it.
#
# For example, using the same instructions as above:
#
# F10 moves the ship to the waypoint 10 times (a total of 100 units east and 10 units north), leaving the ship at east 100, north 10. The waypoint stays 10 units east and 1 unit north of the ship.
# N3 moves the waypoint 3 units north to 10 units east and 4 units north of the ship. The ship remains at east 100, north 10.
# F7 moves the ship to the waypoint 7 times (a total of 70 units east and 28 units north), leaving the ship at east 170, north 38. The waypoint stays 10 units east and 4 units north of the ship.
# R90 rotates the waypoint around the ship clockwise 90 degrees, moving it to 4 units east and 10 units south of the ship. The ship remains at east 170, north 38.
# F11 moves the ship to the waypoint 11 times (a total of 44 units east and 110 units south), leaving the ship at east 214, south 72. The waypoint stays 4 units east and 10 units south of the ship.
# After these operations, the ship's Manhattan distance from its starting position is 214 + 72 = 286.
#
# Figure out where the navigation instructions actually lead. What is the Manhattan distance between that location and the ship's starting position?


class Ferry:
    EAST = "E"
    WEST = "W"
    NORTH = "N"
    SOUTH = "S"
    CLOCKWISE = "CWISE"
    COUNTERCLOCKWISE = "C/CWISE"

    def __init__(self, start_x=0, start_y=0, waypoint_start_x=10, waypoint_start_y=-1):
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        self.waypoint_x = waypoint_start_x
        self.waypoint_y = waypoint_start_y

    def distance_from_start(self):
        """
        return the Manhattan distance from the starting point
        """
        x_distance = abs(self.start_x - self.x)
        y_distance = abs(self.start_y - self.y)
        total_distance = x_distance + y_distance
        return total_distance

    def print(self):
        """
        print out the current location, distance from start, current direction
        """
        print(
            f"ship at ({self.x}, {self.y}) waypoint is at ({self.waypoint_x}, {self.waypoint_y}) ({self.distance_from_start()} from start)"
        )

    def command_forward(self, extent, params):
        """
        Move the ship forward to the waypoint extent times
        params are ignored
        """
        x_offset, y_offset = self.waypoint_x, self.waypoint_y
        self.x += extent * x_offset
        self.y += extent * y_offset
        return True

    def command_move_waypoint(self, extent, params):
        """
        move the waypoint, no turning, params is a tuple of x_offset, y_offset
        """
        x_offset, y_offset = params
        self.waypoint_x += extent * x_offset
        self.waypoint_y += extent * y_offset
        return True

    def command_rotate_waypoint(self, extent, params):
        """
        rotate waypoint either clockwise or counterclockwise (params) around the ship by the number of degrees in extent
        """
        # ok, firstly, more than 360 degrees is just short turning with more steps so eliminate that
        extent %= 360
        # next, counter-clockwise is just negative clockwise
        if params == self.COUNTERCLOCKWISE:
            extent = 360 - extent
        # ok, so always clockwise, we have a number of degrees, should be 0, 90, 180, 270, anything else is bananas
        twist_amount = [0, 90, 180, 270]
        if extent not in twist_amount:
            raise ValueError(
                f"Trying to rotate by {extent} degrees? Sorry buddy, can't do it"
            )

        # right, so this is a little more complicated..
        # if we imagine a point that is 7 north and 1 east of the ship (1, -7)
        # 90 degrees of rotation should be 7 east and 1 south (7, 1)
        # rotating 180 should give us (-1, 7)
        # rotating to the full 270 should give us (-7, -1)
        # so the full 360, which we don't do, is.. (1, -7)
        # so for a 90 degree clockwise turn of (x, y) -> (-y, x)
        # lazy version then.. we could pre-calculate each of these but it's a weekend after all

        twist_idx = twist_amount.index(extent)
        # we have a twist_idx of 0-3, we know how to make the change
        for this_turn in range(twist_idx):
            self.waypoint_x, self.waypoint_y = -self.waypoint_y, self.waypoint_x

        return True

    def execute_command(self, action, extent):
        """
        Based on the current ship position, execute the action passed to the extent specified
        """
        result = None
        command_list = {
            "F": (self.command_forward, None),
            "N": (self.command_move_waypoint, (0, -1)),
            "S": (self.command_move_waypoint, (0, 1)),
            "W": (self.command_move_waypoint, (-1, 0)),
            "E": (self.command_move_waypoint, (1, 0)),
            "R": (self.command_rotate_waypoint, self.CLOCKWISE),
            "L": (self.command_rotate_waypoint, self.COUNTERCLOCKWISE),
        }
        if action in command_list:
            command_function, params = command_list[action]
            result = command_function(extent, params)
        else:
            raise ValueError(f"No idea how to execute command {action}")
        return result

    def follow_instructions_file(self, filename):
        """
        Read the provided file and follow each instruction contained therein
        """
        with open(filename, "r") as f:
            for this_line in f:
                this_line = this_line.strip()
                if "" != this_line:
                    # got a line, split it..
                    command = this_line[0]
                    extent = int(this_line[1:])
                    print(f"Next command: {command} for {extent}")
                    # and execute that bad-boy
                    self.execute_command(command, extent)
                    self.print()


# main
ferry = Ferry()
ferry.print()

filename = "input.txt"
ferry.follow_instructions_file(filename)
