# --- Day 19: Monster Messages ---
# You land in an airport surrounded by dense forest. As you walk to your high-speed train, the Elves at the Mythical Information Bureau contact you again.
# They think their satellite has collected an image of a sea monster! Unfortunately, the connection to the satellite is having problems, and many of the messages sent back from the satellite have been corrupted.
#
# They sent you a list of the rules valid messages should obey and a list of received messages they've collected so far (your puzzle input).
#
# The rules for valid messages (the top part of your puzzle input) are numbered and build upon each other. For example:
#
# 0: 1 2
# 1: "a"
# 2: 1 3 | 3 1
# 3: "b"
# Some rules, like 3: "b", simply match a single character (in this case, b).
#
# The remaining rules list the sub-rules that must be followed; for example, the rule 0: 1 2 means that to match rule 0, the text being checked must match rule 1, and the text after the part that matched rule 1 must then match rule 2.
#
# Some of the rules have multiple lists of sub-rules separated by a pipe (|). This means that at least one list of sub-rules must match. (The ones that match might be different each time the rule is encountered.)
# For example, the rule 2: 1 3 | 3 1 means that to match rule 2, the text being checked must match rule 1 followed by rule 3 or it must match rule 3 followed by rule 1.
#
# Fortunately, there are no loops in the rules, so the list of possible matches will be finite. Since rule 1 matches a and rule 3 matches b, rule 2 matches either ab or ba. Therefore, rule 0 matches aab or aba.
#
# Here's a more interesting example:
#
# 0: 4 1 5
# 1: 2 3 | 3 2
# 2: 4 4 | 5 5
# 3: 4 5 | 5 4
# 4: "a"
# 5: "b"
# Here, because rule 4 matches a and rule 5 matches b, rule 2 matches two letters that are the same (aa or bb), and rule 3 matches two letters that are different (ab or ba).
#
# Since rule 1 matches rules 2 and 3 once each in either order, it must match two pairs of letters, one pair with matching letters and one pair with different letters.
# This leaves eight possibilities: aaab, aaba, bbab, bbba, abaa, abbb, baaa, or babb.
#
# Rule 0, therefore, matches a (rule 4), then any of the eight options from rule 1, then b (rule 5): aaaabb, aaabab, abbabb, abbbab, aabaab, aabbbb, abaaab, or ababbb.
#
# The received messages (the bottom part of your puzzle input) need to be checked against the rules so you can determine which are valid and which are corrupted. Including the rules and the messages together, this might look like:
#
# 0: 4 1 5
# 1: 2 3 | 3 2
# 2: 4 4 | 5 5
# 3: 4 5 | 5 4
# 4: "a"
# 5: "b"
#
# ababbb
# bababa
# abbbab
# aaabbb
# aaaabbb
# Your goal is to determine the number of messages that completely match rule 0. In the above example, ababbb and abbbab match, but bababa, aaabbb, and aaaabbb do not, producing the answer 2. The whole message must match all of rule 0; there can't be extra unmatched characters in the message. (For example, aaaabbb might appear to match rule 0 above, but it has an extra unmatched b on the end.)
#
# How many messages completely match rule 0?
#
# To begin, get your puzzle input.

