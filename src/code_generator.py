'''
Generates readable python code from the nodes of an AST.

@author Nicolás Rodrigo Pèrez
@date 02-05-2023
@version 1.0
'''
class CodeGenerator:


    '''
    Create new CodeGenerator object.

    @type ast: tuple
    @param ast: an AST
    '''
    def __init__(self, ast):
        self.ast = ast
        self.fc_check = False


    '''
    Main function which generates the python code for the given AST node. An AST is considered an AST node in itself.

    @rtype: str
    @returns: plain text python code
    '''
    def generate(self):
        return self.visit(self.ast)
        

    '''
    Visit the given AST node, and generate the python code related to it.

    @raise TypeError: if the AST node is not valid

    @type node: tuple
    @param node: AST node

    @rtype: str
    @returns: plain text python code
    '''
    def visit(self, node):

        node_type = node[0]
        
        if node_type == 'PROGRAM':
            statements = ''
            for i in range(len(node[1])):
                statements += self.visit(node[1][i])
            return statements

        elif node_type == 'IMPORT':
            value = self.visit(node[1])
            return f'import {value}\n\n'

        elif node_type == 'AS':
            value1 = node[2][1]
            value2 = node[1][1]
            return f'{value1} as {value2}'
        
        elif node_type == 'ASSIGNMENT' or node_type == 'SELF_ASSIGNMENT':
            identifier = node[1][1]
            value = self.visit(node[2])
            if self.fc_check == True:
                self.fc_check = False
                return f'{identifier} = {value}'
            else:
                return f'{identifier} = {value}\n\n'

        elif node_type == 'CLASS_ASSIGNMENT':
            identifier = node[1][1]
            value = self.visit(node[2])
            arguments = ''
            for i in range(len(node[3])):
                if i == len(node[3]) - 1:
                    arguments += node[3][i][1]
                else:
                    arguments += node[3][i][1] + ', '
            return f'{identifier} = {value}({arguments})\n\n'
        
        elif node_type == 'IF_STATEMENT':
            condition = self.visit(node[1])
            if_body = ''
            for i in range(len(node[2])):
                if_body += self.visit(node[2][i])
            return f'if {condition}:\n\n{if_body}'

        elif node_type == 'ELIF_STATEMENT':
            condition = self.visit(node[1])
            elif_body = ''
            for i in range(len(node[2])):
                elif_body += self.visit(node[2][i])
            return f'elif {condition}:\n\n{elif_body}'

        elif node_type == 'ELSE_STATEMENT':
            else_body = ''
            for i in range(len(node[1])):
                else_body += self.visit(node[1][i])
            return f'else:\n\n{else_body}'
        
        elif node_type == 'FOR_LOOP':
            identifier = node[1]
            iterable = self.visit(node[2])
            body = self.visit(node[3])
            return f'for {identifier} in {iterable}:\n\n{body}'
        
        elif node_type == 'WHILE_LOOP':
            condition = self.visit(node[1])
            body = ''
            for i in range(len(node[2])):
                body += self.visit(node[2][i])
            return f'while {condition}:\n\n{body}'
        
        elif node_type == 'CLASS_DECLARATION':
            class_name = node[1][1]
            parent_class = node[2][1]
            body = ''
            for i in range(len(node[3])):
                body += self.visit(node[3][i])
            if parent_class is not None:
                return f'class {class_name}({parent_class}):\n\n{body}'
            else:
                return f'class {class_name}:\n\n{body}'
        
        elif node_type == 'FUNCTION_DEFINITION':
            function_name = node[1][1]
            parameters = ''
            for i in range(len(node[2])):
                if i == len(node[2]) - 1:
                    parameters += node[2][i][1]
                else:
                    parameters += node[2][i][1] + ', '
            body = ''
            for i in range(len(node[3])):
                body += self.visit(node[3][i])
            return f'def {function_name}({parameters}):\n\n{body}'
        
        elif node_type == 'FUNCTION_CALL':
            self.fc_check = True
            function_name = node[1][1]
            arguments = ''
            for i in range(len(node[2])):
                if i == len(node[2]) - 1:
                    arguments += node[2][i][1]
                else:
                    arguments += node[2][i][1] + ', '
            return f'{function_name}({arguments})\n\n'

        elif node_type == 'ATRIBUTE_ACCESS':
            identifier = node[1][1]
            body = ''
            for i in range(len(node[2])):
                body += self.visit(node[2][i])
            return f'{identifier}.{body}'

        elif node_type == 'LOGICAL_EXPRESSION':
            operator = node[1]
            left = self.visit(node[2])
            right = self.visit(node[3])
            return f'{left} {operator} {right}'

        elif node_type == 'COMPARISON_EXPRESSION':
            operator = node[1]
            left = self.visit(node[2])
            right = self.visit(node[3])
            return f'{left} {operator} {right}'
        
        elif node_type == 'OPERATION':
            operator = node[1]
            left = node[2][1]
            right = self.visit(node[3])
            return f'{left} {operator} {right}'

        elif node_type == 'RETURNED':
            returned = self.visit(node[1])
            return f'return {returned}\n\n'
        
        elif node_type == 'NUMBER' or node_type == 'STRING' or node_type == 'IDENTIFIER' or node_type == 'SELF_IDENTIFIER' or node_type == 'CLASS_IDENTIFIER':
            return f'{node[1]}'
        
        else:
            raise TypeError(f"Invalid node type: {node_type}")