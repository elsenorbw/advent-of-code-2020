#
#  trying to improve the logic for combining a pair of (inc,off)'s
#

# this is the maive version to beat..
# and as I type, the answer has arrived..
# so that method worked ok..
# but we could probably do better


def combine_pairs(inc_off_one, inc_off_two):
    print(f"Combining [{inc_off_one}] with [{inc_off_two}]")
    a = IncOff(*inc_off_one)
    b = IncOff(*inc_off_two)
    print(f"{a}   ---   {b}")
    # ok, step one is to find the first intersection
    while a.value() != b.value():
        # increment the smaller one..
        if a.value() < b.value():
            a.next()
        else:
            b.next()
    print(f"{a}   ---   {b}")
    # ok, cool, we have the starting value..
    start_value = a.value()
    # now find the next time they meet
    a.next()
    b.next()
    while a.value() != b.value():
        # increment the smaller one..
        if a.value() < b.value():
            a.fast_increment(b.value())
        else:
            b.fast_increment(a.value())
    print(f"{a}   ---   {b}")
    next_value = a.value()
    # so now we know the increment as well..
    increment = next_value - start_value
    print(f"increment is {increment}")
    # the offset then is..
    offset = increment - start_value
    print(f"offset is {offset}")
    # and we're done..
    return (increment, offset)


new_pair = combine_pairs((7, 0), (9, 2))
print(f"new pair is: {new_pair}")
