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

# sample input
# start_time, schedule = (939, "7, 13, x, x, 59, x, 31, 19")
# real input
start_time, schedule = (
    1000417,
    "23,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,37,x,x,x,x,x,479,x,x,x,x,x,x,x,x,x,x,x,x,13,x,x,x,17,x,x,x,x,x,x,x,x,x,x,x,29,x,373,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,19",
)


def schedule_to_list(schedule):
    """
    Given a string of "1,x, 2, x, 3" return a list of 1,2,3
    """
    result = []
    for this_item in schedule.split(","):
        this_item = this_item.strip()
        if "x" != this_item:
            result.append(int(this_item))
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


# main
sched = schedule_to_list(schedule)
print(f"Looking for a bus at {start_time} in {sched}")
next_arrivals = find_starting_time(start_time, sched)
best_time = min(next_arrivals.keys())

# the first bus we can catch is..
bus_options_for_best_time = next_arrivals[best_time]
first_bus = bus_options_for_best_time[0]
# result is multiplying them for some reason
part1_result = first_bus * best_time
print(f"part1_result is {part1_result}")
