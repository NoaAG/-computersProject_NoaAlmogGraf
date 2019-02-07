import fitgui_filehandling as filehandling
import fitgui_chi_calculations as fitgui
from matplotlib import pyplot
from matplotlib.mlab import frange
import numpy

OUTPUT_FORMAT = \
    "a={a_value} ± {a_error}\n" \
    "b={b_value} ± {b_error}\n" \
    "chi2={chi_squared}\n" \
    "chi2_reduced={chi_reduced}"


# Function for non - linear fit.
def myfunc(x, a):
    return a[0] + x * a[1] + 0.5 * a[2] * (x ** 2)


# Function for the linear fit
def linear_function(x, a):
    return a[1] + x * a[0]


# This functions draws the red fitted line on the graph.
def plot_fitted_graph(min, max, a, func=linear_function, c="red"):
    x_values = numpy.array(frange(min, max))
    y_values = [func(x, a) for x in x_values]
    pyplot.plot(x_values, y_values, color=c)


# This function plots the crosses on the graph.
def plot_data_points(table):
    # Get the table values
    x_values = table["x"]
    x_errors = table["dx"]
    y_values = table["y"]
    y_errors = table["dy"]

    for i in range(len(x_values)):
        pyplot.errorbar(x_values[i], y_values[i], yerr=y_errors[i], xerr=x_errors[i], ecolor="b", elinewidth=0,
                        barsabove=True)


# Save the graph as a SVG file.
def save_the_graph(name):
    pyplot.savefig(name + ".svg", format="svg")


# This function receives data points and calculates
# the best linear fit for those data points.
def fit_linear(filename):
    y_title, x_title, table = filehandling.file_handling(filename)

    a, b, da, db, chi, chi_red = fitgui.fit_results(table)

    print(OUTPUT_FORMAT.format(
        a_value=a,
        a_error=da,
        b_value=b,
        b_error=db,
        chi_squared=chi,
        chi_reduced=chi_red
    ))

    # Create the graph.
    pyplot.figure()
    pyplot.title("Generated linear fit")
    pyplot.ylabel(y_title)
    pyplot.xlabel(x_title)

    # Set the data and the graph.
    # plot_data_points(table)
    plot_fitted_graph(min(table["x"]), max(table["x"]), (a, b))
    plot_data_points(table)

    save_the_graph("linear_fit")
    pyplot.show()


# BONUS
def search_best_parameter(filename):
    a, b, y_title, x_title, table = filehandling.bonus_file_handling(filename)

    b_range = frange(b[0], b[1], b[2])
    a_range = frange(a[0], a[1], a[2])

    # Calculate the chi for each pair.
    chi_values = []
    for b_value in b_range:
        for a_value in a_range:
            chi_values.append([b_value, a_value, fitgui.bonus_chi_squared(table, myfunc, (0, a_value, b_value))])

    # Find the best chi.
    best = chi_values[0]
    for b_value, a_value, chi in chi_values:
        if chi < best[2]:
            best = (b_value, a_value, chi)

    print(OUTPUT_FORMAT.format(
        a_value=best[1],
        a_error=a[2],
        b_value=best[0],
        b_error=b[2],
        chi_squared=best[2],
        chi_reduced=fitgui._chi_reduced(best[2], len(table["x"]))
    ))

    # Create graph.
    pyplot.figure()
    pyplot.title("Generated custom fit")
    pyplot.ylabel(y_title)
    pyplot.xlabel(x_title)

    # Set the data and graph.
    plot_fitted_graph(min(table["x"]), max(table["x"]), (0, best[1], best[0]), myfunc, c="blue")
    plot_data_points(table)

    pyplot.show()


if __name__ == "__main__":
    print("FIRST GRAPH: ")
    fit_linear(r"C:\Users\Noa\Documents\תואר\שנה א\סמסטר א\מחשבים "
               r"לפיזיקאים\Project\inputOutputExamples\workingCols\input.txt")
    print("SECOND GRAPH: ")
    fit_linear(r"C:\Users\Noa\Documents\תואר\שנה א\סמסטר א\מחשבים "
               r"לפיזיקאים\Project\inputOutputExamples\workingRows\input.txt")
    print("THIRD GRAPH (BONUS): ")
    search_best_parameter(r"C:\Users\Noa\Documents\תואר\שנה א\סמסטר א\מחשבים "
                          r"לפיזיקאים\Project\inputOutputExamples\bonus\input.txt")
