import sys

# Write a program in Python that runs programs

# Parse the command line
program_filename = sys.argv[1]
# print(program_filename)
# sys.exit()

PRINT_NICK = 1
HALT = 2
SAVE_REG = 3 # Store a value in a register (in the LS8 called LDI)
PRINT_REG = 4 # Corresponds to PRN in the LS8
PUSH = 5
POP = 6
CALL = 7
RET = 8

# memory = [
#     PRINT_NICK,
#     SAVE_REG,  # SAVE R0,37 (store 37 in R0) THIS IS THE OPCODE
#     0, # Represent Register0 (R0) # Operand ('argument')
#     37, # Represent 37 # Operand ('argument')
#     PRINT_NICK,

#     PRINT_REG, # PRINT_REG R0
#     0, # R0 (Tells PRINT_REG which register to print)
#        # NOTE: Will still need to get value from register number
#     HALT
# ]

memory = [0] * 256

register = [0] * 8 # Like variables R0-R7

# R7 is the SP
SP = 7
register[SP] = 0xF4

# Load program into memory
address = 0

with open(program_filename) as f:
    for line in f:
        line = line.split('#')
        line = line[0].strip()
        if line == '':
            continue
        memory[address] = int(line)
        address += 1
        
# sys.exit()


pc = 0 # Program Counter, the address of the current instruction
running = True

while running:
    inst = memory[pc]

    if inst == PRINT_NICK:
        print('Nick!')
        pc += 1

    elif inst == SAVE_REG:
        reg_num = memory[pc + 1]
        value = memory[pc + 2]
        register[reg_num] = value
        pc += 3

    elif inst == PRINT_REG:
        reg_num = memory[pc + 1]
        value = register[reg_num]
        print(value)
        pc += 2

    elif inst == PUSH:
        # decrement the stack pointer
        register[SP] -= 1

        # copy value from the register into memory
        reg_num = memory[pc + 1]
        value = register[reg_num]

        address = register[SP]
        memory[address] = value

        pc += 1

    elif inst == POP:
        # Copy value from register to memory
        reg_num = memory[pc + 1]

        # Address of item on the top of the stack
        address = register[SP]
        # This is the value we popped
        value = memory[address]

        # Store the value in the register
        register[reg_num] = value

        pc += 2

        # Incriment the stack pointer
        register[SP] += 1
    
    elif inst == CALL:
        # Compute return address
        return_adr = pc + 2

        # Push on the stack
        register[SP] -= 1
        memory[register[SP]] = return_addr

        # Set the PC to the value in the given register
        reg_num = memory[PC + 1]
        dest_addr = register[reg_num]

        pc = dest_addr
    
    elif inst == RET:
        # Pop return address from the top of stack
        return_adr = memory[register[SP]]

    elif inst == HALT:
        running = False

    else:
        print('Unknown Instruction')
        running = False
