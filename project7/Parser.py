class Parser:

    def __init__(self, input_file):

        with open(input_file, 'r') as file:
            lines = file.readlines()

        self.current_command_index = 0
        self.commands = self.cleanLines(lines)


    def cleanLines(self, lines):
        """Remove empty lines and comments"""
        clean_lines = []
        for line in lines:
            line = line.strip()
            # Remove comments and empty lines
            if line and not line.startswith('//'):
                # Remove inline comments
                if '//' in line:
                    line = line[:line.index('//')].strip()
                if line:  # Only add non-empty lines
                    clean_lines.append(line)
        return clean_lines

    def hasMoreCommands(self):
        """Check if there are more commands to process"""
        return self.current_command_index < len(self.commands) - 1

    def advance(self):
        """Move to the next command"""
        if self.hasMoreCommands():
            self.current_command_index += 1

    def commandType(self):
        """Return the type of the current command"""
        if self.current_command_index < 0:
            return None
        
        current_command = self.commands[self.current_command_index]
        first_word = current_command.split()[0]
        
        if first_word == 'push':
            return 'C_PUSH'
        elif first_word == 'pop':
            return 'C_POP'
        else:
            return 'C_ARITHMETIC'


    def arg1(self):
        '''
        Returns the first argument of the current command. It could be pop, push, add, sub..
        '''
        current_command = self.commands[self.current_command_index]
        if self.commandType() == 'C_ARITHMETIC':
            return current_command.split(' ')[0]
        else:
            return current_command.split(' ')[1]

    def arg2(self):
        """Return the second argument (index) as integer"""
        current_command = self.commands[self.current_command_index]
        return int(current_command.split()[2])