# --- Day 10: Adapter Array ---
# Patched into the aircraft's data port, you discover weather forecasts of a massive tropical storm. Before you can figure out whether it will impact your vacation plans, however, your device suddenly turns off!
#
# Its battery is dead.
#
# You'll need to plug it in. There's only one problem: the charging outlet near your seat produces the wrong number of jolts. Always prepared, you make a list of all of the joltage adapters in your bag.
#
# Each of your joltage adapters is rated for a specific output joltage (your puzzle input). Any given adapter can take an input 1, 2, or 3 jolts lower than its rating and still produce its rated output joltage.
#
# In addition, your device has a built-in joltage adapter rated for 3 jolts higher than the highest-rated adapter in your bag. (If your adapter list were 3, 9, and 6, your device's built-in adapter would be rated for 12 jolts.)
#
# Treat the charging outlet near your seat as having an effective joltage rating of 0.
#
# Since you have some time to kill, you might as well test all of your adapters. Wouldn't want to get to your resort and realize you can't even charge your device!
#
# If you use every adapter in your bag at once, what is the distribution of joltage differences between the charging outlet, the adapters, and your device?
#
# For example, suppose that in your bag, you have adapters with the following joltage ratings:
#
# 16
# 10
# 15
# 5
# 1
# 11
# 7
# 19
# 6
# 12
# 4
# With these adapters, your device's built-in joltage adapter would be rated for 19 + 3 = 22 jolts, 3 higher than the highest-rated adapter.
#
# Because adapters can only connect to a source 1-3 jolts lower than its rating, in order to use every adapter, you'd need to choose them like this:
#
# The charging outlet has an effective rating of 0 jolts, so the only adapters that could connect to it directly would need to have a joltage rating of 1, 2, or 3 jolts. Of these, only one you have is an adapter rated 1 jolt (difference of 1).
# From your 1-jolt rated adapter, the only choice is your 4-jolt rated adapter (difference of 3).
# From the 4-jolt rated adapter, the adapters rated 5, 6, or 7 are valid choices. However, in order to not skip any adapters, you have to pick the adapter rated 5 jolts (difference of 1).
# Similarly, the next choices would need to be the adapter rated 6 and then the adapter rated 7 (with difference of 1 and 1).
# The only adapter that works with the 7-jolt rated adapter is the one rated 10 jolts (difference of 3).
# From 10, the choices are 11 or 12; choose 11 (difference of 1) and then 12 (difference of 1).
# After 12, only valid adapter has a rating of 15 (difference of 3), then 16 (difference of 1), then 19 (difference of 3).
# Finally, your device's built-in adapter is always 3 higher than the highest adapter, so its rating is 22 jolts (always a difference of 3).
# In this example, when using every adapter, there are 7 differences of 1 jolt and 5 differences of 3 jolts.
#
# Here is a larger example:
#
# 28
# 33
# 18
# 42
# 31
# 14
# 46
# 20
# 48
# 47
# 24
# 23
# 49
# 45
# 19
# 38
# 39
# 11
# 1
# 32
# 25
# 35
# 8
# 17
# 7
# 9
# 4
# 2
# 34
# 10
# 3
# In this larger example, in a chain that uses all of the adapters, there are 22 differences of 1 jolt and 10 differences of 3 jolts.
#
# Find a chain that uses all of your adapters to connect the charging outlet to your device's built-in adapter and count the joltage differences between the charging outlet, the adapters, and your device.
# What is the number of 1-jolt differences multiplied by the number of 3-jolt differences?
#
# To begin, get your puzzle input.
#

# --- Part Two ---
# To completely determine whether you have enough adapters, you'll need to figure out how many different ways they can be arranged. Every arrangement needs to connect the charging outlet to your device.
# The previous rules about when adapters can successfully connect still apply.

# The first example above (the one that starts with 16, 10, 15) supports the following arrangements:

# (0), 1, 4, 5, 6, 7, 10, 11, 12, 15, 16, 19, (22)
# (0`), 1, 4, 5, 6, 7, 10, 12, 15, 16, 19, (22)
# (0), 1, 4, 5, 7, 10, 11, 12, 15, 16, 19, (22)
# (0), 1, 4, 5, 7, 10, 12, 15, 16, 19, (22)
# (0), 1, 4, 6, 7, 10, 11, 12, 15, 16, 19, (22)
# (0), 1, 4, 6, 7, 10, 12, 15, 16, 19, (22)
# (0), 1, 4, 7, 10, 11, 12, 15, 16, 19, (22)
# (0), 1, 4, 7, 10, 12, 15, 16, 19, (22)
# (The charging outlet and your device's built-in adapter are shown in parentheses.) Given the adapters from the first example, the total number of arrangements that connect the charging outlet to your device is 8.

# The second example above (the one that starts with 28, 33, 18) has many arrangements. Here are a few:

# (0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
# 32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 48, 49, (52)

# (0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
# 32, 33, 34, 35, 38, 39, 42, 45, 46, 47, 49, (52)

# (0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
# 32, 33, 34, 35, 38, 39, 42, 45, 46, 48, 49, (52)

# (0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
# 32, 33, 34, 35, 38, 39, 42, 45, 46, 49, (52)

