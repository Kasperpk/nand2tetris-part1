import sys
from Parser import Parser

comp_table = {'0': '0101010',
              '1': '0111111',
              '-1':'0111010',
              'D': '0001100',
              'A': '0110000',
              'M': '1110000',
              '!D': '0001101',
              '!A': '0110001',
              '!M': '1110001',
              '-D': '0001101',
              '-A': '0110001',
              '-M': '1110001',
              'D+1': '0011111',
              'A+1': '0110111',
              'M+1': '1110111',
              'D-1': '0001110',
              'A-1': '0110010',
              'M-1': '1110010',
              'D+A': '0000010',
              'D+M': '1000010',
              'D-A': '0010011',
              'D-M': '1010011',
              'A-D': '0000111',
              'M-D': '1000111',
              'D&A': '0000000',
              'D&M': '1000000',
              'D|A': '0010101',
              'D|M': '1010101',
            }


dest_table = {'0': '000',
              'M': '001',
              'D': '010',
              'DM': '011',
              'MD': '011',
              'A': '100',
              'AM': '101',
              'AD': '110',
              'ADM': '111'}
    
jmp_table = {'null': '000',
             'JGT': '001',
             'JEQ': '010',
             'JGE': '011',
             'JLT': '100',
             'JNE': '101',
             'JLE': '110',
             'JMP': '111'}

symbolTable = {
                'SP': 0,
                'LCL': 1,
                'THIS': 2,
                'THAT': 4,
                'SCREEN': 16384,
                'KDB': 24576,
                }

symbolTable.update({f'R{i}': i for i in range(16)})


def cleanFile(inputFile):
        '''Removes whitespaces and comments from asm file'''
        clean_lines = []
        with open(inputFile, 'r') as file:
              file = file
              for line in file.readlines():
                line = line.split('/')[0] # split lines and select everything before comment
                line = line.strip()       # strip any whitespace
                if line == '':
                    continue
                clean_lines.append(line) # append the cleaned line to the list
        return clean_lines
        
        
        
    

if __name__ == '__main__':
    inputFile = sys.argv[1]
    cleanedFile = cleanFile(inputFile)
    parser = Parser(symbol_table=symbolTable, 
                    comp_table=comp_table, 
                    dest_table=dest_table, 
                    jmp_table=jmp_table)
    codeLine = parser.parsing(cleanedFile)
    
    outputFile = inputFile.replace('asm','hack')

    with open(outputFile, 'w') as file:
         for line in codeLine:
              file.write(line + '\n')
  
