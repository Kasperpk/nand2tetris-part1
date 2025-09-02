import sys
from Parser import Parser
from CodeWriter import CodeWriter

def main():
    """Drive the VM translation process"""
    if len(sys.argv) != 2:
        print("Usage: python VMTranslator.py <file.vm>")
        return
    
    input_file = sys.argv[1]
    output_file = input_file.replace('.vm', '.asm')
    
    parser = Parser(input_file)
    code_writer = CodeWriter(output_file)
    
    while parser.hasMoreCommands():
        parser.advance()
        command_type = parser.commandType()
        
        if command_type == 'C_ARITHMETIC':
            code_writer.writeArithmetic(parser.arg1())
        elif command_type in ['C_PUSH', 'C_POP']:
            code_writer.writePushPop(command_type, parser.arg1(), parser.arg2())
    
    code_writer.close()
    print(f"Translation complete: {input_file} -> {output_file}")

if __name__ == '__main__':
    main()