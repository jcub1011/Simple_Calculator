"""My Integration Project"""
__author__ = 'Jacob McCormack'

import time
import decimal

# import math
"""
My project is a nifty calculator. Eventually it will do other things.
"""


def main():
    """
    Main is the function that starts the project. It is only called if
    the project is loaded directly, otherwise main must be called
    manually which is only necessary during import.
    """
    try:
        print("Let me load your preferences really quick. ", end="")
        Pref.load_preferences()
        Pref.pref["ask_new_question"] = True
        print("There you go!")
    # try end
    except FileNotFoundError:
        print("\nOops, looks like you don't " +
              "have a preference file just yet.")
        # The + on strings concatenates them.
        Pref.handle_load_error()
        print("I generated a new one for you!")
    # except end
    print()

    print("Welcome to Jacob's Calculator!")
    print("Type 'help' for more information.")
    print("Type 'stop' if you'd like to exit the program.")
    print("Note: exclude the quotes when issuing commands.")
    print()
    print("Start typing math questions below if you just want to "
          "calculate.")
    print("_" * 100)
    # The * on a string repeats whatever is in the string
    # the number of times indicated after the * symbol.

    if Pref.pref["test_code"]:
        timer = Debug()
        timer.start_timer(True)
        test_values = [
            "2+10-2^(5-3)+7-2*2+6/3+5%4+5//2",  # Should equal 16
            "2+10-2^(5-3)+7-2*2+6/3",  # Should equal 13
            "30-10^(20-18+2*1)+16/(2*2)*2+10*(4+6)",  # Should equal -9862
            "3+4*2/((1-5)^2^3)",  # Should equal 3.0001220703125
            "3.2+8",  # should equal 11.2
            "(     1 + 1          )) ",  # Should be error.
            "(     1 + 1           ",  # Should equal 2
            # "1*sin(6)+6* 8 cos(5)",
            "8*2",  # Should equal 16
            "-10+2",  # Should equal -8
            "-1+8 - (-1+2)-0"  # Should equal 6
        ]
        for test_value in test_values:
            print("-" * 10, "New Question", "-" * 10)
            Calculator(test_value)
        # for end
        timer.stop_timer()
    # if end

    while Pref.pref["ask_new_question"]:
        question = input().lower()
        # .lower() converts all the characters of a string into
        # lower cased letters.
        if is_calculator_question(question):
            Calculator(question)
        # if end
        else:
            Respond(question)
        # else end
    # while end


# def end


def is_calculator_question(question: str):
    """
    Checks if the given string is a calculator question or not.

    A calculator question is any question that has at least one number.
    :param question: String.
    :return: Boolean.
    """
    for character in question:
        if character.isnumeric():
            # isnumeric is a variation of isalpha that returns true
            # if the character is a number.
            return True
        # if end
    # for end


# def end


