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

# Your puzzle answer was 21993583522852.
#
# The first half of this puzzle is complete! It provides one gold star: *
#
# --- Part Two ---
# You manage to answer the child's questions and they finish part 1 of their homework, but get stuck when they reach the next section: advanced math.
#
# Now, addition and multiplication have different precedence levels, but they're not the ones you're familiar with. Instead, addition is evaluated before multiplication.
#
# For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are now as follows:
#
# 1 + 2 * 3 + 4 * 5 + 6
#   3   * 3 + 4 * 5 + 6
#   3   *   7   * 5 + 6
#   3   *   7   *  11
#      21       *  11
#          231
# Here are the other examples from above:
#
# 1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
# 2 * 3 + (4 * 5) becomes 46.
# 5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
# 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
# ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.
# What do you get if you add up the results of evaluating the homework problems using these new rules?


# so no longer left-to-right parsing, damn..
# only two types of operator though, so lazy is possible..
# reduce everything to just operators and numbers..
# find out if there are any additions to do, if so reduce them..
# then run the multiplications the same way


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

    # ok, so we have a clean expression without parens..
    result = 0
    terms = [s for s in ex.split(" ") if "" != s]
    print(f" Initial terms: {terms}")

    # ok, first precedence is +, so going to find any of those and run them first
    for idx, this_term in reversed(list(enumerate(terms))):
        if "+" == this_term:
            # we have the idx, so..
            lhs = int(terms[idx - 1])
            rhs = int(terms[idx + 1])
            new_val = lhs + rhs
            # remove the other part
            terms[idx - 1] = new_val
            terms.pop(idx)
            terms.pop(idx)
            print(f"Modified terms: {terms}")

    # ok, now the multiplication is the last thing, so just going to run through multiplying..
    # in fact, everything left is a multiplication, can ignore the operators..
    result = 1
    for x in range(0, len(terms), 2):
        int_x = int(terms[x])
        result *= int_x

    return result


test_cases = [
    ("1 + 2 * 3 + 4 * 5 + 6", 231),
    ("1 + (2 * 3) + (4 * (5 + 6))", 51),
    ("2 * 3 + (4 * 5)", 46),
    ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445),
    ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060),
    ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340),
]

for expression, expected in test_cases:
    print(f"Parsing: {expression}")
    x = parse_expression(expression)
    print(f"Parsing: {expression}, expected {expected}, actual {x}")
    if x != expected:
        raise RuntimeError("Failed the test bro..")


# now run all the expressions in the file and add up the answers..
filename = "input.txt"
part2_total = 0
with open(filename, "r") as f:
    for this_line in f:
        this_line = this_line.strip()
        if "" != this_line:
            x = parse_expression(this_line)
            print(f"{this_line} -> {x}")
            part2_total += x
print(f"part1 answer is {part2_total}")
