"""My Integration Project

An interactive calculator that accepts a few commands.
"""
__author__ = 'Jacob McCormack'

import time
import calculator
import pref
import graphing_calculator

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
        pref.Pref.load_preferences()
        # Pref.pref["ask_new_question"] = True
        print("There you go!")
    # try end
    except FileNotFoundError:
        print("\nWhoops, looks like you don't " +
              "have a preference file just yet.")
        # The + on strings concatenates them.
        pref.Pref.handle_load_error()
        print("I generated a new one for you!")
    # except end
    print()

    print("Welcome to Jacob's Calculator!")
    print("Put '=' in a function to graph a "
          "function. Otherwise, write normal math questions to use "
          "the regular calculator.")
    print("Type 'help' for more information.")
    print("Type 'stop' if you'd like to exit the program.")
    print("Note: exclude the quotes when issuing commands.")
    print()
    print("Start typing math questions below if you just want to "
          "calculate.")
    print("_" * 100)
    # The * on a string repeats whatever is in the string
    # the number of times indicated after the * symbol.

    if pref.Pref.pref["test_code"]:
        """
        If the value of the key 'test_code' is True it loops through
        the test_values array and passes said values to the Calculator
        class to work out the answer.
        """

        Respond.run_tests()
    # if end

    while pref.Pref.pref["ask_new_question"]:
        """
        This while loop repeats until the 'ask_new_question' key is reassigned
        False.
        The loop is fairly self explanatory.
        """

        question = input().lower()

        if "\\" in question:
            print("Sorry, '\\' is not allowed here.")

        else:
            try:
                while question[0] == " ":
                    question = question[1:]
                # while end
            except IndexError:
                print("Type something first!")
                continue
            # except end

            question_type = is_calculator_question(question)

            if type(question_type) is str:
                try:
                    graphing_calculator.Graph(question_type,
                                              resolution=Respond.resolution,
                                              x_range=Respond.x_range,
                                              y_range=Respond.y_range)
                except calculator.OperationError as error:
                    print(error)
                except ValueError as error:
                    print(error)

            elif question_type:

                print(f"The answer: {calculator.Calculate(question).answer}")

            else:
                Respond(question)
            # else end
        # else end
    # while end


# def end


def is_calculator_question(question: str):
    """
    Checks if the given string is a calculator question or not.

    :param question: String.
    :return: Boolean.
    """

    if "=" in question:
        return question
    # if end

    for character in question:
        if character.isnumeric():
            return True
        # if end
    # for end
    return False


# def end


