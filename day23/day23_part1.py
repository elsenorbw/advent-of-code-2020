# --- Day 23: Crab Cups ---
# The small crab challenges you to a game! The crab is going to mix up some cups, and you have to predict where they'll end up.
#
# The cups will be arranged in a circle and labeled clockwise (your puzzle input). For example, if your labeling were 32415, there would be five cups in the circle;
# going clockwise around the circle from the first cup, the cups would be labeled 3, 2, 4, 1, 5, and then back to 3 again.
#
# Before the crab starts, it will designate the first cup in your list as the current cup. The crab is then going to do 100 moves.
#
# Each move, the crab does the following actions:
#
# The crab picks up the three cups that are immediately clockwise of the current cup.
# They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
# The crab selects a destination cup: the cup with a label equal to the current cup's label minus one.
# If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up.
# If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
# The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. They keep the same order as when they were picked up.
# The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
# For example, suppose your cup labeling were 389125467. If the crab were to do merely 10 moves, the following changes would occur:
#
# -- move 1 --
# cups: (3) 8  9  1  2  5  4  6  7
# pick up: 8, 9, 1
# destination: 2
#
# -- move 2 --
# cups:  3 (2) 8  9  1  5  4  6  7
# pick up: 8, 9, 1
# destination: 7
#
# -- move 3 --
# cups:  3  2 (5) 4  6  7  8  9  1
# pick up: 4, 6, 7
# destination: 3
#
# -- move 4 --
# cups:  7  2  5 (8) 9  1  3  4  6
# pick up: 9, 1, 3
# destination: 7
#
# -- move 5 --
# cups:  3  2  5  8 (4) 6  7  9  1
# pick up: 6, 7, 9
# destination: 3
#
# -- move 6 --
# cups:  9  2  5  8  4 (1) 3  6  7
# pick up: 3, 6, 7
# destination: 9
#
# -- move 7 --
# cups:  7  2  5  8  4  1 (9) 3  6
# pick up: 3, 6, 7
# destination: 8
#
# -- move 8 --
# cups:  8  3  6  7  4  1  9 (2) 5
# pick up: 5, 8, 3
# destination: 1
#
# -- move 9 --
# cups:  7  4  1  5  8  3  9  2 (6)
# pick up: 7, 4, 1
# destination: 5
#
# -- move 10 --
# cups: (5) 7  4  1  8  3  9  2  6
# pick up: 7, 4, 1
# destination: 3
#
# -- final --
# cups:  5 (8) 3  7  4  1  9  2  6
# In the above example, the cups' values are the labels as they appear moving clockwise around the circle; the current cup is marked with ( ).
#
# After the crab is done, what order will the cups be in? Starting after the cup labeled 1, collect the other cups' labels clockwise into a single string with no extra characters;
# each number except 1 should appear exactly once. In the above example, after 10 moves, the cups clockwise from 1 are labeled 9, 2, 6, 5, and so on, producing 92658374.
# If the crab were to complete all 100 moves, the order after cup 1 would be 67384529.
#
# Using your labeling, simulate 100 moves. What are the labels on the cups after cup 1?
#
# Your puzzle input is 589174263.
#


