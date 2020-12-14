# --- Day 13: Shuttle Search ---
# Your ferry can make it safely to a nearby port, but it won't get much further. When you call to book another ship, you discover that no ships embark from that port to your vacation island. You'll need to get from the port to the nearest airport.
#
# Fortunately, a shuttle bus service is available to bring you from the sea port to the airport! Each bus has an ID number that also indicates how often the bus leaves for the airport.
#
# Bus schedules are defined based on a timestamp that measures the number of minutes since some fixed reference point in the past. At timestamp 0, every bus simultaneously departed from the sea port.
# After that, each bus travels to the airport, then various other locations, and finally returns to the sea port to repeat its journey forever.
#
# The time this loop takes a particular bus is also its ID number: the bus with ID 5 departs from the sea port at timestamps 0, 5, 10, 15, and so on. The bus with ID 11 departs at 0, 11, 22, 33, and so on.
# If you are there when the bus departs, you can ride that bus to the airport!
#
# Your notes (your puzzle input) consist of two lines. The first line is your estimate of the earliest timestamp you could depart on a bus.
# The second line lists the bus IDs that are in service according to the shuttle company; entries that show x must be out of service, so you decide to ignore them.
#
# To save time once you arrive, your goal is to figure out the earliest bus you can take to the airport. (There will be exactly one such bus.)
#
# For example, suppose you have the following notes:
#
# 939
# 7,13,x,x,59,x,31,19
# Here, the earliest timestamp you could depart is 939, and the bus IDs in service are 7, 13, 59, 31, and 19. Near timestamp 939, these bus IDs depart at the times marked D:
#
# time   bus 7   bus 13  bus 59  bus 31  bus 19
# 929      .       .       .       .       .
# 930      .       .       .       D       .
# 931      D       .       .       .       D
# 932      .       .       .       .       .
# 933      .       .       .       .       .
# 934      .       .       .       .       .
# 935      .       .       .       .       .
# 936      .       D       .       .       .
# 937      .       .       .       .       .
# 938      D       .       .       .       .
# 939      .       .       .       .       .
# 940      .       .       .       .       .
# 941      .       .       .       .       .
# 942      .       .       .       .       .
# 943      .       .       .       .       .
# 944      .       .       D       .       .
# 945      D       .       .       .       .
# 946      .       .       .       .       .
# 947      .       .       .       .       .
# 948      .       .       .       .       .
# 949      .       D       .       .       .
# The earliest bus you could take is bus ID 59. It doesn't depart until timestamp 944, so you would need to wait 944 - 939 = 5 minutes before it departs. Multiplying the bus ID by the number of minutes you'd need to wait gives 295.
#
# What is the ID of the earliest bus you can take to the airport multiplied by the number of minutes you'll need to wait for that bus?

# Your puzzle answer was 171.
#
# The first half of this puzzle is complete! It provides one gold star: *
#
# --- Part Two ---
# The shuttle company is running a contest: one gold coin for anyone that can find the earliest timestamp such that the first bus ID departs at that time and each subsequent listed bus ID departs at that subsequent minute.
# (The first line in your input is no longer relevant.)
#
# For example, suppose you have the same list of bus IDs as above:
#
# 7,13,x,x,59,x,31,19
# An x in the schedule means there are no constraints on what bus IDs must depart at that time.
#
# This means you are looking for the earliest timestamp (called t) such that:
#
# Bus ID 7 departs at timestamp t.
# Bus ID 13 departs one minute after timestamp t.
# There are no requirements or restrictions on departures at two or three minutes after timestamp t.
# Bus ID 59 departs four minutes after timestamp t.
# There are no requirements or restrictions on departures at five minutes after timestamp t.
# Bus ID 31 departs six minutes after timestamp t.
# Bus ID 19 departs seven minutes after timestamp t.
# The only bus departures that matter are the listed bus IDs at their specific offsets from t. Those bus IDs can depart at other times, and other bus IDs can depart at those times. For example, in the list above,
# because bus ID 19 must depart seven minutes after the timestamp at which bus ID 7 departs, bus ID 7 will always also be departing with bus ID 19 at seven minutes after timestamp t.
#
# In this example, the earliest timestamp at which this occurs is 1068781:
#
# time     bus 7   bus 13  bus 59  bus 31  bus 19
# 1068773    .       .       .       .       .
# 1068774    D       .       .       .       .
# 1068775    .       .       .       .       .
# 1068776    .       .       .       .       .
# 1068777    .       .       .       .       .
# 1068778    .       .       .       .       .
# 1068779    .       .       .       .       .
# 1068780    .       .       .       .       .
# 1068781    D       .       .       .       .
# 1068782    .       D       .       .       .
# 1068783    .       .       .       .       .
# 1068784    .       .       .       .       .
# 1068785    .       .       D       .       .
# 1068786    .       .       .       .       .
# 1068787    .       .       .       D       .
# 1068788    D       .       .       .       D
# 1068789    .       .       .       .       .
# 1068790    .       .       .       .       .
# 1068791    .       .       .       .       .
# 1068792    .       .       .       .       .
# 1068793    .       .       .       .       .
# 1068794    .       .       .       .       .
# 1068795    D       D       .       .       .
# 1068796    .       .       .       .       .
# 1068797    .       .       .       .       .
# In the above example, bus ID 7 departs at timestamp 1068788 (seven minutes after t). This is fine; the only requirement on that minute is that bus ID 19 departs then, and it does.
#
# Here are some other examples:
#
# The earliest timestamp that matches the list 17,x,13,19 is 3417.
# 67,7,59,61 first occurs at timestamp 754018.
# 67,x,7,59,61 first occurs at timestamp 779210.
# 67,7,x,59,61 first occurs at timestamp 1261476.
# 1789,37,47,1889 first occurs at timestamp 1202161486.
# However, with so many bus IDs in your list, surely the actual earliest timestamp will be larger than 100000000000000!
#
# What is the earliest timestamp such that all of the listed bus IDs depart at offsets matching their positions in the list?


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


