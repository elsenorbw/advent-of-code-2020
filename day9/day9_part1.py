# --- Day 9: Encoding Error ---
# With your neighbor happily enjoying their video game, you turn your attention to an open data port on the little screen in the seat in front of you.
#
# Though the port is non-standard, you manage to connect it to your computer through the clever use of several paperclips. Upon connection, the port outputs a series of numbers (your puzzle input).
#
# The data appears to be encrypted with the eXchange-Masking Addition System (XMAS) which, conveniently for you, is an old cypher with an important weakness.
#
# XMAS starts by transmitting a preamble of 25 numbers. After that, each number you receive should be the sum of any two of the 25 immediately previous numbers. The two numbers will have different values, and there might be more than one such pair.
#
# For example, suppose your preamble consists of the numbers 1 through 25 in a random order. To be valid, the next number must be the sum of two of those numbers:
#
# 26 would be a valid next number, as it could be 1 plus 25 (or many other pairs, like 2 and 24).
# 49 would be a valid next number, as it is the sum of 24 and 25.
# 100 would not be valid; no two of the previous 25 numbers sum to 100.
# 50 would also not be valid; although 25 appears in the previous 25 numbers, the two numbers in the pair must be different.
# Suppose the 26th number is 45, and the first number (no longer an option, as it is more than 25 numbers ago) was 20. Now, for the next number to be valid, there needs to be some pair of numbers among 1-19, 21-25, or 45 that add up to it:
#
# 26 would still be a valid next number, as 1 and 25 are still within the previous 25 numbers.
# 65 would not be valid, as no two of the available numbers sum to it.
# 64 and 66 would both be valid, as they are the result of 19+45 and 21+45 respectively.
# Here is a larger example which only considers the previous 5 numbers (and has a preamble of length 5):
#
# 35
# 20
# 15
# 25
# 47
# 40
# 62
# 55
# 65
# 95
# 102
# 117
# 150
# 182
# 127
# 219
# 299
# 277
# 309
# 576
# In this example, after the 5-number preamble, almost every number is the sum of two of the previous 5 numbers; the only number that does not follow this rule is 127.
#
# The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble) which is not the sum of two of the 25 numbers before it. What is the first number that does not have this property?
#
#


# ok, we need to maintain state, so going to create an xmas machine to do that..


class XMASDecoder:
    def __init__(self, preamble_size):
        self.preamble = preamble_size
        self.state = []

    def add_one_number(self, the_number: int):
        """
        add this new value onto the end of the list, storing at most preamble entries
        """
        self.state.append(the_number)
        self.state = self.state[-self.preamble :]

    def show_state(self):
        """
        print the current state
        """
        print(f"holding max of {self.preamble}, current state is: {self.state}")

    def acceptable_next_number(self, the_number):
        """
        would this number be acceptable as next in the sequence ?
        - if there are fewer than <preamble> numbers then yes
        - if we have a full complement of <preamble> numbers then:
          - yes, if this number is the sum of any pair of the previous numbers
          - no otherwise
        """
        result = False

        if len(self.state) < self.preamble:
            result = True
        else:
            # lazy, non-caching implementation for now
            for idx, x in enumerate(self.state):
                y = the_number - x
                if y in self.state[idx + 1 :]:
                    # ok, we have a pair that make a product
                    result = True
                    break

        return result


# main
# filename, preamble_size = "sample.txt", 5
filename, preamble_size = "input.txt", 25


decoder = XMASDecoder(preamble_size)
with open(filename, "r") as f:
    for this_line in f:
        this_line = this_line.strip()
        if "" != this_line:
            this_int_val = int(this_line)
            # can we add this one ?
            if decoder.acceptable_next_number(this_int_val):
                decoder.add_one_number(this_int_val)
            else:
                print(f"Found an unacceptable next value: {this_int_val}")
                break
