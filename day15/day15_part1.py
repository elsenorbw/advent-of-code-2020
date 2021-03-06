# --- Day 15: Rambunctious Recitation ---
# You catch the airport shuttle and try to book a new flight to your vacation island. Due to the storm, all direct flights have been cancelled, but a route is available to get around the storm. You take it.
#
# While you wait for your flight, you decide to check in with the Elves back at the North Pole. They're playing a memory game and are ever so excited to explain the rules!
#
# In this game, the players take turns saying numbers. They begin by taking turns reading from a list of starting numbers (your puzzle input). Then, each turn consists of considering the most recently spoken number:
#
# If that was the first time the number has been spoken, the current player says 0.
# Otherwise, the number had been spoken before; the current player announces how many turns apart the number is from when it was previously spoken.
# So, after the starting numbers, each turn results in that player speaking aloud either 0 (if the last number is new) or an age (if the last number is a repeat).
#
# For example, suppose the starting numbers are 0,3,6:
#
# Turn 1: The 1st number spoken is a starting number, 0.
# Turn 2: The 2nd number spoken is a starting number, 3.
# Turn 3: The 3rd number spoken is a starting number, 6.
# Turn 4: Now, consider the last number spoken, 6. Since that was the first time the number had been spoken, the 4th number spoken is 0.
# Turn 5: Next, again consider the last number spoken, 0. Since it had been spoken before, the next number to speak is the difference between the turn number when it was last spoken (the previous turn, 4) and the turn number of the time it was most recently spoken before then (turn 1). Thus, the 5th number spoken is 4 - 1, 3.
# Turn 6: The last number spoken, 3 had also been spoken before, most recently on turns 5 and 2. So, the 6th number spoken is 5 - 2, 3.
# Turn 7: Since 3 was just spoken twice in a row, and the last two turns are 1 turn apart, the 7th number spoken is 1.
# Turn 8: Since 1 is new, the 8th number spoken is 0.
# Turn 9: 0 was last spoken on turns 8 and 4, so the 9th number spoken is the difference between them, 4.
# Turn 10: 4 is new, so the 10th number spoken is 0.
# (The game ends when the Elves get sick of playing or dinner is ready, whichever comes first.)
#
# Their question for you is: what will be the 2020th number spoken? In the example above, the 2020th number spoken will be 436.
#
# Here are a few more examples:
#
# Given the starting numbers 1,3,2, the 2020th number spoken is 1.
# Given the starting numbers 2,1,3, the 2020th number spoken is 10.
# Given the starting numbers 1,2,3, the 2020th number spoken is 27.
# Given the starting numbers 2,3,1, the 2020th number spoken is 78.
# Given the starting numbers 3,2,1, the 2020th number spoken is 438.
# Given the starting numbers 3,1,2, the 2020th number spoken is 1836.
# Given your starting numbers, what will be the 2020th number spoken?
#
# Your puzzle input is 0,14,1,3,7,9.
from collections import defaultdict


def play_game(starting_numbers, iterations=2020, verbose=True):
    """
    Run n iterations of the game and return the number that will be spoken at that time
    """
    all_values = [-1]
    value_seen_at = defaultdict(list)

    # 1) add the initial list
    for this_turn_number, this_number in enumerate(starting_numbers, start=1):
        all_values.append(this_number)
        value_seen_at[this_number].append(this_turn_number)
    # and a little printing action..
    if verbose:
        print(
            f"list:{all_values}, dict: {value_seen_at}, this_turn:{this_turn_number}, this_number: {this_number}"
        )

    # 2) ok, so we now loop until we're done..
    #    at the top of the loop, this_number is the previous value stored
    #    and this_turn_number is the previous turn number..
    while this_turn_number < iterations:
        # next one then..
        this_turn_number += 1

        # ok, consider the last number, has it been said more than once ?
        if 2 <= len(value_seen_at[this_number]):
            # It has, we need to calculate the difference
            this_number = (
                value_seen_at[this_number][-1] - value_seen_at[this_number][-2]
            )
        else:
            # first time, so the answer is 0
            this_number = 0

        # and now store this number
        all_values.append(this_number)
        value_seen_at[this_number].append(this_turn_number)

        # and print if we're printing
        if verbose:
            print(
                f"list:{all_values}, dict: {value_seen_at}, this_turn:{this_turn_number}, this_number: {this_number}"
            )

    # and we have finished
    if verbose:
        print(f"returning result {this_number}")
    return this_number


# main
test_cases = [
    ((0, 3, 6), 436),
    ((1, 3, 2), 1),
    ((2, 1, 3), 10),
    ((1, 2, 3), 27),
    ((2, 3, 1), 78),
    ((3, 2, 1), 438),
    ((3, 1, 2), 1836),
]

puzzle_input = (0, 14, 1, 3, 7, 9)

for the_input, expected in test_cases:
    actual = play_game(the_input, iterations=2020, verbose=False)
    print(f"input: {the_input}, expected={expected}, actual={actual}")

part1_answer = play_game(puzzle_input, iterations=2020, verbose=False)
print(f"Part 1 answer: {part1_answer}")