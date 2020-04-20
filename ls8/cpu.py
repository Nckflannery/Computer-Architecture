"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Step 1
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

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


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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

            # LDI command
            if ir == LDI:
                # Read values at PC+1 and PC+2 into operand_a and operand_b respectively
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                # Set register at address 'operand_a' to value 'operand_b'
                self.reg_write(operand_a, operand_b)
                self.pc += 3
            # PRN command
            elif ir == PRN:
                # Read value at PC+1 into operand_a
                operand_a = self.ram_read(self.pc + 1)
                # Print value
                print(self.reg_read(operand_a))
                self.pc += 2
            elif ir == HLT:
                running = False
                self.pc += 1
            else:
                print('Unknown Command!')
                running = False


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