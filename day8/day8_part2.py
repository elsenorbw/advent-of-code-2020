# --- Day 8: Handheld Halting ---
# Your flight to the major airline hub reaches cruising altitude without incident. While you consider checking the in-flight menu for one of those drinks that come with a little umbrella, you are interrupted by the kid sitting next to you.
#
# Their handheld game console won't turn on! They ask if you can take a look.
#
# You narrow the problem down to a strange infinite loop in the boot code (your puzzle input) of the device. You should be able to fix it, but first you need to be able to run the code in isolation.
#
# The boot code is represented as a text file with one instruction per line of text. Each instruction consists of an operation (acc, jmp, or nop) and an argument (a signed number like +4 or -20).
#
# acc increases or decreases a single global value called the accumulator by the value given in the argument. For example, acc +7 would increase the accumulator by 7. The accumulator starts at 0.
# After an acc instruction, the instruction immediately below it is executed next.
# jmp jumps to a new instruction relative to itself. The next instruction to execute is found using the argument as an offset from the jmp instruction; for example, jmp +2 would skip the next instruction,
# jmp +1 would continue to the instruction immediately below it, and jmp -20 would cause the instruction 20 lines above to be executed next.
# nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next.
# For example, consider the following program:
#
# nop +0
# acc +1
# jmp +4
# acc +3
# jmp -3
# acc -99
# acc +1
# jmp -4
# acc +6
# These instructions are visited in this order:
#
# nop +0  | 1
# acc +1  | 2, 8(!)
# jmp +4  | 3
# acc +3  | 6
# jmp -3  | 7
# acc -99 |
# acc +1  | 4
# jmp -4  | 5
# acc +6  |
# First, the nop +0 does nothing. Then, the accumulator is increased from 0 to 1 (acc +1) and jmp +4 sets the next instruction to the other acc +1 near the bottom. After it increases the accumulator from 1 to 2,
# jmp -4 executes, setting the next instruction to the only acc +3. It sets the accumulator to 5, and jmp -3 causes the program to continue back at the first acc +1.
#
# This is an infinite loop: with this sequence of jumps, the program will run forever. The moment the program tries to run any instruction a second time, you know it will never terminate.
#
# Immediately before the program would run an instruction a second time, the value in the accumulator is 5.
#
# Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the accumulator?

# Your puzzle answer was 1528.

# The first half of this puzzle is complete! It provides one gold star: *

# --- Part Two ---
# After some careful analysis, you believe that exactly one instruction is corrupted.

# Somewhere in the program, either a jmp is supposed to be a nop, or a nop is supposed to be a jmp. (No acc instructions were harmed in the corruption of this boot code.)

# The program is supposed to terminate by attempting to execute an instruction immediately after the last instruction in the file. By changing exactly one jmp or nop, you can repair the boot code and make it terminate correctly.

# For example, consider the same program from above:

# nop +0
# acc +1
# jmp +4
# acc +3
# jmp -3
# acc -99
# acc +1
# jmp -4
# acc +6
# If you change the first instruction from nop +0 to jmp +0, it would create a single-instruction infinite loop, never leaving that instruction. If you change almost any of the jmp instructions, the program will still eventually find another jmp instruction and loop forever.

# However, if you change the second-to-last instruction (from jmp -4 to nop -4), the program terminates! The instructions are visited in this order:

# nop +0  | 1
# acc +1  | 2
# jmp +4  | 3
# acc +3  |
# jmp -3  |
# acc -99 |
# acc +1  | 4
# nop -4  | 5
# acc +6  | 6
# After the last instruction (acc +6), the program terminates by attempting to run the instruction below the last instruction in the file. With this change, after the program terminates, the accumulator contains the value 8 (acc +1, acc +1, acc +6).

# Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the value of the accumulator after the program terminates?


# ok, so there will be a finite number of instruction locations that would be acceptable at the end of the program,
# landing on any of those would allow the program to terminate normally.
# the approach should presumably be to figure out which jump commands would land us on any of those locations, although it might not be that simple
# brute-force would be easy, simply flip each of the instructions mentioned in the code and run the program, not very elegant though..
# might be a good starter for 10 though..


