"""
My Graphing Calculator

Graphs a function.
"""

__author__ = "Jacob McCormack"

import math
import calculator

"""
Returns a string with a formatted graph in it.
"""


def main():
    """Main function."""
    parse_function("y=2x+8",  # input("Input function here: "),
                   "x")  # input("Input variable used here: "))


# def end


def parse_function(function, variable):
    """
    Parses the infix function.
    :param function: The function being parsed.
    :param variable: The variable that is being used in the function.
    :return: None.
    """

    function_parsed = calculator.Calculate(function, True)
    function_parsed.perform_question_cleanse_pass()
    function_parsed.perform_question_separation_pass(False)
    function_parsed.convert_to_postfix()

    print(function_parsed.question)


# def end


if __name__ == '__main__':
    main()
# if end
