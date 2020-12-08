# --- Day 7: Handy Haversacks ---
# You land at the regional airport in time for your next flight. In fact, it looks like you'll even have time to grab some food: all flights are currently delayed due to issues in luggage processing.
#
# Due to recent aviation regulations, many rules (your puzzle input) are being enforced about bags and their contents; bags must be color-coded and must contain specific quantities of other color-coded bags.
# Apparently, nobody responsible for these regulations considered how long they would take to enforce!
#
# For example, consider the following rules:
#
# light red bags contain 1 bright white bag, 2 muted yellow bags.
# dark orange bags contain 3 bright white bags, 4 muted yellow bags.
# bright white bags contain 1 shiny gold bag.
# muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
# shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# faded blue bags contain no other bags.
# dotted black bags contain no other bags.
# These rules specify the required contents for 9 bag types. In this example, every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded blue and 6 dotted black), and so on.
#
# You have a shiny gold bag. If you wanted to carry it in at least one other bag, how many different bag colors would be valid for the outermost bag? (In other words: how many colors can, eventually, contain at least one shiny gold bag?)
#
# In the above rules, the following options would be available to you:
#
# A bright white bag, which can hold your shiny gold bag directly.
# A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
# A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
# A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
# So, in this example, the number of bag colors that can eventually contain at least one shiny gold bag is 4.
#
# How many bag colors can eventually contain at least one shiny gold bag? (The list of rules is quite long; make sure you get all of it.)
#
# To begin, get your puzzle input.
#

# Your puzzle answer was 169.

# The first half of this puzzle is complete! It provides one gold star: *

# --- Part Two ---
# It's getting pretty expensive to fly these days - not because of ticket prices, but because of the ridiculous number of bags you need to buy!

# Consider again your shiny gold bag and the rules from the above example:

# faded blue bags contain 0 other bags.
# dotted black bags contain 0 other bags.
# vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
# dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.
# So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2 + 2*11 = 32 bags!

# Of course, the actual rules have a small chance of going several levels deeper than this example; be sure to count all of the bags, even if the nesting becomes topologically impractical!

# Here's another example:

# shiny gold bags contain 2 dark red bags.
# dark red bags contain 2 dark orange bags.
# dark orange bags contain 2 dark yellow bags.
# dark yellow bags contain 2 dark green bags.
# dark green bags contain 2 dark blue bags.
# dark blue bags contain 2 dark violet bags.
# dark violet bags contain no other bags.
# In this example, a single shiny gold bag must contain 126 other bags.

# How many individual bags are required inside your single shiny gold bag?


# a bag type to contain the necessary data
class Bag:
    def __init__(self, colour: str):
        self.contains_list = dict()
        self.colour = colour

    def add_contains_rule(self, quantity: int, contained_bag):
        self.contains_list[contained_bag] = quantity

    def can_eventually_contain(self, target_bag):
        """
        return True if this bag or any bag it can contain can contain the target bag
        """
        result = False

        # check each child
        for this_child in self.contains_list.keys():
            # is this bag our bag ?
            if target_bag == this_child.colour:
                result = True
            elif this_child.can_eventually_contain(target_bag):
                result = True

        return result

    def count_contained_bags(self) -> int:
        """
        return the number of bags required to fill this bag, excluding itself
        """
        result = 0

        for this_kid_bag, this_kid_bag_quantity in self.contains_list.items():
            kid_bag_size = this_kid_bag.count_contained_bags()
            result += this_kid_bag_quantity  # add the actual kid bags
            result += (
                this_kid_bag_quantity * kid_bag_size
            )  # and each of them have x contained bags inside

        return result

    def __repr__(self):
        return str(self)

    def __str__(self):
        result = f"A {self.colour} bag containing:"
        if 0 < len(self.contains_list.keys()):
            sep = " "
            for this_bag in self.contains_list:
                this_colour = this_bag.colour
                quantity = self.contains_list[this_bag]
                result += f"{sep}{quantity} {this_colour}"
                sep = ", "
        else:
            result += " nothing"
        return result


def declutter(s):
    """
    Remove the trailing . and any reference to bag[s]
    """
    result = s.strip()
    if result.endswith("."):
        result = result[:-1]
    result = result.replace("bags", "")
    result = result.replace("bag", "")
    return result


def parse_one_bag_rule(the_rule: str):
    """
    takes one line with a bag rule on it
    returns the name of the bag and a list of (child-bag, child-bag-count) tuples
    example inputs:
        bright white bags contain 1 shiny gold bag.
        muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
        shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
        dark olive bags contain 3 faded blue bags, 4 dotted black bags.
        vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
        faded blue bags contain no other bags.
    """
    clean_rule = declutter(the_rule)
    parts = clean_rule.split("contain")
    bag_name = parts[0].strip()
    bag_children = []
    kids = parts[1].split(",")
    for this_kid in kids:
        this_kid = this_kid.strip()
        # handle one child record and push it into the bag_children result
        if "no other" != this_kid:
            # we have a number then a description
            kid_parts = this_kid.split(" ", maxsplit=1)
            kid_quantity = int(kid_parts[0])
            kid_name = kid_parts[1]
            kid_tuple = (kid_quantity, kid_name)
            bag_children.append(kid_tuple)

    return bag_name, bag_children


# ok, so let's get the parsing bit done first
def load_bag_rules(filename: str):
    """
    Load all the bag rules from the file
    Format is:
    <identifier> bags contain <list>
    <list> is 1 or more <quantity> <identifier> bag[s],
    quantity is either "no" or an int

    currently (part 1) the quantities are irrelevant
    """
    all_bags = dict()

    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                # ok, parse this one line
                this_bag_name, this_bag_contains = parse_one_bag_rule(this_line)
                # now ensure that this bag is in the list
                if this_bag_name not in all_bags:
                    all_bags[this_bag_name] = Bag(this_bag_name)
                # and attach all the kids
                for this_kid_quantity, this_kid_name in this_bag_contains:
                    # if this one isn't in the list already then we need to create it, the contents will get set later presumably
                    if this_kid_name not in all_bags:
                        all_bags[this_kid_name] = Bag(this_kid_name)
                    # and now add the reference..
                    all_bags[this_bag_name].add_contains_rule(
                        this_kid_quantity, all_bags[this_kid_name]
                    )

    return all_bags


# main program
filename = "input.txt"
rules = load_bag_rules(filename)

# ok, we have the rules, and the question now is, how many bags can contain at least one shiny gold bag ?
target_bag_colour = "shiny gold"
target_bag = rules[target_bag_colour]

total_bag_count = target_bag.count_contained_bags()
print(f"total_bag_count for {target_bag} is {total_bag_count}")
