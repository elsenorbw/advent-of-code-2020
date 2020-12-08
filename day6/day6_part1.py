# --- Day 6: Custom Customs ---
# As your flight approaches the regional airport where you'll switch to a much larger plane, customs declaration forms are distributed to the passengers.
#
# The form asks a series of 26 yes-or-no questions marked a through z. All you need to do is identify the questions for which anyone in your group answers "yes". Since your group is just you, this doesn't take very long.
#
# However, the person sitting next to you seems to be experiencing a language barrier and asks if you can help. For each of the people in their group, you write down the questions for which they answer "yes", one per line. For example:
#
# abcx
# abcy
# abcz
# In this group, there are 6 questions to which anyone answered "yes": a, b, c, x, y, and z. (Duplicate answers to the same question don't count extra; each question counts at most once.)
#
# Another group asks for your help, then another, and eventually you've collected answers from every group on the plane (your puzzle input). Each group's answers are separated by a blank line,
# and within each group, each person's answers are on a single line. For example:
#
# abc
#
# a
# b
# c
#
# ab
# ac
#
# a
# a
# a
# a
#
# b
# This list represents answers from five groups:
#
# The first group contains one person who answered "yes" to 3 questions: a, b, and c.
# The second group contains three people; combined, they answered "yes" to 3 questions: a, b, and c.
# The third group contains two people; combined, they answered "yes" to 3 questions: a, b, and c.
# The fourth group contains four people; combined, they answered "yes" to only 1 question, a.
# The last group contains one person who answered "yes" to only 1 question, b.
# In this example, the sum of these counts is 3 + 3 + 3 + 1 + 1 = 11.
#
# For each group, count the number of questions to which anyone answered "yes". What is the sum of those counts?
#
# To begin, get your puzzle input.
from typing import List, Set


def get_group_answers(filename: str) -> List[Set[str]]:
    """
    blank-line separated groups of characters, each one indicating a yes to that particular question
    output a list of each group, with the set of each question which has been seen at least once
    """
    group_answers = []
    this_groups_answers = None

    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" == this_line:
                if this_groups_answers is not None:
                    group_answers.append(this_groups_answers)
                    this_groups_answers = None
            else:
                if this_groups_answers is None:
                    this_groups_answers = set()
                # add every character found into this group
                for this_char in this_line:
                    this_groups_answers.add(this_char)

    if this_groups_answers is not None:
        group_answers.append(this_groups_answers)

    return group_answers


filename = "input.txt"
group_answers = get_group_answers(filename)
# group_answers is now a list of sets of answers..
print(f"group_answers: {group_answers}")

group_counts = [len(x) for x in group_answers]
# group_counts now has the number of selected questions per group
print(f"group_counts: {group_counts}")


total = sum(group_counts)
# and this is part 1 answered
print(f"part1: total is {total}")