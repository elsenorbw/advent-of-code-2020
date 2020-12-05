# --- Day 5: Binary Boarding ---
# You board your plane only to discover a new problem: you dropped your
# boarding pass! You aren't sure which seat is yours, and all of the flight
# attendants are busy with the flood of people that suddenly made it through
# passport control.
#
# You write a quick program to use your phone's camera to scan all of the
# nearby boarding passes (your puzzle input); perhaps you can find your
# seat through process of elimination.
#
# Instead of zones or groups, this airline uses binary space partitioning to
# seat people. A seat might be specified like FBFBBFFRLR, where F means
# "front", B means "back", L means "left", and R means "right".
#
# The first 7 characters will either be F or B; these specify exactly one of
# the 128 rows on the plane (numbered 0 through 127). Each letter tells you
# which half of a region the given seat is in. Start with the whole list of
# rows; the first letter indicates whether the seat is in the front
# (0 through 63) or the back (64 through 127). The next letter indicates which
# half of that region the seat is in, and so on until you're left with exactly
# one row.
#
# For example, consider just the first seven characters of FBFBBFFRLR:
#
# Start by considering the whole range, rows 0 through 127.
# F means to take the lower half, keeping rows 0 through 63.
# B means to take the upper half, keeping rows 32 through 63.
# F means to take the lower half, keeping rows 32 through 47.
# B means to take the upper half, keeping rows 40 through 47.
# B keeps rows 44 through 47.
# F keeps rows 44 through 45.
# The final F keeps the lower of the two, row 44.
# The last three characters will be either L or R; these specify exactly one
# of the 8 columns of seats on the plane (numbered 0 through 7). The same
# process as above proceeds again, this time with only three steps. L means to
# keep the lower half, while R means to keep the upper half.
#
# For example, consider just the last 3 characters of FBFBBFFRLR:
#
# Start by considering the whole range, columns 0 through 7.
# R means to take the upper half, keeping columns 4 through 7.
# L means to take the lower half, keeping columns 4 through 5.
# The final R keeps the upper of the two, column 5.
# So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.
#
# Every seat also has a unique seat ID: multiply the row by 8, then add the
# column. In this example, the seat has ID 44 * 8 + 5 = 357.
#
# Here are some other boarding passes:
#
# BFFFBBFRRR: row 70, column 7, seat ID 567.
# FFFBBBFRRR: row 14, column 7, seat ID 119.
# BBFFBBFRLL: row 102, column 4, seat ID 820.
# As a sanity check, look through your list of boarding passes. What is the
# highest seat ID on a boarding pass?
#
# To begin, get your puzzle input.
#

from typing import Set


# so.. it's just binary.
def code_to_number(code: str) -> int:
    """
    The string contains a mix of BFLR characters
    B and R are 1s
    F and L are 0s
    return the value converted to an int
    """
    result = 0
    for this_character in code:
        # left shift the current value
        result = result << 1
        # set the lowest bit if necessary
        if this_character in "BR":
            result += 1
    return result


# print(code_to_number("BFFFBBFRRR"))
# print(code_to_number("FFFBBBFRRR"))
# print(code_to_number("BBFFBBFRLL"))


def load_all_seats(filename: str) -> int:
    """
    Given an input file of FBLR encoded seat numbers return a set of all the values
    """
    seats = set()
    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                this_seat = code_to_number(this_line)
                seats.add(this_seat)
    return seats


def find_empty_seats(seats: Set[int]) -> int:
    """
    Given a list of the populated seats find the missing one in the sequence
    """
    empty_seats = set()
    min_seat = min(seats)
    max_seat = max(seats)
    for this_seat in range(min_seat + 1, max_seat):
        if this_seat not in seats:
            empty_seats.add(this_seat)
    return empty_seats


all_seats = load_all_seats("input.txt")

part1_result = max(all_seats)
print(f"part1: highest seat number is {part1_result}")

empty_seats = find_empty_seats(all_seats)
print(f"part2: empty seats are {empty_seats}")
