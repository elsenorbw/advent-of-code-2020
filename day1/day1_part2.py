# --- Day 1: Report Repair ---
# After saving Christmas five years in a row, you've decided to take a
# vacation at a nice resort on a tropical island. Surely, Christmas will go
# on without you.
#
# The tropical island has its own currency and is entirely cash-only. The gold
# coins used there have a little picture of a starfish; the locals just call
# them stars. None of the currency exchanges seem to have heard of them, but
# somehow, you'll need to find fifty of these coins by the time you arrive
# so you can pay the deposit on your room.
#
# To save your vacation, you need to get all fifty stars by December 25th.
#
# Collect stars by solving puzzles. Two puzzles will be made available on each
# day in the Advent calendar; the second puzzle is unlocked when you complete
# the first. Each puzzle grants one star. Good luck!
#
# Before you leave, the Elves in accounting just need you to fix your expense
# report (your puzzle input); apparently, something isn't quite adding up.
#
# Specifically, they need you to find the two entries that sum to 2020 and
# then multiply those two numbers together.
#
# For example, suppose your expense report contained the following:
#
# 1721
# 979
# 366
# 299
# 675
# 1456
# In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying
# them together produces 1721 * 299 = 514579, so the correct answer is 514579.
#
# Of course, your expense report is much larger. Find the two entries that sum
# to 2020; what do you get if you multiply them together?
#
# To begin, get your puzzle input.
# Your puzzle answer was 138379.
#
# The first half of this puzzle is complete! It provides one gold star: *
#
# --- Part Two ---
# The Elves in accounting are thankful for your help; one of them even offers you
# a starfish coin they had left over from a past vacation. They offer you a second
# one if you can find three numbers in your expense report that meet the same criteria.
#
# Using the above example again, the three entries that sum to 2020 are 979,
# 366, and 675. Multiplying them together produces the answer, 241861950.
#
# In your expense report, what is the product of the three entries that sum to 2020?
#


from typing import Set, Tuple

filename = "input.txt"


def load_list_to_set(filename: str) -> Set[int]:
    """
    Given a filename we should read each line, treat it as an int and
    add it to a resulting set
    """
    result = set()
    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            print(this_line)
            result.add(int(this_line))
    return result


def locate_2020_pair(
    possibilities: Set[int], target_value: int = 2020
) -> Tuple[int, int]:
    """
    Return a tuple of the first pair of integers in the list that meet the target value
    """
    result = None
    for x in possibilities:
        y = target_value - x
        if y in possibilities:
            result = (x, y)
            break
    return result


def locate_2020_triplet(
    possibilities: Set[int], target_value: int = 2020
) -> Tuple[int, int, int]:
    """
    Return a tuple of the 3 values which add up to target_value
    """
    result = None
    for x in possibilities:
        remainder = target_value - x
        remaining_values = possibilities.copy()
        remaining_values.remove(x)
        other_pair = locate_2020_pair(remaining_values, target_value=remainder)
        if other_pair is not None:
            result = (x, *other_pair)
            break
    return result


# load the list
the_list = load_list_to_set(filename)

# find the 2020 pair
the_pair = locate_2020_pair(the_list)

# print the pair and the result
print(f"{the_pair} -> {the_pair[0] * the_pair[1]}")

# and the triplet
the_triplet = locate_2020_triplet(the_list)
print(
    f"{the_triplet} -> {sum(the_triplet)} -> {the_triplet[0] * the_triplet[1] * the_triplet[2]}"
)
