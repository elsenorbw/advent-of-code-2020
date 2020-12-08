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


# yay, IntCode2 - son of IntCode
class TheMachine:
    def __init__(self):
        self.instructions = []
        self.reset()

    def reset(self):
        self.accumulator = 0
        self.instruction_pointer = 0
        self.halting_list = set()

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

    def step(self):
        """
        Execute the next step in the program code
        """
        # 1) Are we pointed at a vaild instruction ?
        if self.instruction_pointer < 0 or self.instruction_pointer >= len(
            self.instructions
        ):
            print(
                f"Trying to execute instruction {self.instruction_pointer}, however the code only has {len(self.instructions)} instructions"
            )
            raise RuntimeError(
                f"invalid instruction pointer location {self.instruction_pointer}"
            )

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
            print(
                f"Oh dear! we've run this instruction before, looping is detected on instruction {self.instruction_pointer}"
            )
            raise RuntimeError(
                f"Infinite looping detected at {self.instruction_pointer}"
            )
        else:
            self.halting_list.add(self.instruction_pointer)

        # 4) Right, now we can run the actual code
        print(f"{self.instruction_pointer} -> {instruction} {int_param}")
        instruction_function(self, int_param)

        # 5) and we need to update the instruction pointer
        self.instruction_pointer += 1


# main program
filename = "input.txt"
the_machine = TheMachine()
the_machine.print_state()
the_machine.load_program_from_file(filename)
the_machine.print_state()

try:
    while True:
        the_machine.step()
finally:
    the_machine.print_state()
