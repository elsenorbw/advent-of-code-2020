#
#  Need to investigate the relationship between the repeating nature of sets of numbers
#  the basic problem is that we have a series of increments, offsets: call them i[1], o[1]
#  we want to find the x where for each i,o pair x+o % i == 0
#
#  for example, (7,0), (9,1)
#

# borrowed from part1 due to lazy
def schedule_to_list(schedule):
    """
    Given a string of "1,x, 2, x, 3, 90" return a list of (bus_id, list_offset) tuples:  (1, 0), (2, 2), (3, 4), (90, 5)
    """
    result = []
    for list_offset, this_item in enumerate(schedule.split(",")):
        this_item = this_item.strip()
        if "x" != this_item:
            result.append((int(this_item), list_offset))
    return result


# so obviously there is a starting point which is always 0, but ignoring that, the real useful point is i-o and then each one is i * n - o
# ok, so is there any pattern in where they meet ?
def print_set_progression(set_1, set_2):
    intersect = list(sorted(set_1.intersection(set_2)))
    print(f"Intersection is {intersect}")
    s = f"{intersect[0]}"
    for idx in range(1, len(intersect)):
        old_val = intersect[idx - 1]
        new_val = intersect[idx]
        diff = new_val - old_val
        s += f" (+{diff}) {new_val}"
    print(f"Progression: {s}")


def calculate_possible_values(the_increment, the_offset, range_max):
    """
    calculate valid values in the range 0..range_max(-1)
    """
    result = set()
    for i in range(range_max):
        remainder = (i + the_offset) % the_increment
        if 0 == remainder:
            result.add(i)
    return result


seven_zero = calculate_possible_values(7, 0, 1000)
print(f"7,0: {sorted(seven_zero)}")

nine_one = calculate_possible_values(9, 1, 1000)
print(f"9,1: {sorted(nine_one)}")

nine_two = calculate_possible_values(9, 2, 1000)
print(f"9,2: {sorted(nine_two)}")


matches = seven_zero.intersection(nine_one)
print(f"intersection 7,0 - 9,1 is {sorted(matches)}")
print_set_progression(seven_zero, nine_one)

matches = seven_zero.intersection(nine_two)
print(f"intersection 7,0 - 9,2 is {sorted(matches)}")
print_set_progression(seven_zero, nine_two)

# well, that's interesting, the progression steps in fixed increments regardless of the offsets (which I guess makes sense)
# let's try it with some bigger numbers where we know some results..
def compare_acceptable_values(inc_off_one, inc_off_two, range_max):
    print(
        f"\n\ncomparing acceptable values for {inc_off_one} and {inc_off_two} up to {range_max}"
    )
    possible_one = calculate_possible_values(inc_off_one[0], inc_off_one[1], range_max)
    possible_two = calculate_possible_values(inc_off_two[0], inc_off_two[1], range_max)
    print_set_progression(possible_one, possible_two)


compare_list = [
    ((7, 0), (9, 1), 1000),
    ((7, 0), (9, 2), 1000),
    ((9, 0), (7, 1), 1000),
    ((17, 0), (19, 3), 5000),
    # and one to make sure the logic is sound..
    # ((1789, 0), (1889, 3), 1300000000),
    # that worked, commented it out because it's very slow doing it this way..
    # that took a while but it worked.. ok, so we can definitely optimise with this.. for any given pair we can generate a starting offset and an increment of potential values..
    # that would be interesting, but I suspect that it's not the whole story, what happens when we throw another variable into the mix.. oh wait..
    # are we saying that actually, two of these progressions boil down to effectively a new progression with an offset and an increment ? Looks like it since the gap is always the same..
    # cool cool, so maybe we can calculate these two value between a pairing and generate a new value for that, do the same against that result and the next pair until we have a final list
    # pair, and somehow the result of that will be the answer ?
    # worth a go I think.. let's rock.
]
for this_one, this_two, this_range in compare_list:
    compare_acceptable_values(this_one, this_two, this_range)