class CrabCups:
    def __init__(self, initial_configuration: str):
        self.cups = [int(x) for x in initial_configuration.strip()]
        self.cup_count = len(self.cups)
        self.current_cup = self.cups[0]
        self.min_cup_id = min(self.cups)
        self.max_cup_id = max(self.cups)

    def current_cup_idx(self):
        """
        return the index of the current cup, it moves around while we poke and prod the list
        """
        return self.cups.index(self.current_cup)

    def print(self, description: str = None):
        s = ""
        sep = ""
        for idx in range(len(self.cups)):
            s += sep
            if idx == self.current_cup_idx():
                s += f"({self.cups[idx]})"
            else:
                s += f"{self.cups[idx]}"
            sep = " "

        if description is not None:
            desc = f" <--- {description}"
        else:
            desc = ""

        print(
            f"cups: {s} min: {self.min_cup_id}, max: {self.max_cup_id}, count: {self.cup_count}, current={self.current_cup}@{self.current_cup_idx()} {desc}"
        )

    def take_cup_after(self, idx: int):
        """
        remove the cup after the provided index from the list and return it
        """
        target_idx = idx + 1
        if target_idx >= len(self.cups):
            target_idx = 0

        result = self.cups[target_idx]
        del self.cups[target_idx]
        return result

    def find_next_destination(self, current_cup: int):
        """
        # The crab selects a destination cup: the cup with a label equal to the current cup's label minus one.
        # If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up.
        # If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
        """
        target_cup = current_cup - 1
        # keep going until we find a valid cup
        while target_cup not in self.cups:
            target_cup -= 1
            if target_cup < self.min_cup_id:
                target_cup = self.max_cup_id
        # we have the value, now we need the idx
        target_idx = self.cups.index(target_cup)
        return target_idx

    def add_cups(self, target_idx, cups_to_insert):
        """
        insert [cups_to_insert] to the right of target_idx
        """
        part_a = self.cups[0 : target_idx + 1]
        part_b = self.cups[target_idx + 1 :]
        print(f"cups: {self.cups} part_a[{part_a}], part_b[{part_b}]")
        self.cups = part_a + cups_to_insert + part_b

    def select_next_cup(self):
        """
        Update the current cup value..
        """
        idx = self.current_cup_idx()
        idx += 1
        if idx >= len(self.cups):
            idx = 0
        self.current_cup = self.cups[idx]

    def play_one_move(self):
        """
        Make one move in the cup game..
            # The crab picks up the three cups that are immediately clockwise of the current cup.
            # They are removed from the circle; cup spacing is adjusted as necessary to maintain the circle.
            # The crab selects a destination cup: the cup with a label equal to the current cup's label minus one.
            # If this would select one of the cups that was just picked up, the crab will keep subtracting one until it finds a cup that wasn't just picked up.
            # If at any point in this process the value goes below the lowest value on any cup's label, it wraps around to the highest value on any cup's label instead.
            # The crab places the cups it just picked up so that they are immediately clockwise of the destination cup. They keep the same order as when they were picked up.
            # The crab selects a new current cup: the cup which is immediately clockwise of the current cup.
        """
        self.print("top of move")
        # 1) grab three cups
        c1 = self.take_cup_after(self.current_cup_idx())
        c2 = self.take_cup_after(self.current_cup_idx())
        c3 = self.take_cup_after(self.current_cup_idx())
        print(f"pick up: {c1}, {c2}, {c3}")
        self.print("after pickup")

        # 2) find a destination cup
        destination_idx = self.find_next_destination(self.current_cup)
        print(
            f"destination index is {destination_idx}, cup is {self.cups[destination_idx]}"
        )

        # 3) insert cups back into the circle
        self.add_cups(destination_idx, [c1, c2, c3])
        self.print("after adding cups..")

        # 4) select the next cup
        self.select_next_cup()

        self.print("post move")

    def play(self, moves: int):
        for move_no in range(1, moves + 1):
            print(f"-- move {move_no} --")
            self.print(f"before move {move_no}")
            self.play_one_move()
            self.print(f"after move {move_no}")

    def score(self):
        """
        After the crab is done, what order will the cups be in?
        Starting after the cup labeled 1, collect the other cups' labels clockwise into a single string with no extra characters;
        each number except 1 should appear exactly once.
        """
        result = 0

        idx = self.cups.index(1)
        idx += 1
        if idx >= len(self.cups):
            idx = 0
        # ok, keep adding things until we get back to 1
        while 1 != self.cups[idx]:
            # add this value..
            result *= 10
            result += self.cups[idx]
            # and on to the next one..
            idx += 1
            if idx >= len(self.cups):
                idx = 0

        return result


# main


games = [
    ("389125467", 10, 92658374),
    ("389125467", 100, 67384529),
    ("589174263", 100, None),
]

for starting_position, required_iterations, expected_result in games:
    c = CrabCups(starting_position)
    c.play(required_iterations)
    actual = c.score()
    print(
        f"start: {starting_position}, iterations={required_iterations}, expected={expected_result}, actual={actual}"
    )
    if expected_result is not None and actual != expected_result:
        print(f"Problem here chief..")
        exit(1)
