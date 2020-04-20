# Write a program in Python that runs programs

PRINT_NICK = 1
HALT = 2
SAVE_REG = 3 # Store a value in a register (in the LS8 called LDI)
PRINT_REG = 4 # Corresponds to PRN in the LS8

memory = [
    PRINT_NICK,
    SAVE_REG,  # SAVE R0,37 (store 37 in R0) THIS IS THE OPCODE
    0, # Represent Register0 (R0) # Operand ('argument')
    37, # Represent 37 # Operand ('argument')
    PRINT_NICK,

    PRINT_REG, # PRINT_REG R0
    0, # R0 (Tells PRINT_REG which register to print)
       # NOTE: Will still need to get value from register number
    HALT
]

register = [0] * 8 # Like variables R0-R7

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

    elif inst == HALT:
        break

    else:
        print('Unknown Instruction')
        running = False
