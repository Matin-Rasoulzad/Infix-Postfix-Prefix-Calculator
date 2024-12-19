import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify
import sys
from pathlib import Path

path_to_module = Path(".ipynb_checkpoints/mino")
sys.path.append(str(path_to_module))

import coring

class ExpressionCalculator:
    extras = True
    precedence = {"(":1 , ")":1 , "^": 2, "*" : 3, "×" : 3, "/": 3, "+": 4, "-":4 ,"−": 4}

    @classmethod
    def infix2postfix(cls, infix):
        stack = []
        postfix = []
        res =  coring.Infix_to_Postfix(infix)
        for element in infix:
            if cls.extras:
                break
            if (element[0] == "-" or element[0] == "−") and element[1:].isdigit():
                postfix.append(element)
                print(element[1:])


            elif element.isalnum():
                # alphabet letter (a-z) and numbers (0-9)
                postfix.append(element)



            elif element == '(':
                stack.append(element)
            elif element == ')':
                while stack and stack[-1] != '(':
                    postfix.append(stack.pop())
                if not stack:
                    raise ValueError("Mismatched parentheses in expression")
                stack.pop()  # Remove ( from the stack
            else:
                if stack and not cls.precedence.get(stack[-1]) == 1:
                    while (stack and cls.precedence.get(element, 0) <= cls.precedence.get(stack[-1], 0)):
                        # Send element as a key, if not found, return 0
                        postfix.append(stack.pop())
                stack.append(element)

        # Pop any remaining operators from the stack
        while stack:
            if stack[-1] == '(' or stack[-1] == ')':
                raise ValueError("Mismatched parentheses in expression")
            postfix.append(stack.pop())

        return res
    @classmethod
    def infix2prefix(cls, infix):
        stack = []
        prefix = []

        res1 = coring.Infix_to_Prefix(infix)
        for element in infix:
            if cls.extras:
                break
            if (element[0] == "-" or element[0] == "−") and element[1:].isdigit():
                prefix.insert(0, element)
            
            elif element.isalnum():
                prefix.insert(0, element)
            
            elif element == ')':
                stack.append(element)
            
            elif element == '(':
                # Pop operators until ')' is encountered
                while stack and stack[-1] != ')':
                    prefix.insert(0, stack.pop())
                if not stack:
                    raise ValueError("Mismatched parentheses in expression")
                stack.pop()  # Remove ')' from the stack
            
            else:
                # For prefix, we compare with less than or equal
                # Because we're processing from right to left
                while (stack and 
                      stack[-1] != ')' and 
                      cls.precedence.get(element, 0) >= cls.precedence.get(stack[-1], 0)):
                    prefix.insert(0, stack.pop())
                stack.append(element)
        
        # Pop remaining operators from the stack
        while stack:
            operator = stack.pop()
            if operator in ('(', ')'):
                raise ValueError("Mismatched parentheses in expression")
            prefix.insert(0, operator)
        
        return res1
    @classmethod
    def evaluate_postfix(cls,postfix):
        stack = []
        res1 = coring.postfix_calculator(postfix)
        for element in postfix:
            if cls.extras:
                break
            if element.isdigit() or (element.lstrip("-").isdigit()):  # Check if it's a number
                stack.append(int(element))
            else:
                if len(stack) < 2:
                    raise ValueError("Invalid postfix expression")
                
                # Pop the top two elements
                b = stack.pop()
                a = stack.pop()

                # Perform the operation
                if element == '+':
                    stack.append(a + b)
                elif element == '-' or element == '-':
                    stack.append(a - b)
                elif element == '*' or element == '×':
                    stack.append(a * b)
                elif element == '/':
                    if b == 0:
                        raise ZeroDivisionError("Division by zero")
                    stack.append(a / b)
                elif element == '^':
                    stack.append(a ** b)
                else:
                    raise ValueError(f"Unknown operator: {element}")
        return res1
    
    @classmethod
    def string_to_function(self,input_str):
    # Define the function using eval to compute the expression
        def f(x):
            return eval(input_str)
        return f
    @staticmethod
    def process_and_plot(expression):

        # Define the range for x
        x = np.linspace(-10, 10, 500)

        # Define the function
        func = ExpressionCalculator.string_to_function(expression)
        y = func(x)
        # Create the plot
        plt.plot(x, y, label=f"{expression}",color="red")
        plt.title(f"Plot of {expression}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.axhline(0, color='black',linewidth=0.2)
        plt.axvline(0, color='black',linewidth=0.2)
        plt.grid(color = 'black', linestyle = '-', linewidth = 0.3)
        plt.legend()
        plt.show()


calc = ExpressionCalculator()
infix_expression = "-2 * ( 3 - 1 + 5 ^ 2 )"
try:
    postfix_expression = calc.infix2postfix(infix_expression)
    print("Postfix:", postfix_expression)
except ValueError as e:
    print("Error:", e)


calc = ExpressionCalculator()
infix_expression = "-2 * ( 3 - 1 + 5 ^ 2 )"
try:
    prefix_expression = calc.infix2prefix(infix_expression)
    print("Prefix:", prefix_expression)
except ValueError as e:
    print("Error:", e)

calc = ExpressionCalculator()
postfix_expression = "3 1 + 1 3 - *"
try:
    print("Result:", calc.evaluate_postfix(postfix_expression))
except ValueError as e:
    print("Error:", e)