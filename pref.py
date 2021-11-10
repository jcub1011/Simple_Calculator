"""Preference Handler"""
__author__ = "Jacob McCormack"


class Pref:
    """
    This contains all the preference data.
    """

    pref = {
        "test_code": False,
        "ask_new_question": True
    }
    # These are the default values.
    pref_length = len(pref)

    @staticmethod
    def load_preferences():
        """
        Handles the preferences.txt file.

        The function attempts to open the file 'preferences.txt'
        in read mode. Assuming it works out it then loops through every
        line in the text file. In each line it looks for an '=' sign.
        If it finds the '=' sign it splits the line and unpacks
        that line into variables 'key' and 'value'.
        If the unpacked 'value' string is equal to 'True' it
        reassigns 'value' to the bool True, otherwise it assigns it to False.
        Then it updates the dictionary in the Pref class with the new
        key value pair.

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
                # 'as preferences' is the same as
                # preferences = open("file", "r")
                line_count = 0
                for line in preferences:
                    print(".", end=" ")
                    line = line.rstrip()
                    key, value = line.split("=", 1)

                    if value == "True":
                        value = True
                    else:
                        value = False

                    Pref.pref[key] = value
                    line_count += 1
                # for end
            # with end
        # try end
        except ValueError:
            # If a line is missing the '=' character it calls the load error
            # function.
            print("\nOh no, your preference file was damaged. Poor thing...\n"
                  "Using defaults instead.")
            Pref.handle_load_error()
            return
        # except end

        # with end
        if line_count != Pref.pref_length:
            # If lines are missing or there are too many
            # it calls the load error function.
            print("\nOh no, your preference file was damaged. Poor thing.\n"
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

        First it converts the value passed to the function
        into it's bool counterpart. Assuming that works out
        it updates the key value pair in Pref.pref to the new
        key and value. Then it opens the preferences.txt in read mode
        and assigns preference_list to the array of lines in the file.
        While looping through each line it unpacks the line. If the
        key in the line matches what is being changes it
        updates the line to the new value, breaks the loop, and
        rewrites the file with the updated entry.

        :param key: The value to update.
        :param value: What to update the value to. Either True or False.
        """

        print("Updating preference .", end=" ")
        found_key = False
        converted_value = Pref.convert_from_string(value)

        if type(converted_value) is bool:
            print("Reassigning ")
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

                print("Successfully updated preferences.")
            else:
                print("Oops, that preference doesn't exist!")
        # if end
        else:
            print("Invalid preference assignment!")
        # else end

    # def end

    @staticmethod
    def convert_from_string(value: str):
        """
        Attempts to convert a string to a bool, float, integer, or string.

        :param value: The value to convert.
        :return: The converted value.
        """

        value = str(value).lower()
        if value == "false":
            value = False
        # if end
        elif value == "true":
            value = True
        # elif end
        else:
            try:
                value = float(value)
                if int(value) == value:
                    # Converts to integer if the float
                    # is the same as the integer version.
                    value = int(value)
                # if end
            # try end
            except ValueError:
                # This means the value is a string.
                value = str(value)
            # except end
        # else end
        return value
    # def end
# class end