class Pref:
    """
    This contains all the preference data.
    """
    pref = {
        "debugging": False,
        "test_code": False,
        "performance_stats": False,
        "ask_new_question": True
    }
    # These are the default values.
    pref_length = len(pref)

    @staticmethod
    def load_preferences():
        """
        Handles the preferences.txt file.

        References:
        https://www.datacamp.com/community/tutorials/
        reading-writing-files-python
        https://devenum.com/how-to-convert-text-file-to-a-dictionary-in-python/
        https://codefather.tech/blog/python-with-open/
        """
        try:
            with open("preferences.txt", "r") as preferences:
                # With is a context manager that automatically closes
                # the file when it's finished with.
                # As preferences is the same as
                # preferences = open("file", "r")
                line_count = 0
                for line in preferences:
                    print(".", end=" ")
                    line = line.rstrip()
                    # rstrip() removes the extra characters.
                    key, value = line.split("=", 1)
                    # .split splits the string according to the argument
                    # given and the second argument is the number
                    # of splits.
                    # The comma is for unpacking and allows for multiple
                    # variable to be assigned at once.

                    if value == "True":
                        value = True
                    # if end
                    else:
                        value = False
                        # else
                    # if end

                    Pref.pref[key] = value
                    # Updates the dictionary values.
                    line_count += 1
                # for end
            # with end
        # try end
        except ValueError:
            # If there is a value error that means
            # an = sign is missing from one of the lines in the file
            print("\nUh oh, your preference file was damaged. Poor thing...\n"
                  "Using defaults instead.")
            Pref.handle_load_error()
            return
        # except end

        # with end
        if line_count != Pref.pref_length:
            # If lines are missing or there are too many it rewrites the file.
            print("\nUh oh, your preference file was damaged. Poor thing.\n"
                  "Using defaults instead.")
            Pref.handle_load_error()
            return
        # if end

    # def end

    @staticmethod
    def handle_load_error():
        """
        Handles what to do if loading the file doesn't exist.

        References:
        https://www.datacamp.com/community/
        tutorials/reading-writing-files-python
        """
        with open("preferences.txt", "w") as preferences:
            for key in Pref.pref:
                preferences.write(f"{key}={Pref.pref[key]}\n")
            # for end
        # with end

    # def end

    @staticmethod
    def update_preference(key, value):
        """
        Updates the preference as defined by key to true or false.

        :param key: The value to update.
        :param value: What to update the value to. Either True or False.
        """
        print("Updating preference .", end=" ")
        found_key = False
        converted_value = SaveData.convert_from_string(value)

        if type(converted_value) is bool:
            Pref.pref[key] = converted_value
            with open("preferences.txt", "r") as preferences:
                preference_list = preferences.readlines()
            # with end

            for index, line in enumerate(preference_list):
                line = line.rstrip()
                key_in_file, value_in_file = line.split("=", 1)

                if key == key_in_file:
                    preference_list[index] = f"{key}={value}\n"
                    found_key = True
                    break
                # if end
                print(".", end=" ")
            # for end

            if found_key:
                with open("preferences.txt", "w") as preferences:
                    preferences.writelines(preference_list)
                # with close
            # if end
            else:
                Debug.print("Error: Preference doesn't exist!")
            # else end
        else:
            Debug.print("Invalid assignment!")
        # else end
    # def end


# class


class SaveData:
    """
    Holds all the game save data.
    #TODO: Actually implement.
    """
    save_data = {}

    @staticmethod
    def convert_from_string(value: str):
        """
        Attempts to convert a string to a bool, float, integer, or string.

        :param value: The value to convert.
        :return: The converted value.
        """
        value = str(value)
        if value == "False":
            value = False
            Debug.print("Value is a Bool.")
        # if end
        elif value == "True":
            value = True
            Debug.print("Value is a bool.")
        # elif end
        else:
            try:
                value = float(value)
                if int(value) == value:
                    # Converts to integer if the float
                    # is the same as the integer version.
                    value = int(value)
                # if end
                Debug.print("Value is a number.")
            # try end
            except ValueError:
                Debug.print("Value is a string.")
            # except end
        # else end
        return value

    # def end

    def load_save(self):
        """
        Attempts to retrieve game save data.
        """
        try:
            with open("save_data.txt", "r") as save:
                for line in save:
                    line = line.rstrip()
                    key, value = line.split("=", 1)

                    self.save_data[key] = self.convert_from_string(value)
                # for end
                Debug.print(f"Loaded save data:\n{self.save_data}")
            # with end
        # try end
        except FileNotFoundError:
            Debug.print("Save file doesn't exist.")
            self.create_save()
        # except end
        except ValueError:
            Debug.print("End of file.")
        # except end

    # def end

    def create_save(self):
        """
        Used to create a new save file.
        """
        self.save_data = {
            "runs": 1,
            "asked_for_help": False
        }

        with open("save_data.txt", "w") as save:
            for key in self.save_data:
                save.write(f"{key}={str(self.save_data[key])}\n")
            # for end
            Debug.print(f"New save data:\n{self.save_data}")
        # with end

    # def end

    def update_save_data(self, key, value):
        """
        Used to update any given key.

        References:
        https://stackoverflow.com/questions/4719438/
        editing-specific-line-in-text-file-in-python

        :param key: The key of the value to update.
        :param value: The value to update to.
        """
        key = str(key).lower()
        value = str(value).lower().capitalize()
        self.save_data[key] = self.convert_from_string(value)

        print("Saving .", end=" ")

        with open("save_data.txt", "r") as save:
            save_data = save.readlines()
        # with end

        found_line = False
        for index, line in enumerate(save_data):
            # Enumerate gives each element an index.
            line = line.rstrip()
            key_in_file, value_in_file = line.split("=", 1)

            print(".", end=" ")
            if key_in_file == str(key):
                # Checks if the keys match.
                found_line = True

                save_data[index] = f"{key}={value}\n"
                break
            # if end
        # for end
        if found_line:
            # If the key was found it will update it.
            with open("save_data.txt", "w") as save:
                save.writelines(save_data)
            # with close
        # if end
        else:
            # Otherwise it creates a new key value pair.
            with open("save_data.txt", "a") as save:
                save.write(f"{key}={value}")
            # with end
        # else end
        print()
    # def end


