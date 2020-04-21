"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

# Unused so far
ADD = 0b10100000
DIV = 0b10100011
SUB = 0b10100001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Step 1
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0

    def load(self, filename):
        """Load a program into memory."""

        # Counter
        address = 0

        # Open ls8 file
        with open(filename) as f:
            # Read each line
            for line in f:
                # Split on # to remove comments
                line = line.split('#')
                # Remove empty spaces
                line = line[0].strip()
                if line == '':
                    continue
                # Convert to int (base 2 binary) and save to ram at address
                self.ram[address] = int(line, 2)
                # Incriment address counter
                address += 1
        '''
        Old hardcoded program:
        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
            '''


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.register[reg_a] += self.register[reg_b]
        elif op == SUB:
            self.register[reg_a] -= self.register[reg_b]
        elif op == MUL:
            self.register[reg_a] *= self.register[reg_b]
        elif op == DIV:
            self.register[reg_a] /= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, mar):
        '''
        Takes address (mar) in ram and returns the value (mdr) stored there
        '''
        mdr = self.ram[mar]
        return mdr
    
    def ram_write(self, mar, mdr):
        '''
        Stores 'value' (MDR) at given 'address' (MAR) in ram
        '''
        self.ram[mar] = mdr

    def reg_read(self, address):
        '''
        Takes address in register and returns value stored there 
        '''
        return self.register[address]

    def reg_write(self, address, value):
        '''
        Stores value at given address in register
        '''
        self.register[address] = value

    def run(self):
        '''
        Run the CPU
        '''
        
        # Used to exit run()
        running = True

        while running:
            # Read memory address stored in PC and store result in IR
            ir = self.ram_read(self.pc)

            # LDI instruction
            if ir == LDI:
                # Read values at PC+1 and PC+2 into operand_a and operand_b respectively
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                # Set register at address 'operand_a' to value 'operand_b'
                self.reg_write(operand_a, operand_b)
                self.pc += 3
            # PRN instruction
            elif ir == PRN:
                # Read value at PC+1 into operand_a
                operand_a = self.ram_read(self.pc + 1)
                # Print value
                print(self.reg_read(operand_a))
                self.pc += 2
            elif ir == HLT:
                running = False
            # MUL instruction
            # TODO: Impliment all ALU functions here (use list of instructions? [ADD, MUL...])
            elif ir == MUL:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.alu(ir, operand_a, operand_b)
                self.pc += 3
            else:
                print('Unknown Command!')
                running = False
# TODO: Maybe make dict of all instructions to clean up all the if statements

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
