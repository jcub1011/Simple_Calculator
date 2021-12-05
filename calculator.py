"""Calculator

Use calculator.Calculate(question:str)
to return the answer as a float or integer.
"""
__author__ = 'Jacob McCormack'

import decimal
import math


class UnknownItemError(Exception):
    """
    Raise when encountering an unknown operator.

    References:
        https://www.pythontutorial.net/python-oop/python-custom-exception/
    """

    def __init__(self, item):
        """
        :param item: The unknown item.
        """
        self.unk_item = item

    # def end

    def __str__(self):
        return f"Unknown item '{self.unk_item}'."
    # def end


# class end


class OperationError(Exception):
    """
    Raise when an operation fails.
    """

    def __init__(self, *args):
        """
        :param args: (item 1, item 2, operator)
        """
        self.items = args

    # def end

    def __str__(self):
        return f"Unable to perform '{self.items[2]}' on " \
               f"'{self.items[0]}' and '{self.items[1]}'."
    # def end


# class end


class MissingNumbersForOperation(Exception):
    """
    Raise when there are missing numbers for an operator.
    """

    def __init__(self, operator):
        """
        :param operator: The operator that doesn't have numbers to
        operate on.
        """
        self.operator = operator

    # def end

    def __str__(self):
        return f"Operator '{self.operator}' is missing numbers to operate on."
    # def end


# class end


class ParenthesesError(Exception):
    """
    Raise when parentheses is missing it's pair.
    """

    def __str__(self):
        return f"A parentheses is missing it's pair!"
    # def end


# class end


class EmptyStringError(Exception):
    """
    Raise when the question string has no characters.
    """

    def __str__(self):
        return f"Oops, you forgot to enter something to calculate."
    # def end


# class end


class Operations:
    """
    Where all the function operators are stored.
    Use 'Operations.function' to call it.
    """

    @staticmethod
    def multiply(first: float, second: float):
        """
        This returns the multiplication of the first by the second argument.

        :param first: The first number as a decimal.
        :param second: The second number as a decimal.
        :return: The result of multiplying the two decimals.
        """

        return first * second
        # * is the multiplication operator. It returns the result of
        # multiplying the first number to the second number

    # def end

    @staticmethod
    def divide(first, second):
        """
        This returns the division of the first by the second argument.

        :param first: The first number as a decimal.
        :param second: The second number as a decimal.
        :return: The result of multiplying the two decimals.
        """

        return first / second
        # / is the division operator. It returns the result of
        # dividing the first number by the second number.

    # def end

    @staticmethod
    def modulus(first, second):
        """
        This returns the modulus of the first by the second argument.

        :param first: The first number as a decimal.
        :param second: The second number as a decimal.
        :return: The remainder of dividing the two decimals.
        """

        return first % second
        # % is the modulus operator. It returns the remainder of dividing
        # the first number by the second number.

    # def end

    @staticmethod
    def subtract(first, second):
        """
        This returns the subtraction of the first by the second argument.

        :param first: The first number as a decimal.
        :param second: The second number as a decimal.
        :return: The result of multiplying the two decimals.
        """

        return first - second
        # - is the subtraction operator. It returns the result of
        # subtracting the second number from the first one.

    # def end

    @staticmethod
    def add(first, second):
        """
        This returns the addition of the first by the second argument.

        :param first: The first number as a decimal.
        :param second: The second number as a decimal.
        :return: The result of adding the two decimals.
        """

        return first + second
        # + is the addition operator. It returns the sum of the first and
        # second numbers.

    # def end

    @staticmethod
    def exponent(first, second):
        """
        This returns the result putting the first number
        to the exponent of the second number.

        References:
            https://stackoverflow.com/questions/63958582/convert-
            complex-strings-to-real-numbers

        :param first: The first number as a decimal.
        :param second: The second number as a decimal.
        :return: The result of putting the first to the exponent of the second.
        """

        try:
            return first ** second
            # ** is the exponent operator. It returns the first number to the
            # exponent of the second one.
        except decimal.InvalidOperation:
            # Handles what to do with complex numbers.
            result = float(first) ** float(second)

            result = complex(result).real

            return decimal.Decimal(result)
        # except end

    # def end

    @staticmethod
    def floor_division(first, second):
        """
        This returns the floor division of the first number
        by the second number.

        :param first: The first number as a decimal.
        :param second: The second number as a decimal.
        :return: The result of floor dividing the first number
        by the second number.
        """

        return first // second
        # // is the floor division operator. It returns only the integer
        # part of dividing the first number by the second
        # number by rounding down.

    # def end

    @staticmethod
    def factorial(first):
        """
        This returns the floor division of the first number
        by the second number.

        :param first: The first number as a decimal.
        :return: The result of factorial of a number.
        """

        return math.factorial(first)
        # // is the floor division operator. It returns only the integer
        # part of dividing the first number by the second
        # number by rounding down.

    # def end