class Respond:
    """
    This handles word responses.
    """

    x_range = (-20, 20)
    y_range = (-15, 15)
    resolution = (41, 31)

    def __init__(self, question: str):
        question = question.lower()
        self.question = question.split(" ")
        commands = {
            "quit": self.quit,
            "stop": self.quit,
            "help": self.print_help,
            "change_pref": self.update_preferences,
            "y_range": self.change_range,
            "x_range": self.change_domain,
            "resolution": self.change_resolution
        }

        if self.question[0] in commands:
            commands.get(self.question[0])()
        else:
            print("Sorry, I don't understand that command.")
        # else end

    # def end

    @staticmethod
    def quit():
        """
        Exits the program.
        """

        pref.Pref.pref["ask_new_question"] = False
        print("Aww okay :(\nI hope you have a great day!")
        time.sleep(2)

    # def end

    @staticmethod
    def change_resolution():
        """
        Exits the program.
        """

        valid_input = False
        resolution = ["", ""]
        while not valid_input:
            try:
                width = input("Enter width (positive integer): ")
                resolution[0] = int(width)

                if resolution[0] < 0:
                    raise ValueError
                # if end

                valid_input = True
            except ValueError:
                print("Width must be a positive integer.")
        # while end

        valid_input = False
        while not valid_input:
            try:
                height = input("Enter height (positive integer): ")
                resolution[1] = int(height)

                if resolution[1] < 0:
                    raise ValueError
                # if end

                valid_input = True
            except ValueError:
                print("Height must be a positive integer.")
        # while end

        Respond.resolution = tuple(resolution)

        print(f"Resolution successfully changed to {Respond.resolution}.")

    # def end

    @staticmethod
    def change_domain():
        """
        Changes the domain of the graph.
        """

        valid_input = False
        domain = [None, None]
        while not valid_input:
            try:
                x_min = input("Enter x min (any real number): ")
                domain[0] = float(x_min)

                valid_input = True
            except ValueError:
                print("Min must be a real number.")
        # while end

        valid_input = False
        while not valid_input:
            try:
                x_max = input("Enter x max (any real number): ")
                domain[1] = float(x_max)

                valid_input = True
            except ValueError:
                print("Max must be a real number.")
        # while end

        Respond.x_range = tuple(domain)

        print(f"X_range successfully changed to {Respond.x_range}.")

    # def end

    @staticmethod
    def change_range():
        """
        Changes the domain of the graph.
        """

        valid_input = False
        y_range = [None, None]
        while not valid_input:
            try:
                y_min = input("Enter y min (any real number): ")
                y_range[0] = float(y_min)

                valid_input = True
            except ValueError:
                print("Min must be a real number.")
        # while end

        valid_input = False
        while not valid_input:
            try:
                y_max = input("Enter y max (any real number): ")
                y_range[1] = float(y_max)

                valid_input = True
            except ValueError:
                print("Max must be a real number.")
        # while end

        Respond.y_range = tuple(y_range)

        print(f"Y_range successfully changed to {Respond.y_range}.")

    # def end

    @staticmethod
    def print_help():
        """
        Prints the help text.
        """

        print("Type any math equation you can think of and I will answer "
              "it. \nUnfortunately I don't support sin, cos, tan, etc "
              "or equations with variables unless graphing.\n"
              "Type 'y_range', 'x_range', and 'resolution' to change \n"
              "the range, domain, and resolution of the graph respectively.\n"
              "Also, you can "
              "type 'stop' or 'quit' to end the program.")
        # + on strings concatenates them (basically it combines them
        # into one big string)

    # def end

    def update_preferences(self):
        """
        Updates the preferences.
        """

        if len(self.question) == 3:
            pref.Pref.update_preference(self.question[1], self.question[2])
        else:
            print("There needs to be 2 arguments for this command.")
        # else end

    # def end

    @staticmethod
    def run_tests():
        """
        Runs tests.
        """

        print("Running tests now.\n")
        test_values = [
            "2+10-2^(5-3)+7-2*2+6/3+5%4+5//2",  # Should equal 16
            "2+10-2^(5-3)+7-2*2+6/3",  # Should equal 13
            "30-10^(20-18+2*1)+16/(2*2)*2+10*(4+6)",  # Should equal -9862
            "30-10^(20-18+2*1)+16/(2*2)2+10(4+6)",  # Should equal -9862
            "3+4*2/((1-5)^2^3)",  # Should equal 3.0001220703125
            "3.2+8",  # should equal 11.2
            "(     1 + 1          )) ",  # Should be error.
            "(     1 + 1           ",  # Should equal 2
            # "1sin(6)+6* 8 cos(5)",
            "8*2",  # Should equal 16
            "-10+2",  # Should equal -8
            "100/0",  # Should be an error.
            "",  # Should be error.
            "-1+8 - (-1+2)-0"  # Should equal 6
        ]
        for test_value in test_values:
            print("-" * 10, "New Question", "-" * 10)
            print(f"Question being tested:\n{test_value}")
            print(f"Answer: {calculator.Calculate(test_value).answer}")
        # for end

    # def end

    @staticmethod
    def print_secrets():
        """
        Prints the secrets.
        """
        print("Some secret commands:\n"
              # "'play_game' to play a game.\n"
              "'explain_bitwise_operators' to explain bitwise operators.\n"
              "'bitwise_calculator' to use the bitwise calculator.\n"
              "'graphing_calculator' to use the graphing calculator.")

    # def end


# class end


if __name__ == '__main__':
    main()
    # main is a void function that starts my project without returning
    # anything.
# if end
