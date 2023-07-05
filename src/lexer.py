import re
'''
Tokenizes a raw string into a list of basic python tokens.

@author Nicolás Rodrigo Pèrez
@date 02-05-2023
@version 1.0
'''
class Lexer:
    

    '''
    Create new Lexer object which defines some of the most common keywords in python.

    @type source_code: str
    @param source_code: string to tokenize
    '''
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.lineno = 1
        self.indentation_stack = [0]
        self.default_indentation = 4
        self.token_patterns = [
            (r'\bif\b', 'IF'),
            (r'\belif\b', 'ELIF'),
            (r'\belse\b', 'ELSE'),
            (r'\bfor\b', 'FOR'),
            (r'\bin\b', 'IN'),
            (r'\bwhile\b', 'WHILE'),
            (r'\bclass\b', 'CLASS'),
            (r'\bdef\b', 'DEF'),
            (r'\breturn\b', 'RETURN'),
            (r'\bimport\b', 'IMPORT'),
            (r'\bas\b', 'AS'),
            (r'\bTrue\b', 'TRUE'),
            (r'\bFalse\b', 'FALSE'),
            (r'\bNone\b', 'NONE'),
            (r'\bpass\b', 'PASS'),
            (r'\band\b', 'AND'),
            (r'\bor\b', 'OR'),
            (r'\bnot\b', 'NOT'),
            (r'\b[A-Z][A-Za-z0-9_]*\b', 'CLASS_IDENTIFIER'),
            (r'\b[a-z_][a-z0-9_]*\b', 'IDENTIFIER'),
            (r':=', 'WALRUS'),
            (r'==', 'EQUALS'),
            (r'=', 'ASSIGN'),
            (r'!=', 'NOT_EQUALS'),
            (r'>=', 'GREATER_THAN_EQUAL'),
            (r'>', 'GREATER_THAN'),
            (r'<=', 'LESS_THAN_EQUAL'),
            (r'<', 'LESS_THAN'),
            (r'\d+', 'NUMBER'),
            (r'".*?"', 'STRING'),
            (r'\+', 'ADD'),
            (r'-', 'SUBTRACT'),
            (r'\*', 'MULTIPLY'),
            (r'/', 'DIVIDE'),
            (r'\(', 'LEFT_PAREN'),
            (r'\)', 'RIGHT_PAREN'),
            (r'\[', 'LEFT_BRACKET'),
            (r'\]', 'RIGHT_BRACKET'),
            (r'{', 'LEFT_BRACE'),
            (r'}', 'RIGHT_BRACE'),
            (r'\.', 'DOT'),
            (r',', 'COMMA'),
            (r':', 'COLON'),
            (r'\\', 'SLASH'),
            (r'\s+', None)  # Skip whitespace
        ]


    '''
    Main functon which goes through each line of the string to tokenize 
    looking for available token patterns.

    @rtype: list
    @returns: a list of tokens
    '''
    def tokenize(self):
        source_code = self.source_code
        source_code_lines = source_code.split('\n')

        for line in source_code_lines:
            self.process_line(line)

        return self.tokens


    '''
    Goes through the chars in a line of the string to tokenize,
    looking for a match in the available token patterns.

    @raise SyntaxError: if invalid syntax is detected

    @type line: str
    @param line: line of the string to tokenize
    '''
    def process_line(self, line):

        if self.handle_single_line_comment(line):
            self.lineno += 1
        elif self.handle_empty_line(line):
            self.lineno += 1
        else:
            self.handle_indentation(line)
            line = line.strip()
            while line:
                matched = False
                for pattern, token_type in self.token_patterns:
                    match = re.match('^' + pattern, line)
                    if match:
                        value = match.group(0)
                        if token_type:
                            self.tokens.append((token_type, value, self.lineno))
                        line = line[len(value):]
                        matched = True
                        break
                if not matched:
                    raise SyntaxError(f"Invalid syntax in line {self.lineno}: {line}")
            self.lineno += 1


    '''
    Adds INDENT and DEDENT tokens depending on the indentation level on the actual line,
    using a stack holding the indentation levels.

    @raise IndentationError: if invalid indentation is detected

    @type line: str
    @param line: line of the string to tokenize
    '''
    def handle_indentation(self, line):
        indentation_level = self.get_indentation_level(line)
        if indentation_level % self.default_indentation == 0:
            indentation_level = int(indentation_level/self.default_indentation)
            if self.indentation_stack:
                if indentation_level > self.indentation_stack[-1]:
                    self.indentation_stack.append(indentation_level)
                    self.tokens.append(('INDENT', indentation_level, self.lineno))
                    #print(str(self.tokens[-1]) + ' -- ' + line + '\n')
                elif indentation_level < self.indentation_stack[-1]:
                    while self.indentation_stack[-1] > indentation_level:
                        self.tokens.append(('DEDENT', self.indentation_stack[-1], self.lineno))
                        self.indentation_stack.pop()
                        #print(str(self.tokens[-1]) + ' -- ' + line + '\n')
        else:
            raise IndentationError(f"Invalid indentation in line {self.lineno}: {line}")
        

    '''
    Calculate the indentation level on the actual line.

    @type line: str
    @param line: line of the string to tokenize

    @rtype: int
    @returns: current line indentation level
    '''
    def get_indentation_level(self, line):
        count = 0
        for char in line:
            if char == ' ':
                count += 1
            elif char == '\t':
                count += 4
            else:
                break
        return count


    '''
    Match a single line comment on the actual line.

    @type line: str
    @param line: line of the string to tokenize

    @rtype: bool
    @returns: true if comment found, else false
    '''
    def handle_single_line_comment(self, line):
        comment_pattern = r'\s*#.*\n*'
        if re.match('^' + comment_pattern, line):
            return True
        else:
            return False


    '''
    Determine if actual line is empty.

    @type line: str
    @param line: line of the string to tokenize

    @rtype: bool
    @returns: true if actual line is empty, else false
    '''
    def handle_empty_line(self, line):
        if line == '':
            return True
        else:
            return False