# class end


class Debug:
    """
    Contains all the debugging functions.
    Set debugging to False to turn off and True to turn on.
    """

    def __init__(self):
        self.start = None
        self.end = None
        self.use_milliseconds = None

    # def end

    @staticmethod
    def print(text):
        """
        Just like a normal print statement.
        :param text: The text to print.
        """
        if Pref.pref["debugging"]:
            print(text)
        # if end
        # Debug.print() << Copy and paste

    # def end

    def start_timer(self, in_milliseconds=False):
        """
        Starts a timer with ns precision.
        The =False just makes the default value of in_seconds False.
        """
        self.start = time.perf_counter_ns()
        self.use_milliseconds = in_milliseconds

    # def end

    def stop_timer(self):
        """
        Ends a timer.

        References:
        https://www.w3schools.com/python/gloss_python_object_delete.asp
        https://cis.bentley.edu/sandbox/wp-content
        /uploads/Documentation-on-f-strings.pdf
        """
        self.end = time.perf_counter_ns()
        if Pref.pref["performance_stats"]:
            if self.use_milliseconds:
                self.start /= 1000000
                self.end /= 1000000
                print(f"Took {self.end - self.start:0.2f}ms to complete.")
            # if end
            else:
                print(f"Took {self.end - self.start}ns to complete.")
            # else end
        # if end
        del self  # This deletes the timer to save memory.
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


