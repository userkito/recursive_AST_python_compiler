'''
Performs semantic analysis on the nodes of an AST.

@author Nicolás Rodrigo Pèrez
@date 02-05-2023
@version 1.0
'''
class SemanticAnalyzer:
    

    '''
    Create new SemanticAnalyzer object.

    @type ast: tuple
    @param ast: an AST
    '''
    def __init__(self, ast):
        self.ast = ast
        self.symbols = {}
        # add some predefined functions
        self.symbols[('IDENTIFIER', 'print')] = ([('STRING', 'string')], [])


    '''
    Main function which analyzes the given AST node. An AST is considered an AST node in itself.

    @rtype: tuple
    @returns: AST node
    '''
    def analyze(self):
        return self.visit(self.ast)


    '''
    Visit the given AST node, and if required, store the node values on the current program global symbols.

    @raise TypeError: if the AST node is not valid
    @raise ValueError: if the number of arguments for a function is not correct
    @raise ValueError: if a function is not defined

    @type node: tuple
    @param node: AST node

    @rtype: tuple
    @returns: AST node
    '''
    def visit(self, node):
        
        node_type = node[0]

        #print(str(node) + '\n')
        
        if node_type == 'PROGRAM':
            statements = []
            for statement in node[1]:
                statements.append(self.visit(statement))
            return ('PROGRAM', statements)
        
        elif node_type == 'IMPORT':
            body = node[1]
            return ('IMPORT', body)

        elif node_type == 'ASSIGNMENT':
            identifier = node[1]
            value = self.visit(node[2])
            self.symbols[identifier] = value
            return ('ASSIGNMENT', identifier, value)

        elif node_type == 'SELF_ASSIGNMENT':
            identifier = node[1]
            value = self.visit(node[2])
            self.symbols[identifier] = value
            return ('SELF_ASSIGNMENT', identifier, value)

        elif node_type == 'CLASS_ASSIGNMENT':
            identifier = node[1]
            class_identifier = node[2]
            arguments = []
            for argument in node[3]:
                arguments.append(self.visit(argument))
            self.symbols[identifier] = (class_identifier, arguments)
            return ('CLASS_ASSIGNMENT', identifier, class_identifier, arguments)

        elif node_type == 'ATRIBUTE_ACCESS':
            identifier = node[1]
            body = []
            for statement in node[2]:
                body.append(self.visit(statement))
            self.symbols[identifier] = body
            return ('ATRIBUTE_ACCESS', identifier, body)

        elif node_type == 'IF_STATEMENT':
            if_condition = self.visit(node[1])
            if_body = []
            for statement in node[2]:
                if_body.append(self.visit(statement))
            return ('IF_STATEMENT', if_condition, if_body)

        elif node_type == 'ELIF_STATEMENT':
            elif_condition = self.visit(node[1])
            elif_body = []
            for statement in node[2]:
                elif_body.append(self.visit(statement))
            return ('ELIF_STATEMENT', elif_condition, elif_body)

        elif node_type == 'ELSE_STATEMENT':
            else_body = []
            for statement in node[1]:
                else_body.append(self.visit(statement))
            return ('ELSE_STATEMENT', else_body)
        
        elif node_type == 'FOR_LOOP':
            identifier = node[1]
            iterable = self.visit(node[2])
            body = self.visit(node[3])
            return ('FOR_LOOP', identifier, iterable, body)
        
        elif node_type == 'WHILE_LOOP':
            condition = self.visit(node[1])
            body = []
            for statement in node[2]:
                body.append(self.visit(statement))
            return ('WHILE_LOOP', condition, body)
        
        elif node_type == 'CLASS_DECLARATION':
            class_name = node[1]
            parent_class = node[2]
            body = []
            for statement in node[3]:
                body.append(self.visit(statement))
            self.symbols[class_name] = (parent_class, body)
            return ('CLASS_DECLARATION', class_name, parent_class, body)
        
        elif node_type == 'FUNCTION_DEFINITION':
            function_name = node[1]
            parameters = node[2]
            body = []
            for statement in node[3]:
                body.append(self.visit(statement))
            self.symbols[function_name] = (parameters, body)
            return ('FUNCTION_DEFINITION', function_name, parameters, body)
        
        elif node_type == 'FUNCTION_CALL':
            function_name = node[1]
            arguments = []
            for argument in node[2]:
                arguments.append(self.visit(argument))
            if function_name[1] == 'print':
                #return self.call_function(function, arguments)
                return node
            if function_name in self.symbols:
                function = self.symbols[function_name]
                if ('SELF', 'self') in function[0]:
                    if len(arguments) == len(function[0]) - 1:
                        #return self.call_function(function, arguments)
                        return node
                    else:
                        raise ValueError(f"Invalid number of arguments for class function {function_name}")
                else:
                    if len(arguments) == len(function[0]):
                        #return self.call_function(function, arguments)
                        return node
                    else:
                        raise ValueError(f"Invalid number of arguments for function {function_name}")
            else:
                raise ValueError(f"Undefined function: {function_name}")

        elif node_type == 'RETURNED':
            returned = self.visit(node[1])
            return ('RETURNED', returned)
        
        elif node_type == 'OPERATION':
            operator = node[1]
            left = self.visit(node[2])
            right = self.visit(node[3])
            return ('OPERATION', operator, left, right)

        elif node_type == 'LOGICAL_EXPRESSION':
            operator = node[1]
            left = self.visit(node[2])
            right = self.visit(node[3])
            return ('LOGICAL_EXPRESSION', operator, left, right)

        elif node_type == 'COMPARISON_EXPRESSION':
            operator = node[1]
            left = self.visit(node[2])
            right = self.visit(node[3])
            return ('COMPARISON_EXPRESSION', operator, left, right)
        
        elif node_type in ('NUMBER', 'STRING', 'IDENTIFIER', 'SELF_IDENTIFIER'):
            '''
            if node_type in ('IDENTIFIER', 'SELF_IDENTIFIER'):
                identifier = node[1]
                if identifier not in self.symbols:
                    raise ValueError(f"Undefined variable: {identifier}")
            '''
            return node
        
        else:
            raise TypeError(f"Invalid node type: {node_type}")


    '''
    (EXPERIMENTAL)

    Simulates the execution of the code inside a function, merging its local symbols
    with the global symbols, and checking for runTime errors.

    @type function: tuple
    @param function: function definition in the global symbols

    @type arguments: list
    @param arguments: arguments passed to the function on its calling

    @rtype: list
    @returns: list of analyzed statements inside the functions body
    '''
    def call_function(self, function, arguments):
        analyzer = SemanticAnalyzer()
        parameters = function[1]
        body = function[2]
        local_symbols = {}
        for param, arg in zip(parameters, arguments):
            local_symbols[param] = arg
        #print('local symbols: ' + str(local_symbols) + '\n')
        analyzer.symbols = {**self.symbols, **local_symbols}
        #print('merged symbols: ' + str(analyzer.symbols) + '\n')
        statements = []
        for statement in body:
            statements.append(analyzer.visit(statement))
        return statements