# --- Day 11: Seating System ---
# Your plane lands with plenty of time to spare. The final leg of your journey is a ferry that goes directly to the tropical island where you can finally start your vacation. As you reach the waiting area to board the ferry, you realize you're so early, nobody else has even arrived yet!
#
# By modeling the process people use to choose (or abandon) their seat in the waiting area, you're pretty sure you can predict the best place to sit. You make a quick map of the seat layout (your puzzle input).
#
# The seat layout fits neatly on a grid. Each position is either floor (.), an empty seat (L), or an occupied seat (#). For example, the initial seat layout might look like this:
#
# L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL
# Now, you just need to model the people who will be arriving shortly. Fortunately, people are entirely predictable and always follow a simple set of rules. All decisions are based on the number of occupied seats adjacent to a given seat (one of the eight positions immediately up, down, left, right, or diagonal from the seat). The following rules are applied to every seat simultaneously:
#
# If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
# If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
# Otherwise, the seat's state does not change.
# Floor (.) never changes; seats don't move, and nobody sits on the floor.
#
# After one round of these rules, every seat in the example layout becomes occupied:
#
# #.##.##.##
# #######.##
# #.#.#..#..
# ####.##.##
# #.##.##.##
# #.#####.##
# ..#.#.....
# ##########
# #.######.#
# #.#####.##
# After a second round, the seats with four or more occupied adjacent seats become empty again:
#
# #.LL.L#.##
# #LLLLLL.L#
# L.L.L..L..
# #LLL.LL.L#
# #.LL.LL.LL
# #.LLLL#.##
# ..L.L.....
# #LLLLLLLL#
# #.LLLLLL.L
# #.#LLLL.##
# This process continues for three more rounds:
#
# #.##.L#.##
# #L###LL.L#
# L.#.#..#..
# #L##.##.L#
# #.##.LL.LL
# #.###L#.##
# ..#.#.....
# #L######L#
# #.LL###L.L
# #.#L###.##
# #.#L.L#.##
# #LLL#LL.L#
# L.L.L..#..
# #LLL.##.L#
# #.LL.LL.LL
# #.LL#L#.##
# ..L.L.....
# #L#LLLL#L#
# #.LLLLLL.L
# #.#L#L#.##
# #.#L.L#.##
# #LLL#LL.L#
# L.#.L..#..
# #L##.##.L#
# #.#L.LL.LL
# #.#L#L#.##
# ..L.L.....
# #L#L##L#L#
# #.LLLLLL.L
# #.#L#L#.##
# At this point, something interesting happens: the chaos stabilizes and further applications of these rules cause no seats to change state! Once people stop moving around, you count 37 occupied seats.
#
# Simulate your seating area by applying the seating rules repeatedly until no seats change state. How many seats end up occupied?
#
# To begin, get your puzzle input.
#
# Your puzzle answer was 2211.
#
# The first half of this puzzle is complete! It provides one gold star: *
#
# --- Part Two ---
# As soon as people start to arrive, you realize your mistake. People don't just care about adjacent seats - they care about the first seat they can see in each of those eight directions!
#
# Now, instead of considering just the eight immediately adjacent seats, consider the first seat in each of those eight directions. For example, the empty seat below would see eight occupied seats:
#
# .......#.
# ...#.....
# .#.......
# .........
# ..#L....#
# ....#....
# .........
# #........
# ...#.....
# The leftmost empty seat below would only see one empty seat, but cannot see any of the occupied ones:
#
# .............
# .L.L.#.#.#.#.
# .............
# The empty seat below would see no occupied seats:
#
# .##.##.
# #.#.#.#
# ##...##
# ...L...
# ##...##
# #.#.#.#
# .##.##.
# Also, people seem to be more tolerant than you expected: it now takes five or more visible occupied seats for an occupied seat to become empty (rather than four or more from the previous rules). The other rules still apply: empty seats that see no occupied seats become occupied, seats matching no rule don't change, and floor never changes.
#
# Given the same starting layout as above, these new rules cause the seating area to shift around as follows:
#
# L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL
# #.##.##.##
# #######.##
# #.#.#..#..
# ####.##.##
# #.##.##.##
# #.#####.##
# ..#.#.....
# ##########
# #.######.#
# #.#####.##
# #.LL.LL.L#
# #LLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLL#
# #.LLLLLL.L
# #.LLLLL.L#
# #.L#.##.L#
# #L#####.LL
# L.#.#..#..
# ##L#.##.##
# #.##.#L.##
# #.#####.#L
# ..#.#.....
# LLL####LL#
# #.L#####.L
# #.L####.L#
# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##LL.LL.L#
# L.LL.LL.L#
# #.LLLLL.LL
# ..L.L.....
# LLLLLLLLL#
# #.LLLLL#.L
# #.L#LL#.L#
# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##L#.#L.L#
# L.L#.#L.L#
# #.L####.LL
# ..#.#.....
# LLL###LLL#
# #.LLLLL#.L
# #.L#LL#.L#
# #.L#.L#.L#
# #LLLLLL.LL
# L.L.L..#..
# ##L#.#L.L#
# L.L#.LL.L#
# #.LLLL#.LL
# ..#.L.....
# LLL###LLL#
# #.LLLLL#.L
# #.L#LL#.L#
# Again, at this point, people stop shifting around and the seating area reaches equilibrium. Once this occurs, you count 26 occupied seats.
#
# Given the new visibility method and the rule change for occupied seats becoming empty, once equilibrium is reached, how many seats end up occupied?

