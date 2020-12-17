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


# So it'll take longer to parse the input than to do the thinking.. sad times, oh well..


class TicketRules:
    def __init__(self):
        self.rules = dict()
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

    def value_valid_for_any_field(self, i):
        """
        Would i be acceptable for any field ?
        """
        result = i in self.valid_values
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
def calculate_error_rate(filename):
    """
    Calculate the error rate of the tickets from the input file..
    """
    result = 0

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
                    # don't need this one for now
                    pass
                else:
                    # so this is a nearby passenger ticket
                    passenger_details = csv_to_int_list(this_line)
                    for this_field in passenger_details:
                        if not rules.value_valid_for_any_field(this_field):
                            # this is not valid, add it to the total
                            result += this_field

    return result


# main
filename = "input.txt"
answer = calculate_error_rate(filename)
print(f"part1_answer is : {answer}")