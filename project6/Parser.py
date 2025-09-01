class Parser:

    def __init__(self, symbol_table, comp_table, dest_table, jmp_table):

        self.symbol_table = symbol_table
        self.comp_table = comp_table
        self.dest_table = dest_table
        self.jmp_table = jmp_table

      
    
    def firstPass(self, clean_lines):
        '''First pass parsing, locating potential symbol labels, that need to
        be added to the symbol table'''

        line_number = 0
        parsed_lines = []
        for line in clean_lines:
            if line.startswith('('):
                self.symbol_table[line[1:-1].split(')')[0]] = line_number
            else:
                parsed_lines.append(line)
                line_number = line_number + 1

        return parsed_lines
        

    def secondPass(self,parsed_lines):
        '''
        second pass that adds symbol variables to symbol table
        '''
        n = 16
        for line in parsed_lines:
            if line.startswith('@'):
                symbol = line.split('@')[1]
                if symbol in self.symbol_table:
                    continue
                elif symbol[0].isdigit():
                    continue
                else:
                    self.symbol_table[symbol] = n
                    n = n + 1



    def breakDownInstruction(self, parsed_lines):
        '''Breaks down c-instructions into its components'''
        codelines = []
        for line in parsed_lines:
            # Translating C instructions
            if not line.startswith('@'):
                if '=' in line:
                    dest = line.split('=')[0]
                    comp = line.split('=')[1]
                    string = '111' + self.comp_table[comp] + self.dest_table[dest] + '000'
                    codelines.append(string)

                elif ';' in line:
                    jmp = line.split(';')[1]
                    comp = line.split(';')[0]
                    string = '111' + self.comp_table[comp] + '000' + self.jmp_table[jmp]
                    codelines.append(string)
            else:
                # Translating A instructions
                symbol = line.split('@')[1]
                if symbol in self.symbol_table.keys():
                    value = self.symbol_table[symbol]
                    binary_value = self.decimalToBinary(value)
                else:
                    binary_value = self.decimalToBinary(symbol)

                string = '0' + binary_value
                codelines.append(string)

        return codelines


    def decimalToBinary(self, value):

        word = []

        remainder = int(value)

        while remainder > 0:

            quotient = remainder % 2

            remainder = remainder // 2

            word.append(str(quotient))
        
        while len(word) != 15:
            word.append('0')

        word.reverse()

        return ''.join(word)

    def parsing(self, file):
        firstPass = self.firstPass(file)
        self.secondPass(firstPass)
        instructionBreakdown = self.breakDownInstruction(firstPass)
        return instructionBreakdown

            
        