# class end


class Calculate:
    """
    This class is the calculator class that I use to evaluate
    any sort of question the user might input.

    Calculate.(str) to call.
    Returns the answer as a float or int.

    References:
    https://www.w3schools.com/python/python_classes.asp
    https://www.w3schools.com/python/python_datatypes.asp
    https://stackoverflow.com/questions/9168340/
    using-a-dictionary-to-select-function-to-execute
    https://tutorialdeep.com/knowhow/check-data-type-python/
    """

    previous_answers = []
    # Used to store the results
    # from previous calculations.
    pemdas_operators = {"*", "^", "/",
                        "%", "+", "-",
                        ")", "(", "//",
                        "**", "cos", "sin", "tan", "!", "="}
    # This is a set of all the pemdas operators.
    emdas_operators = {"*", "^", "/",
                       "%", "+", "-",
                       "//", "**", "cos",
                       "sin", "tan", "!", "="}
    # This is a set of all the operators excluding parentheses.
    precedence_dict = {"^": 3, "**": 3, "*": 2, "/": 2,
                       "//": 2,
                       "%": 2, "+": 1, "-": 1,
                       "(": 0, ")": 0}
    # Originally named operator_precedence.
    # This is a dictionary with all the precedence values assigned.
    # To their respective keys (the operators).
    return_operation = {
        "*": Operations.multiply,
        "^": Operations.exponent,
        "**": Operations.exponent,
        "/": Operations.divide,
        "%": Operations.modulus,
        "+": Operations.add,
        "-": Operations.subtract,
        "//": Operations.floor_division
    }
    # Calls the functions in the operator class respective to the operator.
    numbers = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."}
    # This is a set of all the numbers.
    ignored_chars = {" ", ","}
    # This is a dictionary of all the operators
    is_operator = {
        "+": True,
        "-": True,
        "/": True,
        "(": True,
        ")": True,
        "*": True,
        "%": True,
        "#": True
    }

    def __init__(self, question_string):
        """
        This is applied to any object created under the Calculator
        class automatically. Self is the object itself which is passed
        by default unless I call a staticmethod.

        :param question_string: An infix question as a string.
        """

        # The ': str' in 'question_string: str' defines the
        # expected datatype of the parameter.
        self.operator_precedence = None
        self.operator_stack = None
        self.question_queue = None
        self.stack_precedence = None
        self.answer = None

        # All the steps are divided into different functions for
        # readability.
        try:
            question = question_string
            cleansed_question = self.clean_question(question)
            question_list = self.perform_question_separation_pass(
                cleansed_question)
            question_postfix = self.convert_to_postfix(question_list)
            answer = self.evaluate_question(question_postfix)
            self.answer = answer
        # try end
        except UnknownItemError as error:
            print(error)
        except OperationError as error:
            print(error)
        except MissingNumbersForOperation as error:
            print(error)
        except ParenthesesError as error:
            print(error)
        except decimal.DivisionByZero:
            print("Woah, division by zero is dangerous.")
        # except end
        except EmptyStringError as error:
            print(error)

    # def end

    @staticmethod
    def perform_question_cleanse_pass(question):
        """
        Cleans the question, removing unnecessary characters and
        adding 0's where necessary.

        :param question:
        """

        prev_char = None
        cleaned_question = ""

        for character in question:
            # Loops through the string.
            # If it encounters a minus or a plus that has no
            # number before it it inserts a zero so it doesn't
            # break the algorithm.
            if character == "-" or character == "+":
                if prev_char is None or prev_char == "(":
                    cleaned_question += f"0{character}"
                else:
                    cleaned_question += character
                # else end
                prev_char = character
            # if end
            elif character not in Calculate.ignored_chars:
                if character.isalpha():
                    # Deals with operators, variables, and parentheses.
                    if prev_char is not None:
                        if (character not in Calculate.emdas_operators and
                                prev_char.isnumeric()):
                            # Checks if the current character is a
                            # special operator and the previous
                            # character is a number.
                            cleaned_question += f"*{character}"
                        else:
                            cleaned_question += character
                            prev_char = character
                        # else end
                    else:
                        cleaned_question += character
                        prev_char = character
                    # else end
                else:
                    # Deals with numbers.
                    cleaned_question += character
                    prev_char = character
                # else end
            # elif end
        # for end

        if cleaned_question == "":
            raise EmptyStringError
        # if end

        return cleaned_question

    # def end

    @staticmethod
    def is_special_character(char):
        """
        Checks if a character is a special character.

        :param char: a single character.
        :return: Bool
        """

        if char == "=" or char == ".":
            return False

        elif ((char is not None) and (not char.isnumeric()) and
              (char not in Calculate.pemdas_operators)):
            return True

        else:
            return False
        # else end

    # def end

    @staticmethod
    def clean_question(question: str):
        """
        Returns a string that has all unnecessary characters removed
        and formatted for the text splitter.

        :param question: The question as a string.
        :return: str
        """

        prev_char = None
        cleaned_question = ""

        for character in question:
            # Loops through the question
            # with leading negatives and positives dealt with
            # and variables formatted (if they exist).

            if (character == "-" or character == "+") and prev_char is None:
                # Puts a zero in front of a negative or positive
                # if there isn't a number before it already.
                cleaned_question += f"0{character}"
                prev_char = character

            elif character.isnumeric() or character == ".":
                # Deals with numbers.

                if Calculate.is_special_character(prev_char):
                    # Checks if the previous character is a special operator.
                    cleaned_question += "$*"
                # if end

                if prev_char == ")":
                    # Puts a multiplication symbol if the previous character
                    # is a closed parentheses.
                    cleaned_question += f"*{character}"

                else:
                    cleaned_question += character
                # else end

                prev_char = character

            elif character not in Calculate.ignored_chars:
                # Deals with operators, variables, and parentheses.
                if character in Calculate.pemdas_operators:
                    # Deals with operators and parentheses.
                    if character == "(":
                        if Calculate.is_special_character(prev_char):
                            # If the previous character is a special one it
                            # appends the formatting identifier before
                            # continuing.
                            cleaned_question += f"$*{character}"

                        else:
                            cleaned_question += character
                        # else end

                        prev_char = None

                    elif character == ")":
                        cleaned_question += character
                        prev_char = character

                    else:
                        # Deals with operators.
                        if prev_char is None:
                            raise ValueError(f"Error: '{character}' is " +
                                             f"operating on nothing.")
                        else:
                            if prev_char.isalpha():
                                # If the previous character is a special one
                                # it inserts the formatting identifier
                                # before the operator itself.
                                cleaned_question += "$"
                            # if end

                            cleaned_question += character
                            prev_char = character
                        # else end
                    # else end
                else:
                    # Deals with special operators and variables.
                    if prev_char is not None:
                        if prev_char.isnumeric() or prev_char == ")":
                            # If the previous character is a number
                            # or a closed parentheses.
                            cleaned_question += "*"
                        # if end

                        if prev_char.isalpha():
                            # If it's another special character.
                            cleaned_question += character

                        else:
                            # Otherwise it inserts the formatting identifier.
                            cleaned_question += f"${character}"
                        # else end

                    else:
                        # If it is none it just inserts the formatting
                        # identifier.
                        cleaned_question += f"${character}"
                    # else end

                    prev_char = character
                # else end

            # elif end
        # for end
        if Calculate.is_special_character(prev_char):
            cleaned_question += "$"
        # if end

        final_cleanse = Calculate.deal_with_special_items(cleaned_question)

        return final_cleanse

    # def end

    @staticmethod
    def deal_with_special_items(question: str):
        """
        Figures out what to do with the special operators.

        :param question: The question string that has already
            been put through the question cleanser.
        :return: The new string properly formatted.
        """

        formatted_question = ""

        while len(question) > 0:
            if question[0] == "$":
                # Deals with the dollar signs.
                question = question[1:]
                special_item = ""
                while question[0] != "$":
                    special_item += question[0]
                    question = question[1:]
                # while end

                question = question[1:]
                # Deletes the first character in the string.

                if special_item in Calculate.emdas_operators:
                    formatted_question += special_item
                    if len(question) > 0:
                        question = question[1:]
                    # if end

                else:
                    if len(special_item) == 1:
                        formatted_question += special_item
                    else:
                        formatted_question += special_item[0]
                        special_item = special_item[1:]

                        for variable in special_item:
                            formatted_question += f"*{variable}"
                        # for end
                    # else end

                # else end

            else:
                formatted_question += question[0]
                question = question[1:]
                # Un-enqueues the item from question
                # and queues it in formatted question.
            # else end

        # while end
        return formatted_question

    # def end

    @staticmethod
    def append_item(item, question):
        """Attempts to append the item to the list."""

        if len(item) > 0:
            question.append(item)
        # if end
        return "", question

    # def end

    @staticmethod
    def append_number(number, question, precision):
        """Attempts to append the number to the list."""

        if len(number) > 0:
            if precision:
                question.append(decimal.Decimal(number))
            else:
                question.append(float(number))
            # else end
        # if end
        return "", question

    # def end

    @staticmethod
    def perform_question_separation_pass(question, precision=True):
        """
        Separates the question into a list of Decimals and operators.

        :param question: The question being worked on as a string.
        :param precision: If True it uses the decimal module and skips
        checking for a special operator at the end of the separation pass.
        """

        # KNOWN BUG: Can't tell that "x sin" is
        # x*sin rather than "xsin".

        special_operator = ""
        operator = ""
        number = ""
        question_string = question
        question = []

        for item in question_string:
            if item.isnumeric() or item == ".":
                # Checks if there are items in the operator or special_operator
                # strings and appends them before dealing with the new item.
                operator, question = Calculate.append_item(operator,
                                                           question)
                special_operator, question = (
                    Calculate.append_item(special_operator, question))

                number = Calculate.combine(number, item)
            # if end

            elif item in Calculate.emdas_operators:
                number, question = Calculate.append_number(number,
                                                           question,
                                                           precision)
                special_operator, question = (
                    Calculate.append_item(special_operator, question))

                operator = Calculate.combine(operator, item)
            # elif end

            elif item.isalpha():
                number, question = Calculate.append_number(number,
                                                           question,
                                                           precision)
                operator, question = Calculate.append_item(operator, question)

                special_operator = Calculate.combine(special_operator,
                                                     item)
            # elif end

            else:
                # Only parentheses can reach here.
                number, question = Calculate.append_number(number,
                                                           question,
                                                           precision)
                operator, question = Calculate.append_item(operator, question)

                special_operator, question = Calculate.append_item(
                    special_operator, question)

                question.append(item)
            # else end
        # for end

        if number != "":
            # It didn't check for any operators because if the operator
            # doesn't have a number after it it would cause an error anyways.
            if precision:
                question.append(decimal.Decimal(number))
            else:
                question.append(float(number))
            # else end
        # if end

        if not precision:
            if special_operator != "":
                question.append(special_operator)
            # if end
        # if end

        return question

    # def end

    @staticmethod
    def convert_to_postfix(question: list):
        """
        This converts an infix question into a postfix expression.

        An infix expression is how people normally write out
        expressions. ex: '(100 + 20) * 10'
        A postfix expression is a lot easier to work with when
        it comes to evaluating expressions via computer.
        ex: [100, 20, +, 10, *]

        Uses the shunting yard algorithm to convert.

        :param question: The question in infix notation.
        :return: The question list in postfix notation.

        References:
        https://www.youtube.com/watch?v=Wz85Hiwi5MY
        https://www.youtube.com/watch?v=bebqXO8H4eA
        https://www.pythonforbeginners.com/basics/decimal-module-in-python
        """

        stack_precedence = -1
        operator_stack = []
        question_queue = []

        for item in question:
            operator_precedence = (
                Calculate.precedence_dict.get(item)
            )

            if type(operator_precedence) is int:
                # Checks if the precedence_dict.get returned a number or None.
                # Only operators will return a number.
                stack_precedence, operator_stack, question_queue = (
                    Calculate.handle_operator(item, stack_precedence,
                                              operator_stack, question_queue,
                                              operator_precedence))
            else:
                question_queue.append(item)
            # else end
        # for end

        operator_stack.reverse()
        # Reverses the stack before combining because the stack is LIFO.
        question_queue += operator_stack
        return question_queue

    # def end

    @staticmethod
    def handle_operator(item, stack_precedence,
                        operator_stack, question_queue,
                        operator_precedence):
        """
        Handles what to do with operators.

        :param item: The operator.
        :param stack_precedence: The precedence of the stack.
        :param operator_stack: The current operator stack.
        :param question_queue: The current question queue.
        :param operator_precedence: The precedence of the current item.
        """

        if item == "(":
            operator_stack.append(item)
            stack_precedence = Calculate.precedence_dict["("]

        elif item == ")":
            try:
                top_of_stack = operator_stack[-1]
                while top_of_stack != "(":
                    question_queue.append(top_of_stack)
                    operator_stack.pop()
                    top_of_stack = operator_stack[-1]
                # while end

                operator_stack.pop()

                if len(operator_stack) > 0:
                    top_of_stack = operator_stack[-1]
                    stack_precedence = (
                        Calculate.precedence_dict[top_of_stack]
                    )

                else:
                    stack_precedence = -1
                # else end
            except IndexError:
                raise ParenthesesError
            # except end
        else:
            if operator_precedence > stack_precedence:
                # Operators with higher precedence are appended.
                stack_precedence = Calculate.precedence_dict[item]
                operator_stack.append(item)

            elif operator_precedence < stack_precedence:
                # If it encounters an operator with lower precedence it
                # pops the stack to the queue till it reaches a
                # closed parentheses.
                stack_precedence = Calculate.precedence_dict[item]
                while (len(operator_stack) > 0 and
                       operator_stack[-1] != "("):
                    question_queue.append(operator_stack[-1])
                    operator_stack.pop()
                # while end

                operator_stack.append(item)
            else:
                # If it encounters something with the same precedence
                # it pops the top of stack to the queue before pushing the new
                # operator.
                if Calculate.precedence_dict[item] == 3:
                    # Exponents are kept in the stack because the are
                    # read from left to right in order to keep
                    # order of operations.
                    operator_stack.append(item)
                else:
                    question_queue.append(operator_stack[-1])
                    operator_stack.pop()
                    operator_stack.append(item)
                # else end
            # else end
        # else end

        return stack_precedence, operator_stack, question_queue

    # def end

    @staticmethod
    def evaluate_question(question: list):
        """
        This takes a parsed question and returns the answer.

        :param question: The question in postfix notation.
        :return: A float or integer of the result.

        References:
            https://www.youtube.com/watch?v=Wz85Hiwi5MY
            https://www.youtube.com/watch?v=bebqXO8H4eA
        """

        question_stack = []
        while len(question) > 0:
            first_num = None
            second_num = None
            current_item = None

            try:
                current_item = question[0]

                if current_item not in Calculate.emdas_operators:
                    question_stack.append(current_item)
                else:
                    first_num = question_stack[-2]
                    second_num = question_stack[-1]

                    result = Calculate.return_operation[current_item](
                        first_num, second_num)

                    for i in range(2):
                        question_stack.pop()
                    # for end

                    question_stack.append(result)
                # else end

                question = question[1:]
            # try end
            except IndexError:
                raise MissingNumbersForOperation(current_item)
            except TypeError:
                raise OperationError(first_num, second_num, current_item)
            # except end
        # while end

        question = question_stack[0]
        try:
            if type(question) is complex:
                return question
            elif int(question) < question:
                question = float(question)
            else:
                question = int(question)
            # else end
        except ValueError:
            print(f"Sorry, I don't know what to do with " +
                  f"'{question}'.")
            question = None

        return question

    # def end

    @staticmethod
    def combine(item, other_item):
        """
        Combines item with other_item.

        :param item: The several item string.
        :param other_item: The individual character.
        :return: The combined item.
        """

        item += other_item
        return item
    # def end

# class end
