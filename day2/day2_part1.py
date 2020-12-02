# --- Day 2: Password Philosophy ---
# Your flight departs in a few days from the coastal airport; the easiest
# way down to the coast from here is via toboggan.

# The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day.
# "Something's wrong with our computers; we can't log in!" You ask
# if you can take a look.

# Their password database seems to be a little corrupted: some of the
# passwords wouldn't have been allowed by the Official Toboggan
# Corporate Policy that was in effect when they were chosen.

# To try to debug the problem, they have created a list (your puzzle input)
# of passwords (according to the corrupted database) and the corporate
# policy when that password was set.

# For example, suppose you have the following list:

# 1-3 a: abcde
# 1-3 b: cdefg
# 2-9 c: ccccccccc
# Each line gives the password policy and then the password. The password
# policy indicates the lowest and highest number of times a given letter
# must appear for the password to be valid. For example, 1-3 a means that
# the password must contain a at least 1 time and at most 3 times.

# In the above example, 2 passwords are valid.
# The middle password, cdefg, is not; it contains no instances of b, but
# needs at least 1.
# The first and third passwords are valid: they contain one a or nine c,
# both within the limits of their respective policies.

# How many passwords are valid according to their policies?
from typing import Tuple

filename = "input.txt"


def check_rule(
    min_count: int, max_count: int, pwd_char: str, pwd_to_check: str
) -> bool:
    """
    Check whether pwd_char exists between min-max times in pwd_to_check
    """
    the_count = pwd_to_check.count(pwd_char)
    result = the_count >= min_count and the_count <= max_count
    return result


def split_rule_and_value(s: str) -> Tuple[str, str]:
    """
    Given a string in the format rule: value
    return a tuple with the trimmed rule,value pair
    throwing on missing colons
    """
    pos = s.find(":")
    if -1 == pos:
        raise ValueError(f"split_rule_and_value: input string has no colon [{s}]")
    rule = s[:pos].strip()
    value = s[pos + 1 :].strip()
    return (rule, value)


def split_rule(s: str) -> Tuple[int, int, str]:
    """
    Return the component parts of the rule
    "min-max pwd_char"
    """
    dash = s.find("-")
    space = s.find(" ")
    if -1 == dash or -1 == space or space < dash:
        raise ValueError("weird rule format for {s} - {dash},{space}")
    min_s = s[:dash].strip()
    max_s = s[dash + 1 : space].strip()
    pwd_char = s[space:].strip()
    return (int(min_s), int(max_s), pwd_char)


def line_is_valid(the_line: str) -> bool:
    """
    Given a single string, determine whether it meets the rules
    format is x-y z: gggggg
    x: the minimum number of times z must appear in gggggg
    y: the maximum number of times z must appear
    z: the character that is important
    gggggg: the value to be checked
    """
    result = False
    rule, value = split_rule_and_value(the_line)
    # print(f"rule:[{rule}], value:[{value}]")
    min_count, max_count, pwd_char = split_rule(rule)
    # print(f"rule states that there must be at least {min_count} but no more than {max_count} instances of {pwd_char} in {value}")
    if check_rule(min_count, max_count, pwd_char, value):
        print(f"valid: {the_line}")
        result = True
    else:
        print(f"not valid: {the_line}")
    return result


def count_valid_passwords(filename: str) -> int:
    """
    Confirm how many of the passwords in the passed file meet the policy
    """
    result = 0
    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                # valid line
                if line_is_valid(this_line):
                    result += 1
    return result


valid_password_count = count_valid_passwords(filename)
print(f"file {filename} has {valid_password_count} valid passwords")
