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
# Your puzzle answer was 43896725.
#
# The first half of this puzzle is complete! It provides one gold star: *
#
# --- Part Two ---
# Due to what you can only assume is a mistranslation (you're not exactly fluent in Crab), you are quite surprised when the crab starts arranging many cups in a circle on your raft - one million (1000000) in total.
#
# Your labeling is still correct for the first few cups; after that, the remaining cups are just numbered in an increasing fashion starting from the number after the highest number in your list and proceeding one by one until one million is reached.
# (For example, if your labeling were 54321, the cups would be numbered 5, 4, 3, 2, 1, and then start counting up from 6 until one million is reached.) In this way, every number from one through one million is used exactly once.
#
# After discovering where you made the mistake in translating Crab Numbers, you realize the small crab isn't going to do merely 100 moves; the crab is going to do ten million (10000000) moves!
#
# The crab is going to hide your stars - one each - under the two cups that will end up immediately clockwise of cup 1. You can have them if you predict what the labels on those cups will be when the crab is finished.
#
# In the above example (389125467), this would be 934001 and then 159792; multiplying these together produces 149245887792.
#
# Determine which two cups will end up immediately clockwise of cup 1. What do you get if you multiply their labels together?
#

from fast_circle_list import FastCircleList


class CrabCups:
    def __init__(self, initial_configuration: str):
        self.cups = FastCircleList()
        for x in initial_configuration.strip():
            self.cups.append(int(x))
        # now add the other cups up to 1 million
        cups_to_add = 1000000 - self.cups.item_count()
        initial_cup_value = self.cups.max_value() + 1
        for x in range(cups_to_add):
            self.cups.append(initial_cup_value + x)

        self.min_cup_id = self.cups.min_value()
        self.max_cup_id = self.cups.max_value()

    def print(self, desc: str = None):

        description = ""
        if desc is not None:
            description = desc

        self.cups.print(desc, walk=20)
        print(
            f"cups: min: {self.min_cup_id}, max: {self.max_cup_id}, count: {self.cups.item_count()}, current={self.cups.get_current_node()} {description}\n"
        )

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
        target_node = self.cups.locate_node(target_cup)
        return target_node

    def play_one_move(self, verbose=False):
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
        if verbose:
            self.print("top of move")

        # 1) grab three cups
        c1 = self.cups.remove_next_node()
        c2 = self.cups.remove_next_node()
        c3 = self.cups.remove_next_node()
        if verbose:
            print(f"pick up: {c1}, {c2}, {c3}")
            self.print("after pickup")

        # 2) find a destination cup
        destination_node = self.find_next_destination(
            self.cups.get_current_node().value
        )
        if verbose:
            print(f"destination node is {destination_node}")

        # 3) insert cups back into the circle
        self.cups.add_after(destination_node, c3.value)
        self.cups.add_after(destination_node, c2.value)
        self.cups.add_after(destination_node, c1.value)
        if verbose:
            self.print("after adding cups..")

        # 4) select the next cup
        target_cup = self.cups.get_current_node().next()
        self.cups.set_current_node(target_cup)

        if verbose:
            self.print("post move")

    def play(self, moves: int):
        for move_no in range(1, moves + 1):
            if move_no % 250000 == 0:
                print(f"-- move {move_no} --")
            # self.print(f"before move {move_no}")
            self.play_one_move(verbose=False)
            # self.print(f"after move {move_no}")

    def score(self):
        """
        Multiply the 2 cup numbers directly to the left of the #1 cup
        """
        result = 1
        one_node = self.cups.locate_node(1)
        a = one_node.next()
        b = a.next()

        result = a.value * b.value

        return result


# main

games = [
    ("389125467", 10000000, 149245887792),
    ("589174263", 10000000, None),
]

for starting_position, required_iterations, expected_result in games:
    c = CrabCups(starting_position)
    c.print()
    c.play(required_iterations)
    actual = c.score()
    print(
        f"start: {starting_position}, iterations={required_iterations}, expected={expected_result}, actual={actual}"
    )
    if expected_result is not None and actual != expected_result:
        print(f"Problem here chief..")
        exit(1)
