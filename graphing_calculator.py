"""
My Graphing Calculator

Graphs a function.
"""

__author__ = "Jacob McCormack"

import calculator
import decimal

"""
Returns a string with a formatted graph in it.
"""


def main():
    """Main function."""
    Graph("5x+2xy=3")


# def end


class Graph:
    """The Graphing Calculator"""

    root_finding_iterations = 0

    def __init__(self, function, x_range=(-20, 20), y_range=(-15, 15),
                 resolution=(41, 31), pixel_width=3, accuracy=True,
                 graph_background=" "):
        """
        Generates a graph based on the given function.

        References:
        https://youtu.be/6oMZb3yP_H8

        :param function: A function.
        :param x_range: tuple(starting x, ending x)
            Range of x values to draw in.
        :param y_range: tuple(starting y, ending y)
            Range of y values to draw in.
        :param resolution: tuple(width, height)
            How many "pixels" to display on the graph.
            NOTE: Keep an odd number.
        :param pixel_width: int
            How many characters wide a "pixel" is.
            ODD NUMBERS ONLY
        :param graph_background: str. length = 1
            What the graph background will look like.
        """

        if type(pixel_width) is not int:
            raise TypeError(f"Error: pixel_width must be an integer.")

        elif type(x_range) is not tuple:
            raise TypeError(
                "Error: x range is an invalid type. Must be tuple.")

        elif len(x_range) != 2:
            raise ValueError("Error: x range must have two values.")

        elif type(y_range) is not tuple:
            raise TypeError(
                "Error: y range is an invalid type. Must be tuple.")

        elif len(y_range) != 2:
            raise ValueError("Error: y range must have two values.")

        elif type(resolution) is not tuple:
            raise TypeError("Error: resolution is an invalid type. "
                            "Must be tuple.")

        elif len(resolution) != 2:
            raise ValueError("Error: resolution must have two values.")

        elif type(accuracy) is not bool:
            raise TypeError("Error: accuracy is an invalid type. "
                            "Must be bool.")

        elif type(graph_background) is not str:
            raise TypeError("Error: graph_background must be a string.")

        elif len(graph_background) != 1 and graph_background != "plug result":
            raise ValueError("Error: graph_background must be a single " +
                             "character long or 'plug result'.")
        # elif end

        # Generates a list where each row is the y pixel and each column is
        # the x pixel.
        self.pixels = [["" for _ in range(resolution[0])]
                       for _ in range(resolution[1])]
        self.graph = ""

        self.graph_background = graph_background

        self.accuracy = accuracy

        if self.is_zero_between(x_range):
            pass
        # if end

        # If accuracy is set to True it converts all the numbers to decimals.
        if not accuracy:
            self.x_range = x_range
            self.y_range = y_range
            self.resolution = resolution
        else:
            self.x_range = (decimal.Decimal(x_range[0]),
                            decimal.Decimal(x_range[1]))
            self.y_range = (decimal.Decimal(y_range[0]),
                            decimal.Decimal(y_range[1]))
            self.resolution = (decimal.Decimal(resolution[0]),
                               decimal.Decimal(resolution[1]))

        # Checks if pixel_width is an even number and converts it to odd.
        self.pixel_width = int(pixel_width)
        if self.pixel_width % 2 == 0:
            self.pixel_width += 1
        # if end

        if not accuracy:
            # left x minus right x divided by resolution of graph.
            self.x_step = (max(x_range) - min(x_range)) / resolution[0]
            self.x_start_point = min(x_range)

            self.y_step = (max(y_range) - min(y_range)) / resolution[1]
            self.y_start_point = max(y_range)
        else:
            self.x_step = ((decimal.Decimal(max(x_range))
                            - decimal.Decimal(min(x_range)))
                           / decimal.Decimal(resolution[0]))
            self.y_step = ((decimal.Decimal(max(y_range))
                            - decimal.Decimal(min(y_range)))
                           / decimal.Decimal(resolution[1]))

            self.x_start_point = decimal.Decimal(min(x_range))
            self.y_start_point = decimal.Decimal(max(y_range))
        # else end

        self.x_y_bar_locations = [None, None]
        # Finds the location of the y-axis.
        if self.is_zero_between(x_range):
            pixel_left = min(x_range)
            pixel_right = pixel_left + float(self.x_step)
            pixel = 0

            while not self.is_zero_between(pixel_left, pixel_right):
                pixel += 1
                pixel_left = pixel_right
                pixel_right += float(self.x_step)

                if pixel > self.resolution[0]:
                    break
                # if end
            # while end

            self.x_y_bar_locations[1] = pixel
        # if end

        # Finds the location of the x-axis.
        if self.is_zero_between(y_range):
            pixel_top = max(y_range)
            pixel_bottom = pixel_top - float(self.y_step)
            pixel = 0

            while not self.is_zero_between(pixel_top, pixel_bottom):
                pixel += 1
                pixel_top = pixel_bottom
                pixel_bottom -= float(self.y_step)

                if pixel > resolution[1]:
                    break
                # if end
            # while end

            self.x_y_bar_locations[0] = pixel
        # if end

        function = calculator.Calculate.clean_question(function)
        function = self.convert_to_implicit_function(function)
        function = calculator.Calculate.perform_question_separation_pass(
            function, accuracy)
        function = calculator.Calculate.convert_to_postfix(function)

        self.create_graph(function)
        self.draw_graph()
        # self.generate_graph(function)

        # response = input("Plug in values for x or y using 'x=' or 'y='.\n"
        #                  "Type 'draw new graph' to draw a new one.\n"
        #                  "Type 'quit' to exit the graphing calculator.\n")
        #
        # valid_response = False
        # draw_new_graph = False
        # stop = False
        #
        # while not valid_response:
        #
        #     response = response.lower()
        #     if response == "draw new graph":
        #         valid_response = True
        #         draw_new_graph = True

    # def end

    @staticmethod
    def convert_to_implicit_function(function: str):
        """
        Converts an explicit function into an implicit one.

        :param function: An explicit function.
        :return: An implicit function.
        """

        equal_count = 0
        for character in function:
            if character == "=":
                equal_count += 1
            # if end
        # for end

        if equal_count > 1:
            print("Invalid function: Too many '='s.")
            return None
        # if end

        first_piece, second_piece = function.split("=", 1)

        return second_piece + f"-({first_piece})"

    # def end

    @staticmethod
    def locate_x_and_y_indexes(function):
        """
        Finds the indices of the x's and y's.

        :param function: A function with x's and y's.
        :return: A list of x indexes and a list of y indexes.
        """

        x_indexes = []
        y_indexes = []
        for index, character in enumerate(function):
            if character == "x":
                x_indexes.append(index)
            elif character == "y":
                y_indexes.append(index)
            # elif end
        # for end

        return x_indexes, y_indexes

    # def end

    def define_pixel(self, function: list, pixel: tuple, indices: tuple):
        """
        Returns the character that will be put in the center of the pixel.

        :param function: The function to plug into.
        :param pixel: The points that define the pixel.
        :param indices: The indexes of the x and y variables.
        :return: A single character or None.
        """

        pixel_values = []
        zero_pixels = []
        for index, point in enumerate(pixel):
            pixel_values.append(self.plug_into_function(function, point,
                                                        indices))
            if pixel_values[-1] == 0:
                zero_pixels.append(pixel[index])
            # if end
        # for end

        if len(zero_pixels) > 2:
            return "*"
        elif len(zero_pixels) == 2:
            rise = zero_pixels[0][1] - zero_pixels[1][1]
            run = zero_pixels[0][0] - zero_pixels[1][0]

            if run == 0:
                return "|"
            else:
                slope = rise / run
                return self.get_character(slope)
            # if end

        pixel_top = (pixel[0], pixel[1])
        pixel_bottom = (pixel[3], pixel[2])
        pixel_left = (pixel[0], pixel[3])
        pixel_right = (pixel[1], pixel[2])

        roots = []
        if self.is_zero_between(pixel_values[0], pixel_values[3]):
            roots.append(self.find_root(function, pixel_left, indices, 5))

        if self.is_zero_between(pixel_values[0], pixel_values[1]):
            roots.append(self.find_root(function, pixel_top, indices, 5))

        if self.is_zero_between(pixel_values[3], pixel_values[2]):
            roots.append(self.find_root(function, pixel_bottom, indices, 5))

        if self.is_zero_between(pixel_values[1], pixel_values[2]):
            roots.append(self.find_root(function, pixel_right, indices, 5))
        # if end

        if len(roots) == 2:
            rise = roots[0][1] - roots[1][1]
            run = roots[0][0] - roots[1][0]

            if run == 0:
                return "|"
            # if end
            slope = rise / run

            return self.get_character(slope)
        elif len(roots) > 2:
            return "#"
        elif len(roots) == 1:
            return "*"
        # elif end

        if self.graph_background == "plug result":
            x = (pixel[0][0] + pixel[1][0]) / 2
            y = (pixel[0][1] + pixel[3][1]) / 2
            return self.plug_into_function(function, (x, y), indices)
        # if end

        return None

    # def end

    def get_character(self, slope):
        """
        Returns a character based on the slope of the line in the pixel.

        :param slope: The slope of the line in the pixel.
        :return: A single character long string.
        """

        # Sets the values of which a slope is drawn with a vertical line
        # or horizontal.
        vertical_slope_threshold = 3 / float(self.x_step)
        horizontal_slope_threshold = 0.5 * float(self.y_step)

        # Makes sure the horizontal slope is never greater than the vertical
        # slope.
        if horizontal_slope_threshold > vertical_slope_threshold:
            vertical_slope_threshold = horizontal_slope_threshold * 6
        # if end

        neg_vertical_slope_threshold = vertical_slope_threshold * (-1)
        neg_horizontal_slope_threshold = horizontal_slope_threshold * (-1)

        if (slope >= vertical_slope_threshold or
                slope <= neg_vertical_slope_threshold):
            return "|"
        elif (neg_horizontal_slope_threshold < slope
              < horizontal_slope_threshold):
            return "-"
        elif slope < 0:
            return "\\"
        elif slope > 0:
            return "/"
        # else end

    # def end

    @staticmethod
    def find_root(function: list, points: tuple,
                  indices: tuple, max_iterations: int):
        """
        Finds the root of the given variable.

        :param function: The implicit function to plug into.
        :param points: The two points to plug in.
        :param indices: The indexes of the x and y variables.
        :param max_iterations: Highest number of iterations to perform.
        :return: The x or y value where the function is zero.
        """

        midpoint = (((points[0][0] + points[1][0]) / 2),
                    ((points[0][1] + points[1][1]) / 2))

        first_value = Graph.plug_into_function(function, points[0], indices)
        midpoint_value = Graph.plug_into_function(function, midpoint, indices)

        if midpoint_value == 0 or max_iterations < 1:
            return midpoint
        # if end

        max_iterations -= 1

        if Graph.is_zero_between(first_value, midpoint_value):
            # If the zero is between the first point and the midpoint
            # it plugs those points into the root finder recursively.
            return Graph.find_root(function, (points[0], midpoint),
                                   indices, max_iterations)
        else:
            # Else it does the same with the midpoint and second point.
            return Graph.find_root(function, (midpoint, points[1]),
                                   indices, max_iterations)
        # else end

    # def end

    def create_graph(self, function: list):
        """
        Creates an array of pixels.

        :param function: The function to graph.
        """

        indices = self.locate_x_and_y_indexes(function)

        pixel_top = self.y_start_point
        pixel_bottom = self.y_start_point - self.y_step

        for y_pixel in range(len(self.pixels)):
            # Resets the pixel left and right every row.
            pixel_left = self.x_start_point
            pixel_right = self.x_start_point + self.x_step

            for x_pixel in range(len(self.pixels[0])):
                # Pixels are defined as [top left, top right, bottom right,
                # bottom left]
                pixel = ((pixel_left, pixel_top),
                         (pixel_right, pixel_top),
                         (pixel_right, pixel_bottom),
                         (pixel_left, pixel_bottom))

                pixel_layout = self.define_pixel(function, pixel, indices)

                # Inserts the character into the defined pixel
                self.pixels[y_pixel][x_pixel] = pixel_layout

                # Shifts the pixel dimensions to the right.
                pixel_left = pixel_right
                pixel_right += self.x_step
            # for end

            # Shifts the pixel dimensions downwards.
            pixel_top = pixel_bottom
            pixel_bottom -= self.y_step
        # for end

    # def end

    def draw_graph(self):
        """
        Prints the graph.
        """

        padding = " " * int((self.pixel_width - 1) / 2)

        # The top and bottom bars of the graph. Decorative.
        graph_bar = ("_" * self.pixel_width) * int(self.resolution[0])

        if self.x_y_bar_locations[1] is None:
            # If the x axis isn't on the graph it will draw it either on the
            # top or bottom side depending on if the range is negative or
            # positive.
            if self.x_range[0] > 0:
                self.x_y_bar_locations[1] = 0
            else:
                self.x_y_bar_locations[1] = int(self.resolution[0] - 1)
            # if end

        if self.x_y_bar_locations[0] is None:
            # If the y axis isn't on the graph it will draw it either on the
            # left or right side depending on if the range is negative or
            # positive.
            if self.y_range[0] < 0:
                self.x_y_bar_locations[0] = 0
            else:
                self.x_y_bar_locations[0] = int(self.resolution[1] - 1)
            # if end
        # if end

        self.graph += " " + graph_bar
        for pixel_y, row in enumerate(self.pixels):
            self.graph += "\n|"

            for pixel_x, pixel in enumerate(row):
                if type(pixel) is str:
                    self.graph += padding + pixel + padding
                else:
                    if pixel is None:
                        if (pixel_y == self.x_y_bar_locations[0] and
                                pixel_x == self.x_y_bar_locations[1]):
                            self.graph += padding + "+" + padding

                        elif pixel_y == self.x_y_bar_locations[0]:
                            if (pixel_x + self.x_y_bar_locations[1]) % 2 == 0:
                                # Prints the number
                                self.graph += self.get_pixel_number(pixel_x)
                            else:
                                self.graph += "-" * self.pixel_width
                            # else end

                        elif pixel_x == self.x_y_bar_locations[1]:
                            if (pixel_y + self.x_y_bar_locations[0]) % 2 == 0:
                                # Prints the number
                                self.graph += self.get_pixel_number(pixel_y,
                                                                    True)
                            else:
                                self.graph += padding + "|" + padding
                            # else end

                        else:
                            self.graph += (padding + self.graph_background
                                           + padding)
                        # else end
                    else:
                        pixel = float(pixel)
                        pixel = round(pixel)

                        # Replaces the number with it's 99 equivalent if
                        # it's out of the (-99, 99) range.
                        if pixel < -99:
                            pixel = -99
                        elif pixel > 99:
                            pixel = 99
                        # elif end

                        self.graph += f"{pixel:3}"
                    # else end
                # else end
            # for end

            self.graph += "|"
        # for end

        self.graph += "\n|" + graph_bar + "|"

        print(self.graph)

    # def end

    def get_pixel_number(self, pixel, is_y=False):
        """
        Gets the pixel number in the graph.

        :param pixel: The number of pixels from the initial y or x pixel.
        :param is_y: Set True if computing y pixel.
        :return: Returns a 3 character long number as a string.
        """

        if not is_y:
            if pixel > self.x_y_bar_locations[1]:
                pixel_midpoint = (self.x_start_point
                                  + (self.x_step * pixel)
                                  + self.x_step)
            else:
                pixel_midpoint = (self.x_start_point
                                  + (self.x_step * pixel))
            # else end
        else:
            if pixel > self.x_y_bar_locations[0]:
                pixel_midpoint = (self.y_start_point
                                  - (self.y_step * pixel)
                                  - self.y_step)
            else:
                pixel_midpoint = (self.y_start_point
                                  - (self.y_step * pixel))
            # else end
        # else end

        pixel_midpoint = round(pixel_midpoint, 2)
        pixel_midpoint = str(pixel_midpoint)

        if pixel_midpoint[0] == "-":
            # Deletes the leading negative sign.
            pixel_midpoint = pixel_midpoint[1:]
        # if end
        if pixel_midpoint[0] == "0":
            # Deletes the leading zero.
            pixel_midpoint = pixel_midpoint[1:]
        # if end

        if len(pixel_midpoint) > 3:
            # Shortens the string if it exceeds 3
            # chars.
            pixel_midpoint = pixel_midpoint[:3]
            if pixel_midpoint[-1] == ".":
                # If the last character is a .
                # it deletes that too.
                pixel_midpoint = pixel_midpoint[:2]
        # if end

        return f"{pixel_midpoint:>3}"
        # Formats the string as 3 characters long
        # right aligned.

    # def end

    @staticmethod
    def plug_into_function(function: list, x_y_values: tuple,
                           indexes: tuple, ):
        """
        Plugs the given values into the given function.

        :param function: An implicit function in postfix notation.
        :param x_y_values: (x value, y value)
        :param indexes: Tuple with lists of x and y indices.
        :return: Result of plugging in.
        """

        for index in indexes[0]:
            function[index] = x_y_values[0]
        # for end

        for index in indexes[1]:
            function[index] = x_y_values[1]
        # for end

        return calculator.Calculate.evaluate_question(function)

    # def end

    @staticmethod
    def is_zero_between(num_1, num_2=None):
        """
        Checks if zero is between two numbers.
        :param num_1: Number 1.
        :param num_2: Number 2.
        :return: Bool.
        """

        if type(num_1) is tuple:
            if num_1[0] < 0 < num_1[1] or num_1[1] < 0 < num_1[0]:
                return True
            # if end
            return False
        else:
            if num_1 < 0 < num_2 or num_2 < 0 < num_1:
                return True
            # if end
            return False
        # else end

    # def end


# class end


if __name__ == '__main__':
    main()
# if end