# Conway tribute then..


class ConwayMachine:

    EMPTY = "L"
    OCCUPIED = "#"

    def __init__(self):
        self.seats = dict()
        self.neighbours = dict()
        self.width = 0
        self.height = 0
        self.current_iteration = 0

    def load_seating_plan(self, filename: str):
        """
        Load a seating plan from a file:
          L -> seat
          . -> space
        """
        self.seats = {}
        self.width = 0
        self.height = 0

        with open(filename, "r") as f:
            y = -1
            for this_line in f:
                this_line = this_line.strip()
                if "" != this_line:
                    y += 1
                    for x, this_char in enumerate(this_line):
                        if "L" == this_char:
                            self.seats[(x, y)] = self.EMPTY
                        if x >= self.width:
                            self.width = x + 1

        # and store the height
        self.height = y + 1

        # and now, pre-calculate the neighbours for each of the seats in the array
        neighbour_directions = [
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            (1, 0),
            (-1, +1),
            (0, +1),
            (1, +1),
        ]

        for x, y in self.seats:
            self.neighbours[(x, y)] = []
            for x_increment, y_increment in neighbour_directions:
                this_neighbour = self.find_neighbour(x, y, x_increment, y_increment)
                if this_neighbour is not None:
                    self.neighbours[(x, y)].append(this_neighbour)

        self.print()

    def find_neighbour(self, x, y, x_increment, y_increment):
        """
        Return a tuple of (x,y) for the neighbour found or None if we walked off the edge of the grid looking
        """
        result = None
        x += x_increment
        y += y_increment
        while (
            result is None
            and x >= 0
            and y >= 0
            and x <= self.width
            and y <= self.height
        ):
            if self.has_seat(x, y):
                result = (x, y)
            else:
                x += x_increment
                y += y_increment
        return result

    def has_seat(self, x, y):
        """
        returns True / False for seat existence
        """
        return (x, y) in self.seats

    def seat_occupied(self, x, y):
        """
        True -> location is a seat and is populated with a person
        """
        return self.seats.get((x, y), self.EMPTY) == self.OCCUPIED

    def count_neighbours(self, x, y, stop_at=8):
        """
        Count the number of neighbours which are occupied, up to a maximum of stop_at
        """
        count = 0

        for target_x, target_y in self.neighbours[(x, y)]:
            if self.seat_occupied(target_x, target_y):
                count += 1
                if count >= stop_at:
                    break
        return count

    def iterate(self):
        """
        Run one set of the logic
        """
        # create a new set of values from the current set of values
        something_changed = False
        new_seats = dict()
        for (x, y), current_state in self.seats.items():
            new_state = current_state
            if self.EMPTY == current_state:
                # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
                occupied_neighbours = self.count_neighbours(x, y, stop_at=1)
                if 0 == occupied_neighbours:
                    new_state = self.OCCUPIED
                    something_changed = True
            else:
                # If a seat is occupied (#) and five or more seats adjacent to it are also occupied, the seat becomes empty.
                occupied_neighbours = self.count_neighbours(x, y, stop_at=5)
                if occupied_neighbours >= 5:
                    new_state = self.EMPTY
                    something_changed = True
            # store the new state
            new_seats[(x, y)] = new_state

        # and store the result
        self.seats = new_seats
        self.current_iteration += 1

        # and return whether anything changed
        return something_changed

    def print(self):
        """
        Output the current grid
        """
        occupied_count = 0
        print(f"Iteration {self.current_iteration}")
        for y in range(self.height):
            s = ""
            for x in range(self.width):
                if self.has_seat(x, y):
                    if self.seat_occupied(x, y):
                        s += "#"
                        occupied_count += 1
                    else:
                        s += "L"
                else:
                    s += "."
            print(s)
        print(f"Occupied seats: {occupied_count}")
        print("")


# main
filename = "input.txt"
conway = ConwayMachine()
conway.load_seating_plan(filename)

# conway.print()
while conway.iterate():
    conway.print()

conway.print()
