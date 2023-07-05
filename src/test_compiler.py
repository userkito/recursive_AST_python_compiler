import os
from compiler import Compiler

test_code = open(f'{os.getcwd()}/test/full_test.py', 'r+').read()

compiler = Compiler(1) # 0 debug disabled, else enabled
compiler.compile(test_code)