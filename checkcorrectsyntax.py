'''In this app , I will bring in a new feature that checks is the 
syntax if the codes being pasted 
by the users are correct since it's only supporting python code'''

# this is a code snippet that explains the use of  a library ast (Abstract Syntax Trees)

import ast


def check_syntax(pasted_code):
    try:
        ast.parse(pasted_code)
        return True, None  # Syntax is correct
    except SyntaxError as e:
        return False, str(e)  # Syntax error message
