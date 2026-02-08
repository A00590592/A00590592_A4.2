"""
P1 - Compute Statistics

Calculates:
- COUNT
- MEAN
- MEDIAN
- MODE (or #N/A)
- Population Standard Deviation
- Population Variance

Usage:
    python computeStatistics.py input_file.txt
"""

import os
import sys
import time


def read_numbers(file_path):
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
    total = 0.0
    for v in values:
        total += v
    return total / len(values)


def calculate_median(sorted_values):
    n = len(sorted_values)
    middle = n // 2

    if n % 2 == 1:
        return sorted_values[middle]

    return (sorted_values[middle - 1] + sorted_values[middle]) / 2


def calculate_mode(sorted_values):
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
            current_value = sorted_values[i]
            current_count = 1

    if current_count > max_count:
        max_count = current_count
        mode_value = current_value

    if max_count == 1:
        return "#N/A"

    return mode_value


def calculate_variance(values, mean):
    total = 0.0
    for v in values:
        diff = v - mean
        total += diff * diff
    return total / len(values)


def sqrt_newton(value):
    if value == 0:
        return 0.0

    guess = value
    for _ in range(30):
        guess = (guess + value / guess) / 2

    return guess


def get_results_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(current_dir, "..", "results")

    if os.path.isdir(results_dir):
        return os.path.join(results_dir, "StatisticsResults.txt")

    return "StatisticsResults.txt"


def main():
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
    variance = calculate_variance(numbers, mean)
    std_dev = sqrt_newton(variance)

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

    output_path = get_results_path()
    with open(output_path, "w", encoding="utf-8") as output_file:
        for line in results:
            output_file.write(line + "\n")


if __name__ == "__main__":
    main()

