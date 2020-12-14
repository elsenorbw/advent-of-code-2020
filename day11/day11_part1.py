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

# Conway tribute then..


class ConwayMachine:

    EMPTY = "L"
    OCCUPIED = "#"

    def __init__(self):
        self.seats = dict()
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

        self.print()

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
        possible_locations = [
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1),
        ]

        count = 0
        for x, y in possible_locations:
            if self.seat_occupied(x, y):
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
                # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
                occupied_neighbours = self.count_neighbours(x, y, stop_at=4)
                if occupied_neighbours >= 4:
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
