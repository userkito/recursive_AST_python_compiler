from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from code_generator import CodeGenerator
'''
Basic python compiler based on a recursive implementation of an AST (Abstract Syntax Tree),
heavily scalable following the simple logic used.

@author Nicolás Rodrigo Pèrez
@date 02-05-2023
@version 1.0
'''
class Compiler:


    '''
    Create new Compiler object.

    @type debug: int
    @param debug: debug level, 0 for disabled, else enabled
    '''
    def __init__(self, debug):
        self.debug = debug


    '''
    Main fuction which compiles the given python code in 4 phases:
    - Lexer
    - Parser
    - Semantic Analyzer
    - Code Generator

    @type source_code: str
    @param source_code: string of python code to compile
    '''
    def compile(self, source_code):

        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        if self.debug != 0: print('1. -> Lexer:\n\n' + str(tokens) + '\n\n\n')

        parser = Parser(tokens)
        ast = parser.parse()
        if self.debug != 0: print('2. --> Parser:\n\n' + str(ast) + '\n\n\n')

        semantic_analyzer = SemanticAnalyzer(ast)
        analyzed_ast = semantic_analyzer.analyze()
        if self.debug != 0: print('3. ---> Semantic Analizer:\n\n' + str(analyzed_ast) + '\n\n\n')

        code_generator = CodeGenerator(analyzed_ast)
        compiled_code = code_generator.generate()
        if self.debug != 0: print('4. ----> Code Generator:\n\n' + str(compiled_code) + '\n\n\n')