# Your puzzle answer was 144.
#
# The first half of this puzzle is complete! It provides one gold star: *
#
# --- Part Two ---
# As you look over the list of messages, you realize your matching rules aren't quite right. To fix them, completely replace rules 8: 42 and 11: 42 31 with the following:
#
# 8: 42 | 42 8
# 11: 42 31 | 42 11 31
# This small change has a big impact: now, the rules do contain loops, and the list of messages they could hypothetically match is infinite. You'll need to determine how these changes affect which messages are valid.
#
# Fortunately, many of the rules are unaffected by this change; it might help to start by looking at which rules always match the same set of values and how those rules (especially rules 42 and 31) are used by the new versions of rules 8 and 11.
#
# (Remember, you only need to handle the rules you have; building a solution that could handle any hypothetical combination of rules would be significantly more difficult.)
#
# For example:
#
# 42: 9 14 | 10 1
# 9: 14 27 | 1 26
# 10: 23 14 | 28 1
# 1: "a"
# 11: 42 31
# 5: 1 14 | 15 1
# 19: 14 1 | 14 14
# 12: 24 14 | 19 1
# 16: 15 1 | 14 14
# 31: 14 17 | 1 13
# 6: 14 14 | 1 14
# 2: 1 24 | 14 4
# 0: 8 11
# 13: 14 3 | 1 12
# 15: 1 | 14
# 17: 14 2 | 1 7
# 23: 25 1 | 22 14
# 28: 16 1
# 4: 1 1
# 20: 14 14 | 1 15
# 3: 5 14 | 16 1
# 27: 1 6 | 14 18
# 14: "b"
# 21: 14 1 | 1 14
# 25: 1 1 | 1 14
# 22: 14 14
# 8: 42
# 26: 14 22 | 1 20
# 18: 15 15
# 7: 14 5 | 1 21
# 24: 14 1
#
# abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
# bbabbbbaabaabba
# babbbbaabbbbbabbbbbbaabaaabaaa
# aaabbbbbbaaaabaababaabababbabaaabbababababaaa
# bbbbbbbaaaabbbbaaabbabaaa
# bbbababbbbaaaaaaaabbababaaababaabab
# ababaaaaaabaaab
# ababaaaaabbbaba
# baabbaaaabbaaaababbaababb
# abbbbabbbbaaaababbbbbbaaaababb
# aaaaabbaabaaaaababaa
# aaaabbaaaabbaaa
# aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
# babaaabbbaaabaababbaabababaaab
# aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
# Without updating rules 8 and 11, these rules only match three messages: bbabbbbaabaabba, ababaaaaaabaaab, and ababaaaaabbbaba.
#
# However, after updating rules 8 and 11, a total of 12 messages match:
#
# bbabbbbaabaabba
# babbbbaabbbbbabbbbbbaabaaabaaa
# aaabbbbbbaaaabaababaabababbabaaabbababababaaa
# bbbbbbbaaaabbbbaaabbabaaa
# bbbababbbbaaaaaaaabbababaaababaabab
# ababaaaaaabaaab
# ababaaaaabbbaba
# baabbaaaabbaaaababbaababb
# abbbbabbbbaaaababbbbbbaaaababb
# aaaaabbaabaaaaababaa
# aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
# aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
# After updating rules 8 and 11, how many messages completely match rule 0?


# ok, going to keep the rules and run them all each time..
# there could be millions of valid combinations, so enmumerating them all ahead of time is probably not a good look but we'll see
# not over-sure how this is going to work out, let's see..
# each rule is basically either:
#  - a string literal match
#  - a list of [lists of other rules]
#
#  when we evaulate a rule to decide whether it completely matches we need to know if the string matched all the rules, and what, if any string is left over..
#  so evaluating the rule "a" on "abc" needs to return True, "bc"
#  a top-level rule is valid only if it returns a True, ""
#

#
#  slightly worried that there may be rules of different lengths in the same node, which would make the evaluation rules a bit more complicated, as we'd have to try them all
#  and somehow deal with returning multiple tuples of (True, "xyz"), (True, "z").. a cursory look at the rules suggests that this isn't the case, so going to add a check
#  at load time.
#

#
#  ok, so now we have rules of different lengths, and there is the possibility that multiple different rulesets on the same rule will return valid results with different length remainder strings..
#  need to accept that each thing will now need to return a list of 0 or more remainder strings instead of a single remainder string..
#  actually, this seems like it should be super easy (14:04)
#

from typing import Tuple, List


class MonsterMessages:
    def __init__(self):
        self.rules = dict()

    def add_rule(self, the_rule: str):
        """
        Parse and add a rule into the collection
        Formats are :
        0: 1 2
        1: "a"
        2: 1 3 | 3 1
        """
        # so split them into rule-no and rule body..
        parts = the_rule.split(":", maxsplit=1)
        if 2 != len(parts):
            raise RuntimeError(f"Got a rule without two bits:{the_rule}")
        rule_no = int(parts[0])
        rule_body = parts[1].strip()
        if rule_body.startswith('"'):
            # it's a literal..
            the_literal = rule_body[1:-1]
            actual_rule = LiteralNode(rule_no, the_literal)
        else:
            # it's the other sort..
            actual_rule = ListNode(rule_no, rule_body, self.rules)

        # and store the rule..
        self.rules[rule_no] = actual_rule

    def evaluate_rule(self, rule_no: int, value_to_check: str) -> bool:
        """
        Does the value passed completely match the specified rule ?
        """
        result = False

        result, remaining = self.rules[rule_no].evaluate(value_to_check)

        if result and "" not in remaining:
            # print(                f"rule {rule_no} matched fine, but left us with [{remaining}] so it's a no from me I'm afraid.."            )
            result = False

        return result


def depth_print(depth, s):
    """
    print s indented by depth space units
    """
    return None
    prefix = "--" * depth
    print(f"{prefix}{s}")