# yay, IntCode2 - son of IntCode
class TheMachine:
    def __init__(self):
        self.instructions = []
        self.reset()

    def reset(self):
        self.accumulator = 0
        self.instruction_pointer = 0
        self.halting_list = set()

    def copy(self):
        duplicate = TheMachine()
        duplicate.instructions = self.instructions.copy()
        duplicate.accumulator = self.accumulator
        duplicate.instruction_pointer = self.instruction_pointer
        duplicate.halting_list = self.halting_list.copy()
        return duplicate

    def get_code_length(self):
        return len(self.instructions)

    def peek(self, location=None):
        """
        return the operation, int_param pair at a given location or the current instruction
        """
        if location is None:
            location = self.instruction_pointer
        if location < 0 or location >= len(self.instructions):
            raise ValueError(
                f"unable to peek at {location}, there are only {len(self.instructions)} instructions in the codebase"
            )
        return self.instructions[location]

    def poke(self, location, operation, int_param):
        """
        Set a particular instruction (only supports inside the current address space for now)
        """
        if location < 0 or location >= len(self.instructions):
            raise ValueError(
                f"unable to poke at {location}, there are only {len(self.instructions)} instructions in the codebase"
            )
        self.instructions[location] = (operation, int_param)

    def operation_nop(self, intval):
        """
        the nop operation, do nothing
        """
        return True

    def operation_acc(self, intval):
        """
        The accumulator function, adjust the accumulator value
        """
        self.accumulator += intval
        return True

    def operation_jmp(self, intval):
        """
        The jmp instruction, adjust the instruction pointer by the value specified
        N.B. The main engine will +1 the result after this so we need to -1 in here
        """
        self.instruction_pointer += intval
        self.instruction_pointer -= 1
        return True

    operations = {"nop": operation_nop, "acc": operation_acc, "jmp": operation_jmp}

    def load_program_from_file(self, filename: str):
        """
        Load the instructions from a file
        format for instructions is:
        abc <intval>
        """
        with open(filename, "r") as f:
            for this_line in f:
                this_line = this_line.strip()
                if this_line != "":
                    # actual value to deal with
                    fields = this_line.split()
                    if 2 != len(fields):
                        print(f"bad code in the input: {this_line}")
                        print(f"bad code gave us {fields}")
                        raise ValueError(
                            f"This doesn't look like valid program code because we got {len(fields)} fields: {this_line}"
                        )
                    else:
                        instruction_code = fields[0]
                        int_argument = int(fields[1])
                        self.instructions.append((instruction_code, int_argument))

    def print_state(self):
        """
        Dump the entire state of the machine to stdout
        """
        print(f"Machine State")
        print(f"-------------")
        print(f"Accumulator: {self.accumulator}")
        print(f"Instruction Pointer: {self.instruction_pointer}")
        print(f"halting_list: {self.halting_list}")
        print(f"program code: {len(self.instructions)} instructions")
        print(f"")

    def run(self, verbose=False):
        """
        Run the progream from the current location until we either hit an exception or a natural finish
        """
        result = False
        result_description = "Unknown"
        try:
            while self.step(verbose=verbose):
                pass
            # if we get to here then it worked..
            result = True
            result_description = "Natural program completion"
        except Exception as e:
            if verbose:
                print(f"well that failed: {e}")
            result = False
            result_description = str(e)
        return result, result_description

    def step(self, verbose=False):
        """
        Execute the next step in the program code
        """
        # 1) Are we pointed at a vaild instruction ?
        if self.instruction_pointer < 0 or self.instruction_pointer > len(
            self.instructions
        ):
            if verbose:
                print(
                    f"Trying to execute instruction {self.instruction_pointer}, however the code only has {len(self.instructions)} instructions"
                )
            raise RuntimeError(
                f"invalid instruction pointer location {self.instruction_pointer}"
            )

        # 1b) If we have run off the end of the program then we're fine
        if self.instruction_pointer == len(self.instructions):
            if verbose:
                print(f"Program finished naturally")
            return False

        # 2) Does the instruction we've found match some code we understand ?
        instruction, int_param = self.instructions[self.instruction_pointer]
        if instruction not in self.operations:
            print(
                f"Instruction not implemented: {instruction} at {self.instruction_pointer}"
            )
            raise RuntimeError(f"Instruction not implemented: {instruction}")
        instruction_function = self.operations[instruction]

        # 3) Ok, great, but have we been here before ? If so this is a halting issue
        if self.instruction_pointer in self.halting_list:
            if verbose:
                print(
                    f"Oh dear! we've run this instruction before, looping is detected on instruction {self.instruction_pointer}"
                )
            raise RuntimeError(
                f"Infinite looping detected at {self.instruction_pointer}"
            )
        else:
            self.halting_list.add(self.instruction_pointer)

        # 4) Right, now we can run the actual code
        if verbose:
            print(f"{self.instruction_pointer} -> {instruction} {int_param}")
        instruction_function(self, int_param)

        # 5) and we need to update the instruction pointer
        self.instruction_pointer += 1

        # and that worked..
        return True


# main program
filename = "input.txt"
the_machine = TheMachine()
the_machine.load_program_from_file(filename)

for this_address in range(the_machine.get_code_length()):
    operation, int_param = the_machine.peek(this_address)
    # print(f"{this_address} -> {operation}, {int_param}")
    if operation in ("nop", "jmp"):
        if operation == "nop":
            operation = "jmp"
        else:
            operation = "nop"
        new_machine = the_machine.copy()
        new_machine.poke(this_address, operation, int_param)
        result, result_desc = new_machine.run(verbose=False)
        print(f"flipped {this_address} -> {result_desc}")
        if result:
            new_machine.print_state()
            break
