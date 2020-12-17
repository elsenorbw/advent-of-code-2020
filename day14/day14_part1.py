# --- Day 14: Docking Data ---
# As your ferry approaches the sea port, the captain asks for your help again. The computer system that runs this port isn't compatible with the docking program on the ferry, so the docking parameters aren't being correctly initialized in the docking program's memory.
#
# After a brief inspection, you discover that the sea port's computer system uses a strange bitmask system in its initialization program. Although you don't have the correct decoder chip handy, you can emulate it in software!
#
# The initialization program (your puzzle input) can either update the bitmask or write a value to memory. Values and memory addresses are both 36-bit unsigned integers. For example, ignoring bitmasks for a moment, a line like mem[8] = 11 would write the value 11 to memory address 8.
#
# The bitmask is always given as a string of 36 bits, written with the most significant bit (representing 2^35) on the left and the least significant bit (2^0, that is, the 1s bit) on the right.
# The current bitmask is applied to values immediately before they are written to memory: a 0 or 1 overwrites the corresponding bit in the value, while an X leaves the bit in the value unchanged.
#
# For example, consider the following program:
#
# mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# mem[8] = 11
# mem[7] = 101
# mem[8] = 0
# This program starts by specifying a bitmask (mask = ....). The mask it specifies will overwrite two bits in every written value: the 2s bit is overwritten with 0, and the 64s bit is overwritten with 1.
#
# The program then attempts to write the value 11 to memory address 8. By expanding everything out to individual bits, the mask is applied as follows:
#
# value:  000000000000000000000000000000001011  (decimal 11)
# mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# result: 000000000000000000000000000001001001  (decimal 73)
# So, because of the mask, the value 73 is written to memory address 8 instead. Then, the program tries to write 101 to address 7:
#
# value:  000000000000000000000000000001100101  (decimal 101)
# mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# result: 000000000000000000000000000001100101  (decimal 101)
# This time, the mask has no effect, as the bits it overwrote were already the values the mask tried to set. Finally, the program tries to write 0 to address 8:
#
# value:  000000000000000000000000000000000000  (decimal 0)
# mask:   XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
# result: 000000000000000000000000000001000000  (decimal 64)
# 64 is written to address 8 instead, overwriting the value that was there previously.
#
# To initialize your ferry's docking program, you need the sum of all values left in memory after the initialization program completes. (The entire 36-bit address space begins initialized to the value 0 at every address.)
# In the above example, only two values in memory are not zero - 101 (at address 7) and 64 (at address 8) - producing a sum of 165.
#
# Execute the initialization program. What is the sum of all values left in memory after it completes?


class BitMask:
    def __init__(self, mask_string):
        and_mask = 0
        or_mask = 0
        mask_string = mask_string.strip()
        # want to store this for later printing
        self.original_mask = mask_string
        # ensure they are 36 bits long, don't want to truncate anything
        padded_mask_string = (("X" * 36) + mask_string)[-36:]

        for this_char in padded_mask_string:
            # handle this character..
            # 1) everything we've seen so far is one bit more important
            and_mask <<= 1
            or_mask <<= 1
            # 2) now set the bottom bit appropriately
            # if we have a 1, then the or_mask must be set here so that this is always a 1
            if "1" == this_char:
                or_mask += 1
            # if we have a 0 here the and mask must not be set here, otherwise it must
            if "0" != this_char:
                and_mask += 1
        self.and_mask = and_mask
        self.or_mask = or_mask

    def apply(self, i: int) -> int:
        """
        Apply the mask to a given integer
        """
        result = (i | self.or_mask) & self.and_mask
        return result

    def __str__(self):
        """
        produce a nicer representation for this..
        """
        result = f"Mask:\n"
        result += f" orig({self.original_mask})\n"
        result += f"  and({self.and_mask:>036b})\n"
        result += f"   or({self.or_mask:>036b})"
        return result


# some quick testing for the BitMask in case I am an idiot
m = BitMask("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X")
print(str(m))
for test_value, expected_value in [(11, 73), (101, 101), (0, 64)]:
    result = m.apply(test_value)
    print(f"Masked {test_value} and got {result}, expected {expected_value}")

# appears to work for my extensive testing..
# soo....


def get_string_between(s, start, end):
    """
    chop up the string appropriately or throw
    """
    start_idx = s.find(start)
    end_idx = s.find(end, start_idx + 1)
    if -1 == start_idx or -1 == end_idx:
        raise ValueError(
            f"Unable to get the string between {start} and {end} with an input of {s}"
        )
    result = s[start_idx + len(start) : end_idx]
    return result


class DockingSystem:
    def __init__(self):
        self.mask = BitMask("")
        self.memory = dict()

    def memory_sum(self):
        """
        Return the sum of all the values currently held in memory
        """
        result = sum(self.memory.values())
        return result

    def print(self):
        print(f"Current Mask: {str(self.mask)}")
        print(f"Memory:")
        for this_memory_location in sorted(self.memory.keys()):
            print(f"{this_memory_location:>5} -> {self.memory[this_memory_location]}")
        print(f"Sum of memory: {self.memory_sum()}")

    def poke(self, address, value):
        """
        apply current mask to value and then store it at the specified address
        """
        new_value = self.mask.apply(value)
        self.memory[address] = new_value

    def set_mask(self, new_mask):
        """
        update the mask string to be the probvided value
        """
        self.mask = BitMask(new_mask)

    def process_one_instruction_line(self, instruction):
        """
        Handle an instruction which will be one of:
            mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
            mem[8] = 11
        so splitting on =
        value is always value, although for mem it needs inting
        """
        parts = instruction.split("=")
        if 2 != len(parts):
            raise ValueError(f"Cannot split this instruction correctly: {instruction}")
        target = parts[0].strip()
        value = parts[1].strip()

        if "mask" == target:
            self.set_mask(value)
        else:
            int_value = int(value)
            # find the location..
            # this is a slightly dirty hack..
            addr_str = get_string_between(target, "[", "]")
            int_addr = int(addr_str)
            self.poke(int_addr, int_value)

    def process_instruction_file(self, filename: str):
        """
        read each line of the instruction file and apply it to the current state
        """
        with open(filename, "r") as f:
            for this_line in f:
                this_line = this_line.strip()
                if "" != this_line:
                    self.process_one_instruction_line(this_line)


# main
filename = "input.txt"
docking_system = DockingSystem()
docking_system.process_instruction_file(filename)
docking_system.print()