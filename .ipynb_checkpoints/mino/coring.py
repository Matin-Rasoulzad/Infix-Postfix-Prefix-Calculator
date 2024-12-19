import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        if not self.isEmpty():
            return self.stack.pop()

    def top(self):
        if not self.isEmpty():
            return self.stack[-1]
        return None

    def isEmpty(self):
        return len(self.stack) == 0


def isHigher(op, top_op):
    if top_op is None or op is None:
        return True
    precedence = { '(' : 0 , ')' : 0 , '^' : 4 , '*' : 3 , '/' : 3 , '+' : 2 , '-' : 2}
    # print(precedence[top_op] , precedence[op] , top_op , op)
    return precedence[top_op] < precedence[op]


def calculator(op1, op2, operator):
    match operator:
        case '+':
            return op1 + op2
        case '-':
            return op1 - op2
        case '*':
            return op1 * op2
        case '/':
            return op2 / op1
        case '^':
            return op1 ** op2

########################################################################################################################

def Infix_to_Postfix(exp):
    postfix = []
    exp_operator = Stack()
    operators = {'+', '-', '*', "/", '^', '(', ')'}

    exp = exp.split(" ")
    # print(exp, "kiiiii")

    for element in exp:

        if element in operators:

            if element == ")":
                while exp_operator.top() != "(":
                    # print(exp_operator.stack)
                    postfix.append(exp_operator.pop())

                exp_operator.pop()

            elif element == "(":
                exp_operator.push(element)

            elif exp_operator.isEmpty():
                exp_operator.push(element)

            elif isHigher(element , exp_operator.top()):
                # print(exp_operator.stack)
                exp_operator.push(element)


            else:
                while not isHigher(element , exp_operator.top()):
                    # print(exp_operator.stack , element)
                    postfix.append(exp_operator.pop())

                exp_operator.push(element)


        else:
            postfix.append(element)



    while not exp_operator.isEmpty():

        op = exp_operator.pop()
        postfix.append(op)

    return " ".join(postfix)


def postfix_calculator(exp):
    operands = Stack()
    operators = {'+', '-', '*', '/', '^'}

    ch = ""
    for i in range(len(exp)):
        if exp[i] == " ":
            if ch:  # Process the token only if `ch` is not empty
                if ch not in operators:
                    operands.push(float(ch))  # Support float operands
                else:
                    op1 = operands.pop()
                    op2 = operands.pop()
                    res = calculator(op2, op1, ch)  # Correct operand order
                    operands.push(res)
                ch = ""  # Reset `ch` for the next token
        else:
            ch += exp[i]

    # Handle the last token (if any)
    if ch:
        if ch not in operators:
            operands.push(float(ch))
        else:
            op1 = operands.pop()
            op2 = operands.pop()
            res = calculator(op2, op1, ch)
            operands.push(res)

    return operands.pop()  # Final result

########################################################################################################################

def Infix_to_Prefix(exp):

    # exp = exp.split(" ")[::-1]
    #
    # # print(exp)
    #
    # prefix = ""
    #
    # for i in range(len(exp)):
    #     if exp[i] == '(':
    #         exp[i] = ')'
    #
    #     elif exp[i] == ')':
    #         exp[i] = '('
    #
    #     else:
    #         continue


    # print(prefix)

    # postfix = Infix_to_Postfix(" ".join(exp))
    #
    # prefix = Infix_to_Postfix(exp).split(" ")[::-1]

    exp = exp.split(" ")[::-1]
    prefix = []
    exp_operator = Stack()
    operators = {'+', '-', '*', "/", '^', '(', ')'}
    precedence = {'(': 0, ')': 0, '^': 4, '*': 3, '/': 3, '+': 2, '-': 2}

    for element in exp:

        if element in operators:

            if element == "(":
                while exp_operator.top() != ")":
                    # print(exp_operator.stack)
                    prefix.append(exp_operator.pop())

                exp_operator.pop()

            elif element == ")":
                exp_operator.push(element)

            elif exp_operator.isEmpty():
                exp_operator.push(element)

            elif precedence[element] >= precedence[exp_operator.top()]:
                # print(exp_operator.stack)
                exp_operator.push(element)


            else:
                while precedence[element] < precedence[exp_operator.top()]:
                    # print(exp_operator.stack , element)
                    prefix.append(exp_operator.pop())

                exp_operator.push(element)


        else:
            prefix.append(element)



    while not exp_operator.isEmpty():

        op = exp_operator.pop()
        prefix.append(op)

    prefix = reversed(prefix)
    return " ".join(prefix)




def prefix_calculator(exp):

    operands = Stack()
    operators = {'+', '-', '*', '/', '^'}

    # Reverse the expression for prefix evaluation
    tokens = exp.split()[::-1]

    for token in tokens:
        if token not in operators:  # Operand
            operands.push(float(token))
        else:
            op1 = operands.pop()
            op2 = operands.pop()
            if op1 is None or op2 is None:
                raise ValueError("Insufficient operands for operator.")
            result = calculator(op1, op2, token)
            operands.push(result)

    return operands.top()


#######################################################################################################################
# def create_function(exp):
#     # create a function from a string expression
#     # def f(x):
#     #     return eval(input_str)
#     # return f
#     return lambda x: eval(exp)
#
#
# def process_expression(exp):
#     # plot the expression given as a string
#     x = np.linspace(-10, 10, 500)
#
#     # Define the function
#     func = create_function(exp)
#     y = func(x)
#
#     # Create the plot
#     plt.figure(figsize=(10, 5))
#     plt.plot(x, y, label="y = 2x²")
#     plt.title("Plot of y = 2x²")
#     plt.xlabel("x")
#     plt.ylabel("y")
#     plt.axhline(0, color='black', linewidth=0.8)
#     plt.axvline(0, color='black', linewidth=0.8)
#     plt.grid(color='gray', linestyle='--', linewidth=0.5)
#     plt.legend()
#     plt.show()
