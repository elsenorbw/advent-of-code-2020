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


# Your puzzle answer was 11884151942312.
#
# The first half of this puzzle is complete! It provides one gold star: *
#
# --- Part Two ---
# For some reason, the sea port's computer system still can't communicate with your ferry's docking program. It must be using version 2 of the decoder chip!
#
# A version 2 decoder chip doesn't modify the values being written at all. Instead, it acts as a memory address decoder. Immediately before a value is written to memory, each bit in the bitmask modifies the corresponding
# bit of the destination memory address in the following way:
#
# If the bitmask bit is 0, the corresponding memory address bit is unchanged.
# If the bitmask bit is 1, the corresponding memory address bit is overwritten with 1.
# If the bitmask bit is X, the corresponding memory address bit is floating.
# A floating bit is not connected to anything and instead fluctuates unpredictably. In practice, this means the floating bits will take on all possible values, potentially causing many memory addresses to be written all at once!
#
# For example, consider the following program:
#
# mask = 000000000000000000000000000000X1001X
# mem[42] = 100
# mask = 00000000000000000000000000000000X0XX
# mem[26] = 1
# When this program goes to write to memory address 42, it first applies the bitmask:
#
# address: 000000000000000000000000000000101010  (decimal 42)
# mask:    000000000000000000000000000000X1001X
# result:  000000000000000000000000000000X1101X
# After applying the mask, four bits are overwritten, three of which are different, and two of which are floating. Floating bits take on every possible combination of values; with two floating bits, four actual memory addresses are written:
#
# 000000000000000000000000000000011010  (decimal 26)
# 000000000000000000000000000000011011  (decimal 27)
# 000000000000000000000000000000111010  (decimal 58)
# 000000000000000000000000000000111011  (decimal 59)
# Next, the program is about to write to memory address 26 with a different bitmask:
#
# address: 000000000000000000000000000000011010  (decimal 26)
# mask:    00000000000000000000000000000000X0XX
# result:  00000000000000000000000000000001X0XX
# This results in an address with three floating bits, causing writes to eight memory addresses:
#
# 000000000000000000000000000000010000  (decimal 16)
# 000000000000000000000000000000010001  (decimal 17)
# 000000000000000000000000000000010010  (decimal 18)
# 000000000000000000000000000000010011  (decimal 19)
# 000000000000000000000000000000011000  (decimal 24)
# 000000000000000000000000000000011001  (decimal 25)
# 000000000000000000000000000000011010  (decimal 26)
# 000000000000000000000000000000011011  (decimal 27)
# The entire 36-bit address space still begins initialized to the value 0 at every address, and you still need the sum of all values left in memory at the end of the program. In this example, the sum is 208.
#
# Execute the initialization program using an emulator for a version 2 decoder chip. What is the sum of all values left in memory after it completes?


class BitMask:
    def __init__(self, mask_string):
        or_mask = 0
        mask_string = mask_string.strip()
        # want to store this for later printing
        self.original_mask = mask_string
        # ensure they are 36 bits long, don't want to truncate anything
        padded_mask_string = (("X" * 36) + mask_string)[-36:]

        # first, we can sort out the or-mask
        for this_char in padded_mask_string:
            # handle this character..
            # 1) everything we've seen so far is one bit more important
            or_mask <<= 1
            # 2) now set the bottom bit appropriately
            # if we have a 1, then the or_mask must be set here so that this is always a 1
            if "1" == this_char:
                or_mask += 1
        self.or_mask = or_mask

        # now, we need to get a list of the locations where bit-flippery must happen
        self.bit_flip_locations = []
        for idx, this_char in enumerate(reversed(padded_mask_string), start=1):
            if "X" == this_char:
                self.bit_flip_locations.append(idx)
        # ok, we're done..

    def generate_addresses(self, i: int, verbose=False) -> int:
        """
        Generate all the target addresses for a given input address
        """
        result = []
        # 1) flip all the bits we know need to be flipped
        static_masked_value = i | self.or_mask
        # 2) Generate all the possible resulting addresses from the flippy bits
        if 0 == len(self.bit_flip_locations):
            result.append(static_masked_value)
        else:
            # we need to loop and generate all the combinations..
            # ok, so we know that we have X bits which need to flip..
            # giving us a certain number of bits to set each time..
            # 1 bit would need us to loop a range up to 2 (0, 1)
            # 2 bits would need us to loop a range up to 4 (0, 1, 2, 3) or (00, 01, 10, 11)
            # 3 bits would need a loop to 8 (0..7) or (000..111)
            loop_range_limit = 1 << len(self.bit_flip_locations)
            for x in range(loop_range_limit):
                # ok, we have the bits set in x, they need to be flipped into the value at the appropriate locations
                # easy way would be a loop to just set those bits
                # we could AND out all the spots where we would need to (which we could pre-calculate for speed)
                # and then we could OR in whichever bits are lit
                # sounds like a plan..
                and_mask = (1 << 36) - 1
                for flip_idx in self.bit_flip_locations:
                    tgt_bit = 1 << (flip_idx - 1)
                    and_mask = and_mask ^ tgt_bit

                or_mask = 0
                for src_idx, dst_idx in enumerate(self.bit_flip_locations, start=0):
                    # get the src index bit separately
                    src_bit = (x >> src_idx) & 1
                    # and put it into the right position for adding to the or mask
                    tgt_bit = src_bit << (dst_idx - 1)
                    # and add it to the or mask
                    or_mask = or_mask | tgt_bit

                # and now calculate this address:
                this_address_stage1 = static_masked_value & and_mask
                this_address_stage2 = this_address_stage1 | or_mask
                if verbose:
                    print(f"   original was: {self.original_mask}")
                    print(f" or_mask is now: {or_mask:>036b}")
                    print(f"and_mask is now: {and_mask:>036b}")
                    print(f"     x value is: {x:>036b}")
                    print(f"initial_address: {static_masked_value:>036b}")
                    print(f"  anded address: {this_address_stage1:>036b}")
                    print(f"  final address: {this_address_stage2:>036b}")

                result.append(this_address_stage2)

        # and we're done...,
        return result

    def __str__(self):
        """
        produce a nicer representation for this..
        """
        result = f"Mask:\n"
        result += f" orig({self.original_mask})\n"
        result += f"   or({self.or_mask:>036b})"
        result += f" flipping bits at: {self.bit_flip_locations}"
        return result


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
        all_target_addresses = self.mask.generate_addresses(address)
        for this_address in all_target_addresses:
            self.memory[this_address] = value

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