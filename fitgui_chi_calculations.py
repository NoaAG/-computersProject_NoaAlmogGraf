import math


def chi_value_avg(values, y_errors):
    # This function calculates and returns the average of the values.
    # Square the error values of y.
    squared_y_errors = map(lambda y: y ** 2, y_errors)

    numerator = []
    denominator = []
    for i in range(len(values)):
        # Calculate for each value the ratio between the value and the squared value of y error.
        numerator.append(values[i] / y_errors[i])
        # Calculate the inverse of each Y error.
        denominator.append(1 / y_errors[i])

    # Return the average of the values.
    return sum(numerator) / sum(denominator)


def _chi_squared(data):
    # Calculate fit values.
    a = _a(data)
    b = _b(data)

    # Get the table values
    y_values = data["y"]
    y_errors = data["dy"]
    x_values = data["x"]
    x_errors = data["dx"]

    # Calculate the approximation for a linear function.
    ratios = []
    for i in range(len(x_values)):
        ratios.append(((y_values[i] - (a * x_values[i] + b)) / y_errors[i]))

    # Square each value.
    squared_values = map(lambda value: value ** 2, ratios)

    # Return the sum of all the squared values.
    return sum(squared_values)


def _chi_reduced(chi_squared, N):
    # this function calculates the reduced chi squared.
    return chi_squared / (N - 2)


# This function calculates the a parameter
def _a(table):
    # Get the values from the table.
    x_values = table["x"]
    x_errors = table["dx"]
    y_values = table["y"]
    y_errors = table["dy"]

    # Calculate new values for formula.
    xy_values = []
    x_values_squared = []
    for i in range(len(x_values)):
        xy_values.append(x_values[i] * y_values[i])
        x_values_squared.append(x_values[i] ** 2)

    # Calculate all the averages for the a formula.
    xy_average = chi_value_avg(xy_values, y_errors)
    x_average = chi_value_avg(x_values, y_errors)
    y_average = chi_value_avg(y_values, y_errors)
    x_squared_average = chi_value_avg(x_values_squared, y_errors)

    return (xy_average - x_average * y_average) / (x_squared_average - x_average ** 2)


# This function calculates the b parameter.
def _b(table):
    # Get the values from the table.
    x_values = table["x"]
    x_errors = table["dx"]
    y_values = table["y"]
    y_errors = table["dy"]

    a = _a(table)
    # Calculate all the averages for the b formula.
    x_average = chi_value_avg(x_values, y_errors)
    y_average = chi_value_avg(y_values, y_errors)

    return y_average - x_average * a


# This function calculates the b uncertainty.
def _db(table):
    # Get the values from the table.
    y_values = table["y"]
    y_errors = table["dy"]
    x_values = table["x"]
    x_errors = table["dx"]

    squared_y_errors = []
    x_values_squared = []
    N = len(x_values)
    for i in range(N):
        squared_y_errors.append(y_errors[i] ** 2)
        x_values_squared.append(x_errors[i] ** 2)

    dy_squared_average = chi_value_avg(squared_y_errors, y_errors)
    x_squared_average = chi_value_avg(x_values_squared, y_errors)
    x_average = chi_value_avg(x_values, y_errors)

    return (dy_squared_average * (x_average ** 2)) / (N * (x_squared_average - x_average ** 2))


# This function calculates the a uncertainty.
def _da(table):
    # Get the values from the table
    y_values = table["y"]
    y_errors = table["dy"]
    x_values = table["x"]
    x_errors = table["dx"]

    squared_y_errors = []
    x_values_squared = []
    N = len(x_values)
    for i in range(N):
        squared_y_errors.append(y_errors[i] ** 2)
        x_values_squared.append(x_errors[i] ** 2)

    dy_squared_average = chi_value_avg(squared_y_errors, y_errors)
    x_squared_average = chi_value_avg(x_values_squared, y_errors)
    x_average = chi_value_avg(x_values, y_errors)

    return dy_squared_average / (N * (x_squared_average - x_average ** 2))


# This function returns the results of the linear fit
def fit_results(table):
    a = _a(table)
    b = _b(table)
    da = _da(table)
    db = _db(table)
    chi_squared = _chi_squared(table)
    chi_squared_reduced = _chi_reduced(chi_squared, len(table["x"]))

    return a, b, da, db, chi_squared, chi_squared_reduced


# BONUS
def bonus_chi_squared(table, func, a):
    # Get the values from the table.
    x_values = table["x"]
    x_errors = table["dx"]
    y_values = table["y"]
    y_errors = table["dy"]

    # Calculate the approximation for a linear function.
    ratios = []
    for i in range(len(x_values)):
        temp = y_errors[i] ** 2
        temp = temp + (func(x_values[i] + x_errors[i], a) - func(x_values[i] - x_errors[i], a)) ** 2
        ratios.append((y_values[i] - func(x_values[i], a)) / (temp ** 0.5))

    # Square each value.
    squared_values = map(lambda value: value ** 2, ratios)

    # Return the sum of all the squared values.
    return sum(squared_values)
