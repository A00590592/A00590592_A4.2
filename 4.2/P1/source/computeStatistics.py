"""
P1 - Compute Statistics

Calculates:
- COUNT
- MEAN
- MEDIAN
- MODE (or #N/A)
- Population Standard Deviation
- Population Variance (expected file uses sample variance N-1)

Rules:
- Invoked from command line
- Receives an input file as parameter
- Prints results to screen and writes them to an output file
- Invalid data is reported and execution continues

Usage:
    python computeStatistics.py input_file.txt

"""

# -----------------------------------------------------------------------------
# pylint_P1_v1
# Pylint notes:
    # - C0305: Trailing newlines (trailing-newlines):
    #   End lines are eliminated.
    # - C0103: Module name "computeStatistics"
    #   doesn't conform to snake_case naming style (invalid-name):
    #   pylint: disable=invalid-name
    # - C0116: Missing function or method docstring
    #   (missing-function-docstring): docstrings are adedd
    # - R1731: Consider using 'mode_value = max(mode_value, current_value)'
    #   instead of unnecessary if block (consider-using-max-builtin):
    #   Built-in functions such as max() are not used
    #   because the goal of the exercise is to implement the logic manually.
    # - R0914: Too many local variables (16/15):
    #   pylint: disable= too-many-locals
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# pylint_P1_v2
# Pylint notes:
    # - C0304: Final newline missing (missing-final-newline)
    #   Final line is added
    # - R1731: Consider using 'mode_value = max(mode_value, current_value)'
    #   instead of unnecessary if block (consider-using-max-builtin):
    #   pylint: disable= consider-using-max-builtin
# -----------------------------------------------------------------------------

# pylint: disable=invalid-name, too-many-locals, consider-using-max-builtin

import os
import sys
import time


def read_numbers(file_path):
    """Reads numeric values from a text file line by line."""
    numbers = []

    with open(file_path, "r", encoding="utf-8") as file:
        line_number = 0
        for line in file:
            line_number += 1
            value = line.strip()

            if value == "":
                print(f"Invalid data at line {line_number}: empty")
                continue

            try:
                number = float(value)
                numbers.append(number)
            except ValueError:
                print(f"Invalid data at line {line_number}: {value}")

    return numbers


def insertion_sort(values):
    """Sorts a list of numeric values in ascending order."""
    sorted_values = values[:]

    for i in range(1, len(sorted_values)):
        key = sorted_values[i]
        j = i - 1
        while j >= 0 and sorted_values[j] > key:
            sorted_values[j + 1] = sorted_values[j]
            j -= 1
        sorted_values[j + 1] = key

    return sorted_values


def calculate_mean(values):
    """Calculates the arithmetic mean of a list of numbers."""
    total = 0.0
    for v in values:
        total += v
    return total / len(values)


def calculate_median(sorted_values):
    """Calculates the median value from a sorted list of numbers."""
    n = len(sorted_values)
    middle = n // 2

    if n % 2 == 1:
        return sorted_values[middle]

    return (sorted_values[middle - 1] + sorted_values[middle]) / 2


def calculate_mode(sorted_values):
    """ Calculates the mode of a sorted list of numbers.
        If multiple values share the highest frequency, the largest value is returned.
        If no value repeats, '#N/A' is returned."""
    max_count = 1
    mode_value = "#N/A"

    current_value = sorted_values[0]
    current_count = 1

    for i in range(1, len(sorted_values)):
        if sorted_values[i] == current_value:
            current_count += 1
        else:
            if current_count > max_count:
                max_count = current_count
                mode_value = current_value
            elif current_count == max_count and mode_value != "#N/A":
                if current_value > mode_value:
                    mode_value = current_value

            current_value = sorted_values[i]
            current_count = 1

    if current_count > max_count:
        max_count = current_count
        mode_value = current_value
    elif current_count == max_count and mode_value != "#N/A":
        if current_value > mode_value:
            mode_value = current_value

    if max_count == 1:
        return "#N/A"

    return mode_value


def sum_squared_diff(values, mean):
    """Calculates the sum of squared differences from the mean."""
    total = 0.0
    for v in values:
        diff = v - mean
        total += diff * diff
    return total


def calculate_variance_sample(values, mean):
    """ Calculates the sample variance of a list of numbers.
        Uses N-1 in the denominator."""
    n = len(values)
    if n <= 1:
        return 0.0
    total_sq = sum_squared_diff(values, mean)
    return total_sq / (n - 1)


def sqrt_newton(value):
    """Calculates the square root of a number using Newton's method."""
    if value == 0:
        return 0.0

    guess = value
    for _ in range(30):
        guess = (guess + value / guess) / 2

    return guess


def get_results_path(input_file):
    """ Builds the output file path for the results file.
        The output file name is based on the input file name."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(current_dir, "..", "results")

    input_name = os.path.basename(input_file)
    base_name, _ = os.path.splitext(input_name)

    result_file = f"{base_name}_Results_generated.txt"

    if os.path.isdir(results_dir):
        return os.path.join(results_dir, result_file)

    return result_file


def main():
    """ Main execution function.
        Handles input arguments, runs calculations, prints results, and writes the output file."""
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py input_file.txt")
        return

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print(f"Error: file not found -> {input_file}")
        return

    numbers = read_numbers(input_file)

    elapsed_time = time.time() - start_time

    if len(numbers) == 0:
        print("No valid numeric data found.")
        print(f"TIME_ELAPSED_SECONDS\t{elapsed_time}")
        return

    count = len(numbers)
    mean = calculate_mean(numbers)
    sorted_numbers = insertion_sort(numbers)
    median = calculate_median(sorted_numbers)
    mode = calculate_mode(sorted_numbers)

    total_sq = sum_squared_diff(numbers, mean)

    std_dev = sqrt_newton(total_sq / count)
    variance = calculate_variance_sample(numbers, mean)

    results = [
        f"COUNT\t{count}",
        f"MEAN\t{mean}",
        f"MEDIAN\t{median}",
        f"MODE\t{mode}",
        f"SD\t{std_dev}",
        f"VARIANCE\t{variance}",
        f"TIME_ELAPSED_SECONDS\t{elapsed_time}",
    ]

    for line in results:
        print(line)

    output_path = get_results_path(input_file)
    with open(output_path, "w", encoding="utf-8") as output_file:
        for line in results:
            output_file.write(line + "\n")


if __name__ == "__main__":
    main()
