# --- Day 18: Operation Order ---
# As you look out the window and notice a heavily-forested continent slowly appear over the horizon, you are interrupted by the child sitting next to you. They're curious if you could help them with their math homework.
#
# Unfortunately, it seems like this "math" follows different rules than you remember.
#
# The homework (your puzzle input) consists of a series of expressions that consist of addition (+), multiplication (*), and parentheses ((...)).
# Just like normal math, parentheses indicate that the expression inside must be evaluated before it can be used by the surrounding expression.
# Addition still finds the sum of the numbers on both sides of the operator, and multiplication still finds the product.
#
# However, the rules of operator precedence have changed. Rather than evaluating multiplication before addition, the operators have the same precedence, and are evaluated left-to-right regardless of the order in which they appear.
#
# For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as follows:
#
# 1 + 2 * 3 + 4 * 5 + 6
#   3   * 3 + 4 * 5 + 6
#       9   + 4 * 5 + 6
#          13   * 5 + 6
#              65   + 6
#                  71
# Parentheses can override this order; for example, here is what happens if parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):
#
# 1 + (2 * 3) + (4 * (5 + 6))
# 1 +    6    + (4 * (5 + 6))
#      7      + (4 * (5 + 6))
#      7      + (4 *   11   )
#      7      +     44
#             51
# Here are a few more examples:
#
# 2 * 3 + (4 * 5) becomes 26.
# 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
# 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
# ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.
# Before you can help with the homework, you need to understand it yourself. Evaluate the expression on each line of the homework; what is the sum of the resulting values?
#
# To begin, get your puzzle input.
#

# so left-to-right parsing, so that should prevent the need for a tree
# however we need to treat parentheses as a single item and run them first..


def is_operator(s):
    """
    is s one of the valid operators ?
    """
    return s in ("+", "*")


def apply_operator(lhs: int, op: str, rhs: int) -> int:
    """
    Apply operator op to the left and right hand side values
    """
    if "+" == op:
        result = lhs + rhs
    elif "*" == op:
        result = lhs * rhs
    elif "$" == op:
        # this is the initial state, we just use the rhs value
        result = rhs
    else:
        raise RuntimeError("No idea how to operate on {op}")

    return result


def parse_expression(ex: str, verbose=False) -> int:
    """
    left to right evaluation of simple expressions
    """
    if verbose:
        print(f"parsing:[{ex}]")
    # lazy way, find any parentheses and execute them first
    start_idx = ex.find("(")
    while -1 != start_idx:
        # find the matching end-paren
        open_count = 1
        end_idx = start_idx + 1
        while open_count > 0 and end_idx < len(ex):
            if ")" == ex[end_idx]:
                open_count -= 1
            elif "(" == ex[end_idx]:
                open_count += 1
            end_idx += 1
        # did we find the end ?
        if open_count > 0:
            raise RuntimeError("No closing paren found")
        # ok, so grab this part..
        sub_ex = ex[start_idx + 1 : end_idx - 1]
        # get the value for that..
        sub_ex_result = parse_expression(sub_ex, verbose=verbose)
        # and replace it..
        prefix = ex[:start_idx]
        postfix = ex[end_idx + 1 :]
        ex = f"{prefix} {sub_ex_result} {postfix}"
        if verbose:
            print(f"Adjusted expression[{ex}]")

        # and look for the next one..
        start_idx = ex.find("(")

    # ok, so we have a clean expression at this point, just split it on spaces and walk left to right doing the maths..
    result = 0
    op = "$"
    terms = ex.split(" ")
    for this_term in terms:
        this_term = this_term.strip()
        if "" != this_term:
            # either it's an operator or a number..
            if is_operator(this_term):
                # store it for use with the next number..
                op = this_term
            else:
                # must be a number
                int_term = int(this_term)
                # apply the logic..
                result = apply_operator(result, op, int_term)
    return result


test_cases = [
    ("1 + 2 * 3 + 4 * 5 + 6", 71),
    ("1 + (2 * 3) + (4 * (5 + 6))", 51),
    ("2 * 3 + (4 * 5)", 26),
    ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
    ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
    ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632),
]

for expression, expected in test_cases:
    x = parse_expression(expression)
    print(f"Parsing: {expression}, expected {expected}, actual {x}")
    if x != expected:
        raise RuntimeError("Failed the test bro..")


# now run all the expressions in the file and add up the answers..
filename = "input.txt"
part1_total = 0
with open(filename, "r") as f:
    for this_line in f:
        this_line = this_line.strip()
        if "" != this_line:
            x = parse_expression(this_line)
            print(f"{this_line} -> {x}")
            part1_total += x
print(f"part1 answer is {part1_total}")
