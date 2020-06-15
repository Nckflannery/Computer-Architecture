"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
POP = 0b01000110
PUSH = 0b01000101
# ALU ops
MUL = 0b10100010
ADD = 0b10100000
DIV = 0b10100011
SUB = 0b10100001
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
        self.register[SP] = 0xF4
        self.branchtable = {
            LDI : self.ldi,
            PRN : self.prn,
            HLT : self.hlt,
            POP : self.pop,
            PUSH: self.push,
            MUL : self.alu,
            ADD : self.alu,
            DIV : self.alu,
            SUB : self.alu
        }

    def ldi(self, op_a, op_b):
        self.register[op_a] = op_b 
    
    # Only one operand but was cleaner to just pass them as unused parameters here
    def prn(self, op_a, op_b=None):
        print(self.register[op_a])
    
    # No operands but again was cleaner to pass as unused paramters here
    def hlt(self, op_a, op_b=None):
        sys.exit()
    
    def pop(self, op_a, op_b=None):
        # Get value from ram at SP in register
        value = self.ram_read(self.register[SP])
        # Set register at address given to value
        self.register[op_a] = value
        # Increment SP
        self.register[SP] += 1
        return value
    
    def push(self, op_a, op_b=None):
        # Decrement SP
        self.register[SP] -= 1
        # Write value given to ram at SP address
        self.ram_write(self.register[SP], self.register[op_a])
        
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

    def run(self):
        '''
        Run the CPU
        '''
        while True:
            # Get opcodes and operands
            ir = self.ram[self.pc]
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            # To update self.pc counter
            run_counter = (ir >> 6) + 1
            # To handle alu operations
            # NOTE: Less code but adds another if statement, may be quicker to implement
                  # individual helper functions that call ALU with specified operations
            alu_op = bool(((ir >> 5) & 0b1))
    
            if ir in self.branchtable:
                if alu_op:
                    self.branchtable[ir](ir, op_a, op_b)
                else:
                    self.branchtable[ir](op_a, op_b)
            else:
                print('Unsupported operation')
            self.pc += run_counter
    

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
