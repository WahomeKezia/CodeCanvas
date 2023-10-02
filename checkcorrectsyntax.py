'''
I will be using Abstract Syntax Trees (ast) library to check is the code pasted by the user has correct
syntax
'''

# this is a code snippet of the function using ast
import ast


def check_syntax(pasted_code):
    try:
        ast.parse(pasted_code)
        return True, None  # Syntax is correct
    except SyntaxError as e:
        return False, str(e)  # Syntax error message