class Calculator:
    """
    This class is the calculator class that I use to evaluate
    any sort of question the user might input.

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
                        ")", "(", "//"}
    # This is a set of all the pemdas operators.
    emdas_operators = {"*", "^", "/",
                       "%", "+", "-",
                       "//"}
    # This is a set of all the operators excluding parentheses.
    operator_precedence = {"^": 3, "*": 2, "/": 2,
                           "//": 2,
                           "%": 2, "+": 1, "-": 1,
                           "(": 0, ")": 0}
    # This is a dictionary with all the precedence values assigned.
    # To their respective keys (the operators).
    numbers = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."}
    # This is a set of all the numbers.
    ignored_chars = {" ", ","}

    def __init__(self, question_string: str):
        """
        This is applied to any object created under the Calculator
        class automatically. Self is the object itself which is passed
        by default unless I call a staticmethod.
        :param question_string: An infix question as a string.
        """
        # The ': str' in 'question_string: str' defines the
        # expected datatype of the parameter.
        Debug.print(f"Your question:\n{question_string}")
        self.operator_precedence = None
        self.special_item = None
        self.operator_stack = None
        self.question_queue = None
        self.stack_precedence = None
        self.prev_item = None
        self.return_operation = {
            "*": Operations.multiply,
            "^": Operations.exponent,
            "/": Operations.divide,
            "%": Operations.modulus,
            "+": Operations.add,
            "-": Operations.subtract,
            "#": Operations.floor_division,
            "//": Operations.floor_division
        }
        self.question = question_string
        self.question_list = self.parse_question()
        if self.question_list is not None:
            Debug.print("-" * 20 + "Starting Evaluation" + "-" * 20)
            self.answer = self.evaluate_question(self.question_list)
            print(f"Answer:\n{self.answer}")
        # if end

    # def end

    @staticmethod
    def are_same_type(item_1, item_2):
        """
        Checks if item one is the same type as item two.
        :param item_1: The first item.
        :param item_2: The second item
        :return: True if they are and false if they aren't.
        """
        item_1_is_number = False
        item_2_is_number = False
        # Assigns the is_number value to false by default.
        if item_1 in Calculator.numbers:
            item_1_is_number = True
            # If item_1 is a number it sets it's is_number value to True.
        # if end
        if item_2 in Calculator.numbers:
            item_2_is_number = True
            # If item_2 is a number it sets it's is_number value to True.
        # elif end
        if item_1_is_number == item_2_is_number:
            # If the is_number value of both items are the same it returns
            # true otherwise it returns false.
            return True
        # if end
        else:
            return False
        # else end

    def handle_operator(self, item):
        """
        This handles what to do with operators.

        :param item: Operator to be pushed to the stack.
        :return: None.
        """
        Debug.print(f"Current item: '{item}' is an operator.")
        if self.operator_precedence > self.stack_precedence:
            # This checks if the precedence of the item is greater
            # than the precedence of the top item in the stack.
            Debug.print("Current operator has greater precedence " +
                        "than operator in stack.")
            self.operator_stack.append(item)
            Debug.print(f"New Stack:\n{self.operator_stack}")
            Debug.print(f"Current Queue:\n{self.question_queue}")
        # if end
        elif self.operator_precedence < self.stack_precedence:
            Debug.print("Current operator has lower precedence " +
                        "than the operator in the stack.")
            while (len(self.operator_stack) > 0 and
                   self.operator_stack[-1] != "("):
                # This pops the stack and enqueues them
                # to the queue until it reaches an open parentheses
                # or the end of the stack.
                self.question_queue.append(self.operator_stack[-1])
                self.operator_stack.pop()
            # while end
            self.operator_stack.append(item)
            Debug.print(f"New Stack:\n{self.operator_stack}\n"
                        f"New Queue:\n{self.question_queue}")
        # elif end
        else:
            # If it reaches this point
            # that means the precedences match.
            if self.operator_precedence == 3:
                Debug.print(f"Current operator has the same precedence " +
                            f"but is an exponent.")
                self.operator_stack.append(item)
                # Exponents are a special case. They need to be kept together
                # in cases like 2^2^2 because if they aren't the postfix
                # becomes 22^2^ which will return the incorrect value
                # as opposed to 222^^.
            # if end
            else:
                Debug.print(f"Current operator has the same precedence " +
                            f"as the operator in the stack.")
                Debug.print(f"Current stack:\n{self.operator_stack}")
                self.question_queue.append(self.operator_stack[-1])
                self.operator_stack.pop()
                self.operator_stack.append(item)
                # This pops the top of the stack and enqueues it
                # to the question_queue then pushes the new operator
                # to the stack.
            # else end
            Debug.print(f"Pushed '{item}' to stack.\n"
                        f"New Stack:\n{self.operator_stack}\n"
                        f"New Queue:\n{self.question_queue}")
        # else end
        self.stack_precedence = self.operator_precedence
        # This updates the precedence of the stack as the operator
        # was pushed to it.

    # def end

    def clean_question(self):
        """
        This removes items defined by Calculator.ignored_chars.

        :return: None
        """
        cleaned_question = ""
        prev_item = None
        for item in self.question:
            if item == "-" or item == "+":
                if prev_item is None or prev_item == "(":
                    # Checks if the previous item is None or an open
                    # parentheses.
                    cleaned_question += "0"
                # if end
            # if end
            if item not in Calculator.ignored_chars:
                # If the item isn't being ignored
                # it adds it to the new question.
                cleaned_question += item
                prev_item = item
            # if end
        # for end
        self.question = cleaned_question

    # def end

    def conv_spec_item_to_num(self):
        """
        Converts the special item to a number

        :return: "error" if there is an error.
        """
        try:
            self.question_queue.append(
                decimal.Decimal(self.special_item)
            )
        # try end
        except decimal.InvalidOperation:
            # This is a custom error defined by the decimal
            # module.
            print(f"Error: unknown item '{self.special_item}'")
            return "error"
        # except end

    # def end

    def parse_question(self):
        """
        This converts an infix question into a postfix expression.

        An infix expression is how people normally write out
        expressions. ex: '(100 + 20) * 10'
        A postfix expression is a lot easier to work with when
        it comes to evaluating expressions via computer.
        ex: [100, 20, +, 10, *]

        References:
        https://www.youtube.com/watch?v=Wz85Hiwi5MY
        https://www.youtube.com/watch?v=bebqXO8H4eA
        https://www.pythonforbeginners.com/basics/decimal-module-in-python

        :return: A postfix expression as a list.
        """
        self.clean_question()
        Debug.print(f"Cleaned question:\n{self.question}")
        self.stack_precedence = -1
        # This what operator happens first according to pemdas.
        # ex. 1+5*2: you would multiply 5 and 2 before adding 1
        # so multiplication has a higher precedence.
        self.prev_item = None
        # This keeps track of what the last item was
        self.operator_stack = []
        # This is a stack of all the operators. A stack is a LIFO
        # data structure where the last item pushed onto it is the
        # first item popped.
        self.question_queue = []
        # This is a queue of operations and the question itself.
        # A queue is a FIFO data structure where the first item
        # enqueued is the first item to be dequeued.
        self.special_item = None
        # This stores characters in the hopes that they eventually
        # combine and form a special operator like sin, cos, tan, etc...
        # or a several character number.
        for item in self.question:
            # This iterates through the question.
            # Element is the current element in the question
            # that is being evaluated and question is the string.
            self.operator_precedence = Calculator.operator_precedence.get(item)
            # Get is a dictionary method. It attempts to return the value
            # pair with the given key and if the key doesn't exist, it returns
            # None.
            if item in Calculator.emdas_operators:
                # Checks if the item in an operator excluding parentheses.
                if self.prev_item in Calculator.emdas_operators:
                    Debug.print(f"Previous item '{self.prev_item}' and "
                                f"current item '{item}' are both operators.\n"
                                f"Combined operators.")
                    self.operator_stack[-1] += item
                    Debug.print(f"New Stack:\n{self.operator_stack}\n"
                                f"New Queue:\n{self.question_queue}")
                    # This combines the operators if they are right next to
                    # each other.
                # if end
                else:
                    if self.special_item is not None:
                        # If there is something in special item it enqueues it
                        # before handling the next operator.
                        if self.conv_spec_item_to_num() == "error":
                            return None
                        # if end
                        Debug.print(f"Enqueued special item because " +
                                    f"next item is an operator.\n" +
                                    f"New Queue:\n{self.question_queue}")
                        self.special_item = None
                        # This appends the special item and clears it.
                    self.handle_operator(item)
                # else end
            # if end
            elif item == "(":
                # Checks if the item is an open parentheses.
                Debug.print("Current item is '('.")
                self.operator_stack.append(item)
                self.stack_precedence = self.operator_precedence
                Debug.print(f"Pushed '{item}' to stack.\n"
                            f"New Stack:\n{self.operator_stack}\n"
                            f"New Queue:\n{self.question_queue}")
            # elif end
            elif item == ")":
                # Checks if the item in an open parentheses.
                Debug.print(f"Current item is a closed parentheses.")
                Debug.print(f"Enqueued special item first: "
                            f"{self.special_item}")
                if self.special_item is not None:
                    self.question_queue.append(
                        decimal.Decimal(self.special_item))
                # if end
                self.special_item = None
                # Enqueues the special item so it doesn't get mixed with
                # values outside the parentheses.
                try:
                    while self.operator_stack[-1] != "(":
                        # This loops until it reaches an open parentheses.
                        self.question_queue.append(self.operator_stack[-1])
                        self.operator_stack.pop()
                        Debug.print(f"Popped '{self.question_queue[-1]}' "
                                    f"from the stack and enqueued it.\n"
                                    f"New Stack:\n{self.operator_stack}\n"
                                    f"New Queue:\n{self.question_queue}")
                    # while end
                # try end
                except IndexError:
                    print("Error: A parentheses is missing it's pair!")
                    return None
                # except end
                self.operator_stack.pop()
                Debug.print("Removed remaining open parentheses.")
                if len(self.operator_stack) > 0:
                    # Checks if there are operators left after popping
                    # the operators in parentheses.
                    self.stack_precedence = (
                        Calculator.operator_precedence.get(
                            self.operator_stack[-1],
                            -1
                        )
                    )
                    Debug.print(f"Reassigned stack precedence: " +
                                f"{self.stack_precedence}")
                    # Reassigns the operator precedence to the last
                    # operator.
                # if end
                else:
                    self.operator_precedence = -1
                # else end
            # elif end
            else:
                # If it is not an operator or parentheses then it
                # must be a letter or number.
                Debug.print(f"Current item: {item}")
                if self.special_item is None:
                    # If special item is empty assign the item to it.
                    self.special_item = item
                    Debug.print(f"New special item: {self.special_item}")
                # if end
                else:
                    Debug.print(f"Current special item: {self.special_item}")
                    if self.are_same_type(self.special_item[-1], item):
                        # Checks if both items are numbers or letters.
                        self.special_item += item
                        if self.special_item in Calculator.emdas_operators:
                            # Checks if by adding the item to it
                            # creates an operator.
                            self.handle_operator(self.special_item)
                            Debug.print(f"Generated new operator: " +
                                        f"{self.special_item}\n" +
                                        f"New Stack:\n{self.operator_stack}\n"
                                        + f"New Queue:\n{self.question_queue}")
                            self.special_item = None
                            # This handles what to do with the new operator
                            # and resets special item.
                        # if end
                        else:
                            Debug.print(f"Updated special item: " +
                                        f"{self.special_item}")
                        # else end
                    # if end
                    else:
                        # This means they aren't the same type.
                        Debug.print(f"Current item and " +
                                    f"special item don't match\n" +
                                    f"Current special item: " +
                                    f"{self.special_item}")
                        if self.conv_spec_item_to_num() == "error":
                            # There should only be a number in the special
                            # item and if it can't be converted, that means
                            # it isn't a number or operator.
                            return None
                        # if end
                        self.special_item = item
                    # else end
                # else end
            # else end
            self.prev_item = item
            Debug.print("-" * 10 + "Next Item" + "-" * 10)
        # for end
        if self.special_item is not None:
            # Appends the special item if there is one.
            try:
                self.question_queue.append(decimal.Decimal(self.special_item))
            # try end
            except decimal.InvalidOperation:
                print("Error: Unknown item ", self.special_item, ".", sep="'")
                return None
            # except end
        # if end
        while len(self.operator_stack) > 0:
            # This pops the remaining operators in the stack to the queue.
            self.question_queue.append(self.operator_stack[-1])
            self.operator_stack.pop()
        # while end
        Debug.print(f"Popped rest of stack to queue. Final queue:\n" +
                    f"{self.question_queue}")

        # This deletes any stray parentheses.
        final_queue = []
        for item in self.question_queue:
            if item == ")":
                print("Error: A parentheses is missing it's pair!")
                return None
            # if end
            elif item != "(":
                # If it's an open parentheses it gets skipped over.
                final_queue.append(item)
            # elif end
        # for end
        if len(final_queue) == 0:
            print("Error: There is nothing to evaluate!")
            return None
        # if end
        return self.question_queue

    def evaluate_question(self, question: list):
        """
        This takes a parsed question and returns the answer.

        References:
        https://www.youtube.com/watch?v=Wz85Hiwi5MY
        https://www.youtube.com/watch?v=bebqXO8H4eA

        :param question: A parsed question as a list.
        :return: The result of performing the calculations.
        """
        question_stack = []
        Debug.print("Beginning evaluation.")
        while len(question) > 0:
            # Repeats these calculations until it is left with the final
            # answer.
            # time.sleep(2)
            Debug.print(f"Remaining question.\n{question}")
            current_element = question[0]
            if current_element not in Calculator.emdas_operators:
                # If the current element is a number.
                question_stack.append(current_element)
                # Push the number to the stack.
                Debug.print(f"Current stack: {question_stack}")
            # if end
            elif (len(question_stack) > 1 and
                  current_element in Calculator.emdas_operators):
                # If there are two items to work on and the current
                # element is an operator.
                first_num = question_stack[-2]
                second_num = question_stack[-1]
                Debug.print(f"Current operation: {current_element}")
                result = self.return_operation[current_element](first_num,
                                                                second_num)
                for i in range(2):
                    # Range takes a number and creates a list starting
                    # from the first argument (if there are two)
                    # to the last number exclusively.
                    # If there are three arguments the third one is
                    # how much it increments by.
                    question_stack.pop()
                # for end
                question_stack.append(result)
                # Push the new result to the stack.
                Debug.print(f"New stack:\n"
                            f"{question_stack}")
            # elif end
            question.pop(0)
            # Un-enqueues the element we just worked on.
            Debug.print("-" * 10 + "Next Item" + "-" * 10)
        # while end
        Debug.print(f"Final stack:\n{question_stack}")
        if question_stack[0] == "paren error":
            return ["er1", question_stack[0]]  # This is an error code.
        if int(question_stack[0]) < question_stack[0]:
            return question_stack[0]
        # if end
        return int(question_stack[0])
    # def end


# class end


class Respond:
    """
    This handles word responses.
    """

    sentence_separators = {
        ".", " ", ",", "!", "?", "*", "/", "^", "@", "#", "$", "%",
        "~", "<", ">", ":", ";", "|", "_", "-", "+", "=", "(", ")"
    }

    sentence_deletions = {
        "'", '"', "`"
    }

    def __init__(self, question: str):
        question = Respond.split(question)
        Debug.print(question)
        if "help" in question:
            print("Type any math question and I'll answer it.\n" +
                  "Unfortunately I don't accept variables or " +
                  "special operators such as sin, cos, tan, etc...")
            # + on strings concatenates them (basically it combines them
            # into one big string)
        # if end
        elif "quit" in question or "stop" in question:
            Pref.pref["ask_new_question"] = False
            print("Aww okay :(\nI hope you have a great day!")
            time.sleep(2)
        # else end
        else:
            print("Sorry, I don't understand that command.")
        # else end

    # def end

    @staticmethod
    def split(question):
        """
        Splits a string according to the items in the sentence_separator set.

        :param question: The question as a string.
        :return: List.
        """
        question_list = [""]
        for character in question:
            if character not in Respond.sentence_separators:
                if character not in Respond.sentence_deletions:
                    question_list[-1] += character
                    # Adds the character to the last word in the question list.
                # if end
            # if end
            else:
                if len(question_list[-1]) > 0:
                    # Only creates a new word if there is
                    # something in the previous word.
                    question_list.append("")
                # if end
            # else end
        # for end

        if question_list[-1] == "":
            # Deletes an empty entry if there is one.
            question_list.pop()
        # if end

        if len(question_list) > 0:
            return question_list
        # if end
        else:
            return None
        # else end


# class end


if __name__ == '__main__':
    main()
    # main is a void function that starts my project without returning
    # anything.
# if end
