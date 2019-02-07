import os.path

# Errors.
ERROR_LENGTHS_DO_NOT_MATCH = "Input file error: Data lists are not the same \
length."
ERROR_UNCERTAINTY_IS_NOT_POSITIVE = "Input file error: Not all \
uncertainties are positive."
ERROR_PATH_NAME_INVALID = "Input file error: path invalid."


# This function checks whether the file is valid or not.
def is_filename_valid(filename):
    # Check if the file path is valid.
    if not (os.path.exists(filename)):
        return False

    # Check if the path leads to a file.
    if not (os.path.isfile(filename)):
        return False

    # Check if the file has the right extension.
    if filename[-3:] != "txt":
        return False

    # File is valid
    return True


# This function rearranges the table to row format.
def transpose_table(lines):
    table = {"x": [], "dx": [], "y": [], "dy": []}

    # Check that all the rows are the same length.
    if len(set([len(line.split(" ")) for line in lines])) != 1:
        print(ERROR_LENGTHS_DO_NOT_MATCH)
        exit()

    # Check if the file is in columns.
    if all([p in ['x', 'y', 'dx', 'dy'] for p in lines[0].lower().split(" ")]):
        # Save the order of columns.
        column_order = lines[0].lower().split(" ")

        # Insert the values into the relevant keys (which are lists).
        for line in lines[1:]:
            for col in range(len(column_order)):
                table[column_order[col]].append(float(line.split(" ")[col]))
    else:
        for line in lines:
            table[line.lower().split(" ")[0]] = list(map(float, line.split(" ")[1:]))

    return table


# This function checks the validity of the data (checks errors).
def check_data(table):
    # Check the x uncertainties.
    for value in table["dx"]:
        if value <= 0:
            print(ERROR_UNCERTAINTY_IS_NOT_POSITIVE)
            return None

    # Check the x uncertainties.
    for value in table["dy"]:
        if value <= 0:
            print(ERROR_UNCERTAINTY_IS_NOT_POSITIVE)
            return None

    # The table is valid.
    return table


# This function gets the content of the file.
def get_content(filename):
    with open(filename, "r") as filehandle:
        lines = filehandle.readlines()

        # Remove empty lines.
        new_lines = []
        for line in lines:
            if line.strip("\n") != "":
                new_lines.append(line.strip("\n"))

        # Get graph titles.
        y_title = new_lines.pop(len(new_lines) - 1)[8:]
        x_title = new_lines.pop(len(new_lines) - 1)[8:]

        # Correct the table.
        table = transpose_table(new_lines)

        return y_title, x_title, check_data(table)

    # Default return value (Error with file).
    return ("", "", None)


# This function receives a file and returns a table of data points.
# If the file is invalid in some way, it returns None.
def file_handling(filename):
    if not is_filename_valid(filename):
        print(ERROR_PATH_NAME_INVALID)
        exit()

    return get_content(filename)


# BONUS
def bonus_file_handling(filename):
    with open(filename, "r") as filehandle:
        lines = filehandle.readlines()

        # Remove empty lines.
        new_lines = []
        for line in lines:
            if line.strip("\n") != "":
                new_lines.append(line.strip("\n"))

        # Get the last 2 lines and convert the values to float.
        b = new_lines.pop(len(new_lines) - 1).split(" ")
        a = new_lines.pop(len(new_lines) - 1).split(" ")

        # range of a and b.
        a = (float(a[1]), float(a[2]), float(a[3]))
        b = (float(b[1]), float(b[2]), float(b[3]))

        # Get graph titles.
        y_title = new_lines.pop(len(new_lines) - 1)[8:]
        x_title = new_lines.pop(len(new_lines) - 1)[8:]

        # Correct the table.
        table = transpose_table(new_lines)

        return a, b, y_title, x_title, check_data(table)

    # Default return value (Error with file).
    return None, None, "", "", None