# (0), 1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 17, 18, 19, 20, 23, 24, 25, 28, 31,
# 32, 33, 34, 35, 38, 39, 42, 45, 47, 48, 49, (52)

# (0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
# 46, 48, 49, (52)

# (0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
# 46, 49, (52)

# (0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
# 47, 48, 49, (52)

# (0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
# 47, 49, (52)

# (0), 3, 4, 7, 10, 11, 14, 17, 20, 23, 25, 28, 31, 34, 35, 38, 39, 42, 45,
# 48, 49, (52)
# In total, this set of adapters can connect the charging outlet to your device in 19208 distinct arrangements.

# You glance back down at your bag and try to remember why you brought so many adapters; there must be more than a trillion valid ways to arrange them! Surely, there must be an efficient way to count the arrangements.

# What is the total number of distinct ways you can arrange the adapters to connect the charging outlet to your device?


from typing import Set

# first we need to get a list of the adapters
def load_adapters_from_file(filename: str) -> Set[int]:
    """
    Return a set of all the adapters in the input list
    """
    result = set()

    with open(filename, "r") as f:
        for this_line in f:
            this_line = this_line.strip()
            if this_line != "":
                this_int_val = int(this_line)
                if this_int_val in result:
                    raise ValueError(
                        f"Unexpected duplicate value in input: {this_int_val}"
                    )
                result.add(this_int_val)

    return result


def connect_max_adapters(adapters, start_jolt=0, max_joltage_difference=3):
    """
    Connect all the adapters to calculate the final joltage of your device
    as many adapters as possible must be connected
    each one can only connect to one that is 1-max_joltage_difference lower than it
    final value is max_joltage_difference more than the highest adapter we could plug in
    returns:
      a dict of the number of times each level of voltage skip was used :
        1 -> 27 times
        2 -> 14 times
        3 -> 11 times
      the final joltage for the adapter
    """
    jump_counts = dict()

    current_joltage = start_jolt
    ordered_adapters = sorted(adapters)
    next_adapter_idx = 0

    while next_adapter_idx < len(ordered_adapters):
        # ok, we know which one is next, is it possible ?
        next_adapter_joltage = ordered_adapters[next_adapter_idx]
        this_joltage_difference = next_adapter_joltage - current_joltage
        if this_joltage_difference > max_joltage_difference:
            raise RuntimeError(
                f"We can't make this work.. current={current_joltage}, next={next_adapter_joltage}, max_joltage_diff={max_joltage_difference}"
            )
        # ok, so add one to the jump counts
        if this_joltage_difference not in jump_counts:
            jump_counts[this_joltage_difference] = 0
        jump_counts[this_joltage_difference] += 1
        # and move onto the next one..
        current_joltage = next_adapter_joltage
        next_adapter_idx += 1

    # calc the final joltage
    final_joltage = current_joltage + max_joltage_difference
    if max_joltage_difference not in jump_counts:
        jump_counts[max_joltage_difference] = 0
    jump_counts[max_joltage_difference] += 1

    return jump_counts, final_joltage


def calculate_combinations_for(
    adapters, start, target, max_joltage_difference=3
) -> int:
    """
    return the number of ways that the adapters mentioned can be connected from start to end
    """
    # get the list in order
    adapters.add(start)
    adapters = sorted(adapters)
    # there's only one way to finish once you're at the final device
    ways_to_finish_from_here = {start: -1, target: 1}
    # work backwards through the list
    for this_adapter in reversed(adapters):
        print(f"considering adapter {this_adapter} against {ways_to_finish_from_here}")
        # for this adapter, it can connect to anything 1..max_joltage_difference above it..
        # the number of ways this adapter can be added in the end is the sum of each of the ways
        # that those reachable adapters can get to the final joltage
        ways_this_adapter_can_finish = 0
        for this_potential_next_adapter in range(
            this_adapter + 1, this_adapter + 1 + max_joltage_difference
        ):
            # if this adapter exists in the ways_to_finish from here list then we should include that count here
            if this_potential_next_adapter in ways_to_finish_from_here:
                ways_this_adapter_can_finish += ways_to_finish_from_here[
                    this_potential_next_adapter
                ]

            print(
                f"- {this_potential_next_adapter} can finish in {ways_this_adapter_can_finish} ways"
            )
            ways_to_finish_from_here[this_adapter] = ways_this_adapter_can_finish

    print(f"final ways to finish: {ways_to_finish_from_here}")

    return ways_to_finish_from_here[start]


# main
filename = "input.txt"
adapters = load_adapters_from_file(filename)
print(f"Adapters: {adapters}")

# connect the adapters up..
jolt_diffs, final_value = connect_max_adapters(adapters)


print(f"Jolt diffs: {jolt_diffs}")
print(f"Final joltage: {final_value}")
volt_1_diffs = jolt_diffs[1]
volt_3_diffs = jolt_diffs[3]
print(
    f"Answer: 1 volt diffs={volt_1_diffs}, 3 volt diffs={volt_3_diffs}, product: {volt_1_diffs * volt_3_diffs}"
)

# and now, calculate the number of adaptor combinations..
total_combinations = calculate_combinations_for(adapters, start=0, target=final_value)
print(f"Total ways to connect your adapters: {total_combinations}")
