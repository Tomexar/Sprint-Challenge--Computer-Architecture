"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.live = True
        self.SP = 7
        self.fl = [0] * 4 


    def read(self, address):
        return self.ram[address]

    def write(self,address,value):
        MDR = value
        self.ram[address] = value


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        with open(sys.argv[1]) as f:
            for line in f:
                if line[0] is not '#' and line is not '\n':
                    self.ram[address] = int(line[:8], 2)
                    address += 1
            f.closed

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        #     0b10100010 # MUL R0,R1
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op =="CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl[1] = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl[2] = 1
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl[3] = 1
            print(f'flag = {self.fl}')
        else:
            raise Exception("Unsupported ALU operation")

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

    def push(self, a):
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.reg[a]

    def pop(self, a):
        self.reg[a] = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1

    def run(self):
        """Run the CPU."""

        print(self.ram[self.pc])
        

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        CMP = 0b10100111
        JEQ = 0b01010101
        JNE = 0b01010110
        JMP = 0b01010100

        10100111

        while self.live:
            operand_a = self.read(self.pc + 1)
            operand_b = self.read(self.pc + 2)
            
            if self.ram[self.pc] is LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif self.ram[self.pc] is PRN:
                print(f"{self.reg[operand_a]}")
                self.pc += 2
        
            elif self.ram[self.pc] is HLT:
                self.live is False
                break

            elif self.ram[self.pc] is MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            
            elif self.ram[self.pc] is PUSH:
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = self.reg[operand_a]
                self.pc += 2

            elif self.ram[self.pc] is POP:
                self.reg[operand_a] = self.ram[self.reg[self.SP]]
                self.reg[self.SP] += 1
                self.pc += 2

            elif self.ram[self.pc] is CALL:
                self.reg[4] = self.pc + 2
                self.push(4)
                self.pc = self.reg[operand_a]

            elif self.ram[self.pc] is RET:
                self.pop(0x04)
                self.pc = self.reg[0x04]

            elif self.ram[self.pc] is CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3 

            elif self.ram[self.pc] is JMP:
                self.pc = self.reg[operand_a]


            elif self.ram[self.pc] is JEQ:
                if self.fl[3] is 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            
            elif self.ram[self.pc] is JNE:
                if self.fl[3] is 0:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            
            else:
                self.live = False
                print(f"{self.ram[self.pc]} wrong command")
                break