"""Calculator

Use calculator.Calculate(question:str)
to return the answer as a float or integer.
"""
__author__ = 'Jacob McCormack'

import decimal


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

        :param first: The first number as a decimal.
        :param second: The second number as a decimal.
        :return: The result of putting the first to the exponent of the second.
        """

        return first ** second
        # ** is the exponent operator. It returns the first number to the
        # exponent of the second one.

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
                        "**"}
    # This is a set of all the pemdas operators.
    emdas_operators = {"*", "^", "/",
                       "%", "+", "-",
                       "//", "**"}
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
        "#": Operations.floor_division,
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

        # All the steps are divided into different functions for
        # readability.
        self.question = question_string
        self.perform_question_cleanse_pass()
        self.perform_question_separation_pass()
        self.convert_to_postfix()
        self.evaluate_question()
        # print(f"The answer: {self.question}")
        self.answer = self.question

    # def end

    def perform_question_cleanse_pass(self):
        """
        Cleans the question, removing unnecessary characters and
        adding 0's where necessary.
        """

        prev_char = None
        cleaned_question = ""

        for character in self.question:
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
            # if end
            elif character not in self.ignored_chars:
                cleaned_question += character
                prev_char = character
            # elif end
        # for end

        self.question = cleaned_question

    # def end

    def append_item(self, item):
        """
        Attempts to append the item to the list.
        """

        if len(item) > 0:
            self.question.append(item)
        # if end
        return ""
    # def end

    def perform_question_separation_pass(self):
        """
        Separates the question into a list of Decimals and operators.
        """

        special_operator = ""
        operator = ""
        number = ""
        question_string = self.question
        self.question = []

        for item in question_string:
            if item.isnumeric() or item == ".":
                # Checks if there are items in the operator or special_operator
                # strings and appends them before dealing with the new item.
                operator = self.append_item(operator)
                special_operator = self.append_item(special_operator)

                number = self.combine(number, item)
            # if end

            elif item in self.emdas_operators:
                if len(number) > 0:
                    self.question.append(decimal.Decimal(number))
                    number = ""
                # if end

                operator = self.combine(operator, item)
            # elif end

            elif item.isalpha():
                if len(number) > 0:
                    self.question.append(decimal.Decimal(number))
                    number = ""
                # if end
                operator = self.append_item(operator)

                special_operator = self.combine(special_operator, item)
            # elif end

            else:
                # Only parentheses can reach here.
                if len(number) > 0:
                    self.question.append(decimal.Decimal(number))
                    number = ""
                # if end
                operator = self.append_item(operator)
                special_operator = self.append_item(special_operator)

                self.question.append(item)
            # else end
        # for end

        if number != "":
            # It didn't check for any operators because if the operator
            # doesn't have a number after it it would cause an error anyways.
            self.question.append(decimal.Decimal(number))
        # if end

    # def end

    def convert_to_postfix(self):
        """
        This converts an infix question into a postfix expression.

        An infix expression is how people normally write out
        expressions. ex: '(100 + 20) * 10'
        A postfix expression is a lot easier to work with when
        it comes to evaluating expressions via computer.
        ex: [100, 20, +, 10, *]

        Uses the shunting yard algorithm to convert.

        References:
        https://www.youtube.com/watch?v=Wz85Hiwi5MY
        https://www.youtube.com/watch?v=bebqXO8H4eA
        https://www.pythonforbeginners.com/basics/decimal-module-in-python
        """

        self.stack_precedence = -1
        self.operator_stack = []
        self.question_queue = []

        for item in self.question:
            self.operator_precedence = (
                self.precedence_dict.get(item)
            )

            if type(self.operator_precedence) is int:
                # Checks if the precedence_dict.get returned a number or None.
                # Only operators will return a number.
                self.handle_operator(item)
            else:
                self.question_queue.append(item)
            # else end
        # for end

        self.operator_stack.reverse()
        # Reverses the stack before combining because the stack is LIFO.
        self.question_queue += self.operator_stack
        self.question = self.question_queue

    # def end

    def handle_operator(self, item):
        """
        Handles what to do with operators.

        :param item: The operator.
        """

        if item == "(":
            self.operator_stack.append(item)
            self.stack_precedence = self.precedence_dict["("]

        elif item == ")":
            try:
                top_of_stack = self.operator_stack[-1]
                while top_of_stack != "(":
                    self.question_queue.append(top_of_stack)
                    self.operator_stack.pop()
                    top_of_stack = self.operator_stack[-1]
                # while end

                self.operator_stack.pop()

                if len(self.operator_stack) > 0:
                    top_of_stack = self.operator_stack[-1]
                    self.stack_precedence = (
                        self.precedence_dict[top_of_stack]
                    )

                else:
                    self.stack_precedence = -1
                # else end
            except IndexError:
                print("Uh oh, one of your parentheses is missing it's pair!")
                self.question = None
                return
            # except end
        else:
            if self.operator_precedence > self.stack_precedence:
                # Operators with higher precedence are appended.
                self.stack_precedence = self.precedence_dict[item]
                self.operator_stack.append(item)

            elif self.operator_precedence < self.stack_precedence:
                # If it encounters an operator with lower precedence it
                # pops the stack to the queue till it reaches a
                # closed parentheses.
                self.stack_precedence = self.precedence_dict[item]
                while (len(self.operator_stack) > 0 and
                       self.operator_stack[-1] != "("):
                    self.question_queue.append(self.operator_stack[-1])
                    self.operator_stack.pop()
                # while end

                self.stack_precedence = self.precedence_dict[item]
                self.operator_stack.append(item)
            else:
                # If it encounters something with the same precedence
                # it pops the top of stack to the queue before pushing the new
                # operator.
                if self.precedence_dict[item] == 3:
                    # Exponents are kept in the stack because the are
                    # read from left to right in order to keep
                    # order of operations.
                    self.operator_stack.append(item)
                else:
                    self.question_queue.append(self.operator_stack[-1])
                    self.operator_stack.pop()
                    self.operator_stack.append(item)
                # else end
            # else end
        # else end

    # def end

    def evaluate_question(self):
        """
        This takes a parsed question and returns the answer.

        References:
        https://www.youtube.com/watch?v=Wz85Hiwi5MY
        https://www.youtube.com/watch?v=bebqXO8H4eA
        """

        question_stack = []

        while len(self.question) > 0:
            current_item = self.question[0]

            if current_item not in self.emdas_operators:
                question_stack.append(current_item)
            else:
                first_num = question_stack[-2]
                second_num = question_stack[-1]
                result = self.return_operation[current_item](
                    first_num, second_num)

                for i in range(2):
                    question_stack.pop()
                # for end
                question_stack.append(result)
            # else end

            self.question = self.question[1:]
        # while end

        self.question = question_stack[0]
        try:
            if int(self.question) < self.question:
                self.question = float(self.question)
            else:
                self.question = int(self.question)
            # else end
        except ValueError:
            print(f"Sorry, I don't know what to do with " +
                  f"'{self.question}'.")
            self.question = None
        # except end

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
