class CodeWriter:

    def __init__(self, output_file):
        '''
        Opens the output file and gets ready  to write into it.
        '''
        self.output_file = open(output_file, 'w')


    def writeBinaryOperation(self, op):
        """Helper for binary arithmetic operations"""
        self.output_file.write(f"{self.selectTopOfStack()}\nD=M\nA=A-1\nM=M{op}D\n")

    def writeUnaryOperation(self, op):
        '''Helper for unary arithemetic operations'''
        self.output_file.write(f'{self.selectTopOfStack()}\nM={op}M\n')


    def writeArithmetic(self, command):
        '''
        Write assembly code that implements arithmetic commands
        '''
        if command == 'add':
            self.writeBinaryOperation('+')
        elif command == 'sub':
            self.writeBinaryOperation('-')
        elif command == 'and':
            self.writeBinaryOperation('&')
        elif command == 'or':
            self.writeBinaryOperation('|')
        elif command == 'neg':
            self.writeUnaryOperation('-')
        elif command == 'not':
            self.writeUnaryOperation('!')
        elif command in ['eq', 'gt', 'lt']:
            self.writeComparison(command)
            
    
    def writeComparison(self, command):
        '''Helper for comparison operations (eg, gt, lt)'''
        jump_map = {'eq', 'JEQ', 'gt', 'JGT', 'lt', 'JLT'}
        jump_cmd = jump_map[command]

        true_label = f'TRUE_{self.label_counter}'
        end_label = f'END_{self.label_counter}'
        self.label_counter += 1

        self.output_file.write(f'{self.selectTopOfStack()}\nD=M\nA=A-1\nD=M-D\n@{true_label}\nD;{jump_cmd}\n@SP\nA=M-1\nM=0\n@{end_label}\n0;JMP\n({true_label})\n@SP\nA=M-1\nM=-1\n({end_label})\n')


    def selectTopOfStack(self):
        return '@SP\nAM=M-1'
    
    def selectStackPointer(self):
        return '@SP\nAM=M'
    
    def incrementStackPointer(self):
        return '@SP\nM=M+1'

    def selectSegmentIndex(self,segment):
        return f'@{segment}\nD=D+A\nA=D\n'
    
    def writePushPop(self, command, segment, index):
        '''
        Writes to the output file the assembly code that implements the given command,
        where command is either push or pop
        '''
        if command == 'C_PUSH':
            if segment == 'constant':
                self.output_file.write(f'@{index}\nD=A\n{self.selectStackPointer()}\nM=D\n{self.incrementStackPointer()}\n')
            else:
                base_address = self.getSegmentBase(segment=segment)
                self.output_file.write(
                    f"@{base_address}\n"
                    "D=M\n" if segment in ['local', 'argument', 'this', 'that'] else "D=A\n"
                    f"@{index}\n"
                    "A=D+A\n"
                    "D=M\n"
                    "@SP\n"
                    "A=M\n"
                    "M=D\n"
                    "@SP\n"
                    "M=M+1\n"
                )

        elif command == 'C_POP':
            base_address = self.getSegmentBase(segment=segment)
            self.output_file.write(f'@{base_address}\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n{self.selectTopOfStack()}\nD=M\n@R13\nM=D\n')

    def getSegmentBase(self, segment):
        """Get the base address for memory segments"""
        segment_map = {
            'local': 'LCL',
            'argument': 'ARG', 
            'this': 'THIS',
            'that': 'THAT',
            'temp': '5',
            'static': '16'
        }
        return segment_map.get(segment, '0')


    def close(self):
        '''
        Closes the output file
        '''
        self.output_file.close()