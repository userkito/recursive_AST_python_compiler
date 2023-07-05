
####    ####    ####
####    ####    ####
AST_PYTHON_COMPILER
####    ####    ####
####    ####    ####

@author Nicolás Rodrigo Pèrez
@date 02-05-2023
@version 1.0

A simple python compiler, implemented using a recursive version of an AST (Abstract Syntax Tree),
able to manage most of the common python errors when coding, and heavily escalable
following the simple logic used.

Its functionality is based on 4 main phases:

 - Lexer: turns a text string into a list of tokens.

 - Parser: generates an AST and performs some syntactic analysis over its nodes.

 - Semantic Analyzer: performs some semantic analysis over the AST nodes.

 - Code Generator: generates readable python code from the AST nodes.

In this compiler, the AST is the result of the syntactic analysis made by the parser. 
Then the AST goes through all the remaining phases of the compiler, visiting each node
of the AST and acting accordingly.

Usage:

 - To test the compiler, simply execute the 'test_compiler.py' file. It runs the compiler 
   over a simple python code, 'full_test.py', located in 'test' directory, not giving any output 
   if the 'debug' parameter is set to 0, meaning theres no errors on the actual code,
   or printing debugging messages for each step of the compiler elseway. 
   Try changing or adding elements to this test file, and see what the output is!!!.

