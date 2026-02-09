"""
P2 - Converter

Converts integer numbers from a text file into:
- Binary base
- Hexadecimal base

Rules:
- Invoked from command line
- Receives an input file as parameter
- Prints results to screen and writes them to an output file
- Invalid data is reported and execution continues

Usage:
    python convertNumbers.py fileWithData.txt
"""

# -----------------------------------------------------------------------------
# pylint_P2_v1
# Pylint notes:
    # - C0304: Final newline missing (missing-final-newline)
    #   Final line is added
# -----------------------------------------------------------------------------
# pylint: disable=invalid-name, too-many-locals

import os
import sys
import time


HEX_DIGITS = "0123456789ABCDEF"


def read_integers(file_path):
    """Reads integers from a text file line by line.

    Invalid or empty lines are reported and skipped.
    Returns a list of valid integers.
    """
    numbers = []

    with open(file_path, "r", encoding="utf-8") as file:
        line_number = 0
        for line in file:
            line_number += 1
            raw = line.strip()

            if raw == "":
                print(f"Invalid data at line {line_number}: empty")
                continue

            try:
                value = float(raw)
            except ValueError:
                print(f"Invalid data at line {line_number}: {raw}")
                continue

            if not value.is_integer():
                print(f"Invalid data at line {line_number}: not an integer -> {raw}")
                continue

            numbers.append(int(value))

    return numbers


def to_binary(number):
    """Converts an integer to binary string using basic division."""
    if number == 0:
        return "0"

    sign = ""
    n = number
    if n < 0:
        sign = "-"
        n = -n

    bits = []
    while n > 0:
        remainder = n % 2
        bits.append(str(remainder))
        n //= 2

    bits.reverse()
    return sign + "".join(bits)


def to_hex(number):
    """Converts an integer to hexadecimal string using basic division."""
    if number == 0:
        return "0"

    sign = ""
    n = number
    if n < 0:
        sign = "-"
        n = -n

    digits = []
    while n > 0:
        remainder = n % 16
        digits.append(HEX_DIGITS[remainder])
        n //= 16

    digits.reverse()
    return sign + "".join(digits)


def get_results_path(input_file):
    """Builds the output file path based on the input file name."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(current_dir, "..", "results")

    input_name = os.path.basename(input_file)
    base_name, _ = os.path.splitext(input_name)
    result_file = f"{base_name}_Results_generated.txt"

    if os.path.isdir(results_dir):
        return os.path.join(results_dir, result_file)

    return result_file


def main():
    """Main execution function for P2."""
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py input_file.txt")
        return

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print(f"Error: file not found -> {input_file}")
        return

    numbers = read_integers(input_file)
    elapsed_time = time.time() - start_time

    if len(numbers) == 0:
        print("No valid integer data found.")
        print(f"TIME_ELAPSED_SECONDS\t{elapsed_time}")
        return

    # Fixed-width column settings
    item_width = 6
    number_width = 12
    binary_width = 28
    hex_width = 10

    header = (
        f"{'ITEM':<{item_width}}"
        f"{'NUMBER':<{number_width}}"
        f"{'BINARY':<{binary_width}}"
        f"{'HEX':<{hex_width}}"
    )

    results = [header]

    item_index = 0
    for n in numbers:
        item_index += 1
        binary_value = to_binary(n)
        hex_value = to_hex(n)

        line = (
            f"{item_index:<{item_width}}"
            f"{n:<{number_width}}"
            f"{binary_value:<{binary_width}}"
            f"{hex_value:<{hex_width}}"
        )
        results.append(line)

    results.append(f"TIME_ELAPSED_SECONDS\t{elapsed_time}")

    for line in results:
        print(line)

    output_path = get_results_path(input_file)
    with open(output_path, "w", encoding="utf-8") as output_file:
        for line in results:
            output_file.write(line + "\n")


if __name__ == "__main__":
    main()