# find next starting time..
def find_starting_time(start_time, schedule):
    """
    Figure out when each bus is going to be here next and take the earliest one
    """
    next_arrival_times = dict()

    for this_bus_no in schedule:
        # figure out when this bus will next be here after the mentioned time
        x = start_time % this_bus_no
        if x > 0:
            x = this_bus_no - x
        print(
            f"bus#:{this_bus_no}  for a start_time of {start_time} will have to wait {x} minutes until {start_time + x}"
        )
        if x not in next_arrival_times:
            next_arrival_times[x] = []
        next_arrival_times[x].append(this_bus_no)

    return next_arrival_times


def rule_check(the_time, schedule, verbose=False):
    """
    Is it correct that the_time means that everything in the schedule arrives <list_offset> minutes after the specified time ?
    """
    result = True

    for this_bus_no, this_list_offset in schedule:
        x = (the_time + this_list_offset) % this_bus_no
        if 0 != x:
            result = False
            break

    if verbose:
        if result:
            print(f"successful check for {the_time}")
        else:
            print(f"checking time {the_time} failed because of bus {this_bus_no}")

    return result


def attempt_0(schedule):
    """
    approach 0: simple brute force, I know this won't work, but I want to check my rule logic is solid
    """
    candidate_time = 0
    checks_made = 1
    while not rule_check(candidate_time, schedule):
        candidate_time += 1
        checks_made += 1

    return candidate_time, checks_made


def attempt_1(schedule, cut_off_time=None, verbose=False):
    """
    approach 1: iterate through the possible values of the largest item, and check whether those values meet the rule
    """
    # finding the largest of the schedules
    largest_bus_id = schedule[0][0]
    largest_bus_id_list_offset = schedule[0][1]
    for this_bus_id, this_list_offset in schedule[1:]:
        if this_bus_id > largest_bus_id:
            largest_bus_id = this_bus_id
            largest_bus_id_list_offset = this_list_offset
    print(
        f"Largest bus_id is {largest_bus_id} with an offset of {largest_bus_id_list_offset}"
    )

    # going to start in the first location where this
    candidate_time = largest_bus_id - largest_bus_id_list_offset
    # we always make an initial check
    checks_made = 1

    while not rule_check(candidate_time, schedule, verbose) and (
        cut_off_time is None or candidate_time <= cut_off_time
    ):

        # next time that large id will be in the right slot
        candidate_time += largest_bus_id
        # and check again
        checks_made += 1

    return candidate_time, checks_made


# main

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

sched = schedule_to_list(schedule)
print(f"Scheduled and offsets are: {sched}")

# maybe we can solve this by walking the biggest number and seeing whether everything else lines up ? I'd imagine this will take too long but as a starter for 10 let's see

print(f"Expected result is {expected_result} for {sched}")
result = attempt_1(sched, cut_off_time=expected_result, verbose=False)
print(f"Result was {result[0]} using {result[1]} checks (expected {expected_result})")
