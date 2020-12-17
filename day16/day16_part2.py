# --- Day 16: Ticket Translation ---
# As you're walking to yet another connecting flight, you realize that one of the legs of your re-routed trip coming up is on a high-speed train.
# However, the train ticket you were given is in a language you don't understand. You should probably figure out what it says before you get to the train station after the next flight.
#
# Unfortunately, you can't actually read the words on the ticket. You can, however, read the numbers, and so you figure out the fields these tickets must have and the valid ranges for values in those fields.
#
# You collect the rules for ticket fields, the numbers on your ticket, and the numbers on other nearby tickets for the same train service (via the airport security cameras) together into a single document you can reference (your puzzle input).
#
# The rules for ticket fields specify a list of fields that exist somewhere on the ticket and the valid ranges of values for each field. For example, a rule like class: 1-3 or 5-7 means that one of the fields in every ticket is named class
# and can be any value in the ranges 1-3 or 5-7 (inclusive, such that 3 and 5 are both valid in this field, but 4 is not).
#
# Each ticket is represented by a single line of comma-separated values. The values are the numbers on the ticket in the order they appear; every ticket has the same format. For example, consider this ticket:
#
# .--------------------------------------------------------.
# | ????: 101    ?????: 102   ??????????: 103     ???: 104 |
# |                                                        |
# | ??: 301  ??: 302             ???????: 303      ??????? |
# | ??: 401  ??: 402           ???? ????: 403    ????????? |
# '--------------------------------------------------------'
# Here, ? represents text in a language you don't understand. This ticket might be represented as 101,102,103,104,301,302,303,401,402,403; of course, the actual train tickets you're looking at are much more complicated.
# In any case, you've extracted just the numbers in such a way that the first number is always the same specific field, the second number is always a different specific field, and so on - you just don't know what each position actually means!
#
# Start by determining which tickets are completely invalid; these are tickets that contain values which aren't valid for any field. Ignore your ticket for now.
#
# For example, suppose you have the following notes:
#
# class: 1-3 or 5-7
# row: 6-11 or 33-44
# seat: 13-40 or 45-50
#
# your ticket:
# 7,1,14
#
# nearby tickets:
# 7,3,47
# 40,4,50
# 55,2,20
# 38,6,12
# It doesn't matter which position corresponds to which field; you can identify invalid nearby tickets by considering only whether tickets contain values that are not valid for any field.
# In this example, the values on the first nearby ticket are all valid for at least one field. This is not true of the other three nearby tickets: the values 4, 55, and 12 are are not valid for any field.
# Adding together all of the invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.
#
# Consider the validity of the nearby tickets you scanned. What is your ticket scanning error rate?

# Your puzzle answer was 30869.
#
# The first half of this puzzle is complete! It provides one gold star: *
#
# --- Part Two ---
# Now that you've identified which tickets contain invalid values, discard those tickets entirely. Use the remaining valid tickets to determine which field is which.
#
# Using the valid ranges for each field, determine what order the fields appear on the tickets. The order is consistent between all tickets: if seat is the third field, it is the third field on every ticket, including your ticket.
#
# For example, suppose you have the following notes:
#
# class: 0-1 or 4-19
# row: 0-5 or 8-19
# seat: 0-13 or 16-19
#
# your ticket:
# 11,12,13
#
# nearby tickets:
# 3,9,18
# 15,1,5
# 5,14,9
# Based on the nearby tickets in the above example, the first position must be row, the second position must be class, and the third position must be seat; you can conclude that in your ticket, class is 12, row is 11, and seat is 13.
#
# Once you work out which field is which, look for the six fields on your ticket that start with the word departure. What do you get if you multiply those six values together?
import operator
from functools import reduce


class TicketRules:
    def __init__(self):
        self.rules = dict()
        self.valid_by_column = dict()
        # quick cache of all the valid values
        self.valid_values = set()

    def add_one_rule(self, rule_str):
        """
        take a string in the format
        arrival location: 48-154 or 166-965
        and store it appropriately
        """
        name, rule_components = rule_str.split(":")
        name = name.strip()
        self.rules[name] = []
        self.valid_by_column[name] = set()

        # and now handle each of the rules..
        components = rule_components.split("or")
        for this_rule in components:
            lo_str, hi_str = this_rule.split("-")
            lo = int(lo_str.strip())
            hi = int(hi_str.strip())
            # and store it
            self.rules[name].append((lo, hi))
            # and quick-cache it
            for i in range(lo, hi + 1):
                self.valid_values.add(i)
                self.valid_by_column[name].add(i)

    def value_valid_for_any_field(self, i):
        """
        Would i be acceptable for any field ?
        """
        result = i in self.valid_values
        return result

    def list_matching_column_rules(self, the_values):
        """
        given a set of values (the_values)
        return a list of all the named columns where this list could fit
        """
        result = []

        for this_col in self.valid_by_column.keys():
            # do all these values fit in this column ?
            diff = the_values.difference(self.valid_by_column[this_col])
            if 0 == len(diff):
                result.append(this_col)

        return result