# There are, as mentioned two types of node, either a list of rules or a string literal
# each type needs to provide an evaluate(the_value) -> bool, remaining string

# first the simple string matcher
class LiteralNode:
    def __init__(self, rule_no: int, the_literal: str):
        self.literal = the_literal
        self.rule_no = rule_no

    def __repr__(self):
        return f"#{self.ruleno}: literal={self.literal}"

    def evaluate(self, the_value, depth=0) -> Tuple[bool, List[str]]:
        """
        if the string matches then return True and the remainder..
        else False and the whole string as nothing was consumed..
        """
        result = False
        if the_value.startswith(self.literal):
            result = True
            the_value = the_value[len(self.literal) :]
        # there is only ever a single result for a given literal
        depth_print(
            depth,
            f'{self.rule_no} ("{self.literal}"): returning {result}, {[the_value]}',
        )
        return result, [the_value]


# now the slightly more complicated string matcher..
class ListNode:
    def __init__(self, rule_no: int, list_of_lists_of_rules: str, rulebook: dict):
        """
        input will be a pipe delimted list of space delimited lists of ints and a reeference to the central store for rules
        """
        self.rulesets = []
        self.rule_no = rule_no
        self.rulebook = rulebook

        lists_of_rules = list_of_lists_of_rules.split("|")
        for this_list_of_rules in lists_of_rules:
            the_individual_rules = this_list_of_rules.split(" ")
            this_rule_list = [int(x) for x in the_individual_rules if x != ""]
            self.rulesets.append(this_rule_list)

    def __repr__(self):
        return f"#{self.rule_no}: sub-rules={self.rulesets}"

    def evaluate(self, the_value, depth=0) -> Tuple[bool, List[str]]:
        """
        if the string matches any of our rules in the ruleset then return True and the remainder..
        else False and the whole string as nothing was consumed..
        """
        all_remaining_values = set()

        depth_print(depth, f"{self}")

        # try each of our rules in turn, keeping all the winners..
        for this_rule in self.rulesets:
            # run this rule based on our single starting value..
            valid_at_start_of_step = [the_value]

            for this_rule_no in this_rule:
                # this is a step in the process
                # this step should be evaluated for every input in valid_at_start_of_step
                # if needs to generate a list for valid_after_step which will become the input to the next round or this final result if this is the last round
                depth_print(
                    depth,
                    f"{self.rule_no}: running sub_rule #{this_rule_no} against {valid_at_start_of_step}",
                )
                valid_after_step = list()
                for this_input_value in valid_at_start_of_step:
                    depth_print(
                        depth,
                        f"{self.rule_no}: executing rule #{this_rule_no} with input {this_input_value}",
                    )
                    # running this rule step for this particular input
                    result, valid_outputs = self.rulebook[this_rule_no].evaluate(
                        this_input_value, depth=depth + 1
                    )
                    if result:
                        # these are valid for the start of the next round..
                        valid_after_step.extend(valid_outputs)
                #
                #  so we now have a full set of values which are valid for the next round..
                #
                valid_at_start_of_step = valid_after_step

            #
            #  ok, so we've run one rule-set and we have some results, 0 or more valid answers..
            #
            all_remaining_values.update(valid_after_step)

        # ok, so we have all the answers in a set, so they're unique, either there are none (which is bad) or some (which is good)
        result_list = list(all_remaining_values)
        result = len(result_list) > 0

        depth_print(depth, f"{self.rule_no}: returning {result}, {result_list}")

        return result, result_list


# testing
if False:
    test_rules = ["0: 1 2", '1: "a"', "2: 1 3 | 3 1", '3: "b"']
    m = MonsterMessages()
    for this_rule in test_rules:
        m.add_rule(this_rule)

    test_cases = ["aab", "aabb", "abb", "bab"]
    for this_test in test_cases:
        x = m.evaluate_rule(0, this_test)
        print(f"checking {this_test} with rule 0 : {x}")

    exit(42)

# and the real-deal
filename = "input_part2.txt"
# filename = "sample3.txt"
m = MonsterMessages()
match_count = 0

with open(filename, "r") as f:
    in_rules_section = True
    for this_line in f:
        this_line = this_line.strip()
        if "" == this_line:
            in_rules_section = False
        else:
            # either this is a rule..
            if in_rules_section:
                m.add_rule(this_line)
            else:
                if not this_line.startswith("#"):
                    # we need to evaluate the rule 0 against this string..
                    matching = m.evaluate_rule(0, this_line)
                    print(f"{matching} -> {this_line}")
                    if matching:
                        match_count += 1
print(f"total matches: {match_count}")