# right along that thinking then.. we need to find a smart way to turn a pair of (inc, off) values into a new (inc, off) value..
# merging the values together and walking along.
# let's sort out the logic to get the two values into one place first

# I wonder if common factors would be a problem here... I guess we'll see (or not)
class IncOff:
    def __init__(self, increment, offset):
        self.inc = increment
        self.off = offset
        self.current_value = increment - offset

    def __str__(self):
        return f"({self.inc}, {self.off}) -> {self.current_value}"

    def __repr__(self):
        return str(self)

    def next(self):
        self.current_value += self.inc
        return self.current_value

    def fast_increment(self, target_value):
        # increment until we are at or beyond the target_value
        diff = target_value - self.current_value
        # so we have an amount to cover, let's say it's 70
        inc_count = (diff + self.inc - 1) // self.inc
        # print(            f"FastIncrement: ({self.inc},{self.off}), current={self.current_value}, target={target_value}, diff={diff}, inc_count={inc_count}"        )
        # and now we know how many times we need to increment
        self.current_value += self.inc * inc_count
        # and a failsafe
        if 0 == inc_count:
            exit(32)

    def value(self):
        return self.current_value


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


# ok, so we can merge one pair, now let's merge 4 pairs and see if we can answer the first question


# real input
expected_result, schedule = (
    None,
    "23,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,37,x,x,x,x,x,479,x,x,x,x,x,x,x,x,x,x,x,x,13,x,x,x,17,x,x,x,x,x,x,x,x,x,x,x,29,x,373,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,19",
)

# sample input from part 1
# start_time, schedule = (939, "7, 13, x, x, 59, x, 31, 19")

# first example, small result space, brute force expected to work
# expected_result, schedule = (3417, "17,x,13,19")
# larger example..
# expected_result, schedule = (754018, "67,7,59,61")
# larger again
# expected_result, schedule = (779210, "67,x,7,59,61")
# and starting to get big..
# expected_result, schedule = (1261476, "67,7,x,59,61")
# and quite large..
# expected_result, schedule = (1202161486, "1789,37,47,1889")


def naive_solve(sched):
    print(f"Scheduled and offsets are: {sched}")
    while len(sched) > 1:
        # reduce the first two into dust..
        new_int_off = combine_pairs(sched[0], sched[1])
        sched = [new_int_off, *sched[2:]]
        print(f"Scheduled and offsets are now: {sched}")

    # could it be this easy ?
    answer = sched[0][0] - sched[0][1]
    print(f"answer is {answer}")
    return answer


def extract_increment(int_off_tuple):
    return int_off_tuple[0]


def smallest_pairs_solve(sched):
    print(f"\n\n\nsmallest_pairs_solve\n\n\n")
    print(f"Scheduled and offsets are: {sched}")
    while len(sched) > 1:
        # sort the list in order of smallest first
        sched.sort(key=extract_increment)
        print(f"Sorted scheduled and offsets are: {sched}")
        # reduce the first two into dust..
        new_int_off = combine_pairs(sched[0], sched[1])
        sched = [new_int_off, *sched[2:]]
        print(f"Scheduled and offsets are now: {sched}")

    # could it be this easy ?
    answer = sched[0][0] - sched[0][1]
    print(f"answer is {answer}")
    return answer


sched = schedule_to_list(schedule)
result = smallest_pairs_solve(sched)


# this worked for 3417
# and 754018
# and all the rest.. ok
# not the prettiest thing you'll ever see.. oh.. we could do faster incrementing logic.. hang on..
# we know how much ground there is to cover, so we can just add that much more in a single go..
# let's try that..

# so that all works, but it gets slow, easier to combine numbers of about the same size..
# perhaps we should be trying to find the smallest two increments and combining them first
# going to add that, although I suspect this would finish within an hour


# hmm, even the smallest_pairs method is taking ages, admittedly on the last pair
# maybe we need to think a bit harder about how to calculate where two pairs will intersect
# perhaps there's some way of calculating that which is smarter than just looping until we get there
# in fact, there really should be or my name's not Captain Dave Starbuck - Space Adventurer..