# sanity check
if False:
    rules = TicketRules()
    rules.add_one_rule("departure location: 36-626 or 651-973")
    checker = [35, 36, 37, 625, 626, 627, 650, 651, 652, 972, 973, 974]
    for i in checker:
        res = rules.value_valid_for_any_field(i)
        print(f"{i} acceptable ? {res}")


def csv_to_int_list(s):
    return [int(x.strip()) for x in s.split(",")]


# ok, onto the parsing
def load_rules_and_valid_tickets(filename):
    """
    Return valid tickets and the set of named rules
    """
    valid_tickets = list()

    # get a rules engine
    rules = TicketRules()

    # parse the input file..
    parsing_rules = True
    parsing_my_ticket = False

    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if "" != this_line:
                # ok, is this a transition line ?
                if "your ticket:" == this_line:
                    parsing_rules = False
                    parsing_my_ticket = True
                elif "nearby tickets:" == this_line:
                    parsing_rules = False
                    parsing_my_ticket = False
                elif parsing_rules:
                    # this is a rule, add it
                    rules.add_one_rule(this_line)
                elif parsing_my_ticket:
                    this_ticket = csv_to_int_list(this_line)
                    valid_tickets.append(this_ticket)
                    pass
                else:
                    # so this is a nearby passenger ticket
                    passenger_details = csv_to_int_list(this_line)
                    ticket_valid = True
                    for this_field in passenger_details:
                        if not rules.value_valid_for_any_field(this_field):
                            # this is not valid, ignore it
                            ticket_valid = False
                    if ticket_valid:
                        valid_tickets.append(passenger_details)

    return rules, valid_tickets


def run_one_reduction(potentials):
    """
    Run the logic once to find a single change to make,
    True if we changed anything, False otherwise
    """
    result = False
    for this_col in potentials.keys():
        # is this a single value ?
        if 1 == len(potentials[this_col]):
            this_certainty = potentials[this_col][0]
            # print(f"column {this_col} is definitely {this_certainty}")
            # ok, do we need to remove this from everywhere else ?
            other_columns = set(potentials.keys())
            other_columns.remove(this_col)
            # print(f"other columns than {this_col} are {other_columns}")
            for target_col in other_columns:
                if this_certainty in potentials[target_col]:
                    potentials[target_col].remove(this_certainty)
                    result = True
            if result:
                break

    return result


def prod(iterable):
    return reduce(operator.mul, iterable, 1)


def get_field_order(rules, valid_tickets):
    """
    valid_tickets a list of valid tickets, where each field is in the same order on each ticket..
    """
    potentials = dict()
    # ok, starter for 10, find the range of each column and see which fields it could be
    for this_col in range(len(valid_tickets[0])):
        # we have the column, get all the seen values..
        values_seen = set()
        for this_ticket in valid_tickets:
            this_value = this_ticket[this_col]
            values_seen.add(this_value)
        # now, for each of the rule columns, are these valid values ?
        valid_for = rules.list_matching_column_rules(values_seen)
        print(f"column {this_col} could be {valid_for}")
        potentials[this_col] = valid_for

    # now for the reduction part..
    print(f"potentials: {potentials}")
    # there are 2 ways that we can decide a column..
    # either there is only one value that remains as a possibility for that column (in which case duh)
    # of this column is the only place where that particular value is still a possibility
    # starting with the simple one, only one value left for a column
    iteration = 1
    while run_one_reduction(potentials) and iteration < 1000:
        print(f"after [{iteration}] potentials: {potentials}")
        iteration += 1

    print(f"final potentials: {potentials}")

    #
    # ok, so we have the field order get the fields which start with departure
    #
    all_dep_field_idxs = []
    for this_idx in potentials.keys():
        if potentials[this_idx][0].startswith("departure"):
            all_dep_field_idxs.append(this_idx)
    print(f"Fields indexes we care about : {all_dep_field_idxs}")

    # and get all our values for those fields..
    our_values = [valid_tickets[0][idx] for idx in all_dep_field_idxs]
    print(f"Our values for those fields: {our_values}")

    # and the final answer
    part2_answer = prod(our_values)
    print(f"Part2 answer is: {part2_answer}")


# main
filename = "input.txt"
rules, valid_tickets = load_rules_and_valid_tickets(filename)
print(f"rules: {rules}\nvalid_tickets:{valid_tickets}")

# ok, solve it..
get_field_order(rules, valid_tickets)
