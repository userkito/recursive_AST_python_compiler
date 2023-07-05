'''
Generates an AST from a list of basic python tokens, and performs syntactic analysis on its nodes.

@author Nicolás Rodrigo Pèrez
@date 02-05-2023
@version 1.0
'''
class Parser:
    

    '''
    Create new Parser object.

    @type tokens: list
    @param tokens: a list of tokens
    '''
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token_line = 1
        self.current_token = self.tokens[self.current_token_index]
        self.if_check = False
        self.return_check = False


    '''
    Checks if current token is not None and that is not the end of the list,
    and goes on one position on the tokens list.
    '''
    def advance(self):
        self.current_token_index += 1
        if self.current_token is not None and self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
            self.current_token_line = self.current_token[2]
        else:
            self.current_token = None


    '''
    Check if current token is of the desired pattern, or any pattern, if so,
    advance on the tokens list.

    @raise SyntaxError: if invalid syntax is detected

    @type token_type: str
    @param token_type: token pattern or 0
    '''
    def consume(self, token_type):
        if token_type == 0:
            self.advance()
        elif self.current_token[0] == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Invalid syntax in line {self.current_token_line}: expected {token_type} got {self.current_token[1]}") 


    '''
    Main function which parses a python program into an AST, and 
    checks the correct ending of the program.

    @raise SyntaxError: if invalid syntax is detected

    @rtype: tuple
    @returns: an AST
    '''
    def parse(self):
        program = self.parse_program()
        ast = ('PROGRAM', program)
        if self.current_token is not None:
            raise SyntaxError(f"Invalid syntax in line {self.current_token_line}")
        return ast


    '''
    Parses the different statements that compose a python program.

    @rtype: list
    @returns: list of statements
    '''
    def parse_program(self):
        statements = []
        while self.current_token is not None:
            statements.append(self.parse_statement())
        return statements


    '''
    Parses the correctness of parameters in statements which require of them.

    @rtype: list
    @returns: list of parameters
    '''
    def parse_parameters(self):
        self.consume('LEFT_PAREN')
        parameters = []
        while self.current_token is not None and self.current_token[0] != 'RIGHT_PAREN':
            parameters.append(self.parse_factor())
            if self.current_token is not None and self.current_token[0] == 'COMMA':
                self.consume('COMMA')
        self.consume('RIGHT_PAREN')
        self.consume('COLON')
        return parameters


    '''
    Parses the correctness of arguments in statements which require of them.

    @rtype: list
    @returns: list of arguments
    '''
    def parse_arguments(self):
        self.consume('LEFT_PAREN')
        arguments = []
        while self.current_token is not None and self.current_token[0] != 'RIGHT_PAREN':
            argument = self.parse_factor()
            arguments.append(argument)
            if self.current_token is not None and self.current_token[0] == 'COMMA':
                self.consume('COMMA')
        self.consume('RIGHT_PAREN')
        return arguments
        

    '''
    Parses blocks, a block being an agrupation of statements in between an INDENT and a DEDENT token.

    @rtype: list
    @returns: list of statements
    '''
    def parse_block(self):
        self.consume('INDENT')
        statements = []
        while self.current_token is not None and self.current_token[0] != 'DEDENT':
            statements.append(self.parse_statement())
        self.consume('DEDENT')
        return statements


    '''
    Parses factors, a factor being the smaller of the possible python structures.

    @raise SyntaxError: if invalid syntax is detected

    @rtype: tuple
    @returns: AST node
    '''
    def parse_factor(self):

        token_type, token_value, lineno = self.current_token

        if token_type == 'NONE':
            self.consume(0)
            node = ('NONE', token_value)
            return node

        elif token_type == 'NUMBER':
            self.consume(0)
            node = ('NUMBER', token_value)
            return node

        elif token_type == 'STRING':
            self.consume(0)
            node = ('STRING', token_value)
            return node

        elif token_type == 'CLASS_IDENTIFIER':
            self.consume(0)
            node = ('CLASS_IDENTIFIER', token_value)
            return node

        elif token_type == 'IDENTIFIER':
            self.consume(0)
            if token_value == 'self':
                if self.current_token[0] == 'DOT':
                    self.consume('DOT')
                    mod_token_value = 'self.' + self.current_token[1]
                    self.consume(0)
                    node = ('SELF_IDENTIFIER', mod_token_value)
                else:
                    node = ('SELF', token_value)
                return node
            else:
                node = ('IDENTIFIER', token_value)
                return node

        else:
            raise SyntaxError(f"Invalid syntax in line {self.current_token_line}: {token_type} {token_value}")
        

    '''
    Parses expressions, an expression being an agrupation of factors and expressions.

    @rtype: tuple
    @returns: AST node
    '''
    def parse_expression(self):
        
        node = self.parse_factor()

        if self.current_token is not None and self.current_token[0] in ('MULTIPLY', 'DIVIDE', 'ADD', 'SUBTRACT'):
            operator = self.current_token[1]
            self.consume(0)
            right = self.parse_factor() 
            node = ('OPERATION', operator, node, right)
            return node

        elif self.current_token is not None and self.current_token[0] in ('EQUALS', 'NOT_EQUALS', 'GREATER_THAN', 'LESS_THAN', 'GREATER_THAN_EQUAL', 'LESS_THAN_EQUAL'):
            cmp_operator = self.current_token[1]
            self.consume(0)
            cmp_right = self.parse_expression()
            cmp_node = ('COMPARISON_EXPRESSION', cmp_operator, node, cmp_right)
            if self.current_token is not None and self.current_token[0] in ('AND', 'OR', 'NOT'):
                lgc_operator = self.current_token[1]
                self.consume(0)
                lgc_rigth = self.parse_expression()
                lgc_node = ('LOGICAL_EXPRESSION', lgc_operator, cmp_node, lgc_rigth)
                return lgc_node
            else:
                return cmp_node

        elif self.current_token is not None and self.current_token[0] in ('DOT'):
            expressions = []
            while self.current_token is not None and self.current_token[0] in ('DOT'):
                self.consume('DOT')
                expressions.append(self.parse_expression())
            node = ('ATRIBUTE_ACCESS', node, expressions)
            return node

        elif self.current_token is not None and self.current_token[0] in ('LEFT_PAREN'):
            arguments = self.parse_arguments()
            node = ('FUNCTION_CALL', node, arguments)
            return node

        elif self.current_token is not None and self.current_token[0] in ('AS'):
            self.consume('AS')
            identifier = self.parse_factor()
            node = ('AS', identifier, node)
            return node
            
        else:
            return node


    '''
    Parses statements, a statement being an agrupation of factors, expressions and statements.

    @raise SyntaxError: if invalid syntax is detected

    @rtype: tuple
    @returns: AST node
    '''
    def parse_statement(self):

        token_type, token_value, lineno = self.current_token

        if token_type == 'IDENTIFIER':

            if token_value != 'self':
                identifier = self.parse_factor()

                if self.current_token[0] == 'ASSIGN':
                    self.consume('ASSIGN')

                    if self.current_token[0] == 'CLASS_IDENTIFIER':
                        class_name = self.parse_factor()
                        arguments = self.parse_arguments()
                        node = ('CLASS_ASSIGNMENT', identifier, class_name, arguments)
                    else:
                        expression = self.parse_expression()
                        node = ('ASSIGNMENT', identifier, expression)
                    return node

                elif self.current_token[0] == 'DOT':
                    expressions = []
                    while self.current_token is not None and self.current_token[0] in ('DOT'):
                        self.consume('DOT')
                        expressions.append(self.parse_expression())
                    node = ('ATTRIBUTE_ACCESS', identifier, expressions)
                    return node

                elif self.current_token[0] == 'LEFT_PAREN':
                    arguments = self.parse_arguments()
                    node = ('FUNCTION_CALL', identifier, arguments)
                    return node

                else:
                    raise SyntaxError(f"Invalid syntax in line {self.current_token_line}: {token_type} {token_value}")

            else:
                identifier = self.parse_factor()

                if self.current_token[0] == 'ASSIGN':
                    self.consume('ASSIGN')

                    if self.current_token[0] == 'CLASS_IDENTIFIER':
                        class_name = self.parse_factor()
                        arguments = self.parse_arguments()
                        node = ('SELF_CLASS_ASSIGNMENT', identifier, class_name, arguments)
                    else:
                        expression = self.parse_expression()
                        node = ('SELF_ASSIGNMENT', identifier, expression)
                    return node

                elif self.current_token[0] == 'DOT':
                    expressions = []
                    while self.current_token is not None and self.current_token[0] in ('DOT'):
                        self.consume('DOT')
                        expressions.append(self.parse_expression())
                    node = ('SELF_ATTRIBUTE_ACCESS', identifier, expressions)
                    return node

                elif self.current_token[0] == 'LEFT_PAREN':
                    arguments = self.parse_arguments()
                    node = ('SELF_FUNCTION_CALL', identifier, arguments)
                    return node

                else:
                    raise SyntaxError(f"Invalid syntax in line {self.current_token_line}: {token_type} {token_value}")

        elif token_type == 'IMPORT':
            self.consume('IMPORT')
            imported = self.parse_expression()
            node = ('IMPORT', imported)
            return node

        elif token_type == 'IF':
            self.consume('IF')
            if_condition = self.parse_expression()
            self.consume('COLON')
            if_body = self.parse_block()
            node = ('IF_STATEMENT', if_condition, if_body)
            self.if_check = True
            return node

        elif token_type == 'ELIF' and self.if_check == True:
            self.consume('ELIF')
            elif_condition = self.parse_expression()
            self.consume('COLON')
            elif_body = self.parse_block()
            node = ('ELIF_STATEMENT', elif_condition, elif_body)
            return node

        elif token_type == 'ELSE' and self.if_check == True:
            self.consume('ELSE')
            self.consume('COLON')
            else_body = self.parse_block()
            node = ('ELSE_STATEMENT', else_body)
            self.if_check = False
            return node

        elif token_type == 'FOR':
            self.consume('FOR')
            identifier = self.parse_factor()
            self.consume('IN')
            iterable = self.parse_expression()
            self.consume('COLON')
            body = self.parse_block()
            node = ('FOR_LOOP', identifier, iterable, body)
            return node

        elif token_type == 'WHILE':
            self.consume('WHILE')
            condition = self.parse_expression()
            self.consume(0)
            body = self.parse_block()
            node = ('WHILE_LOOP', condition, body)
            return node

        elif token_type == 'CLASS':
            self.consume('CLASS')
            class_name = self.parse_factor()
            parent_class = None
            self.consume('LEFT_PAREN')
            if self.current_token[0] != 'RIGHT_PAREN':
                parent_class = self.parse_factor()
            self.consume('RIGHT_PAREN')
            self.consume('COLON')
            body = self.parse_block()
            node = ('CLASS_DECLARATION', class_name, parent_class, body)
            self.if_check = False
            return node

        elif token_type == 'DEF':
            self.return_check = True
            self.consume('DEF')
            function_name = self.parse_factor()
            parameters = self.parse_parameters()
            body = self.parse_block()
            node = ('FUNCTION_DEFINITION', function_name, parameters, body)
            self.if_check = False
            self.return_check = False
            return node

        elif token_type == 'RETURN' and self.return_check == True:
            self.consume('RETURN')
            returned = self.parse_expression()
            node = ('RETURNED', returned)
            return node

        else:
            raise SyntaxError(f"Invalid syntax in line {self.current_token_line}: {token_type} {token_value}")
