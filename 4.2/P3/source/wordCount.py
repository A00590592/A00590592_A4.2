"""
P3 - Word Count

Reads a text file and counts how many times each word appears.

Rules:
- Invoked from command line
- Receives an input file as parameter
- Prints results to screen and writes them to an output file
- Invalid data is reported and execution continues
- Words are separated by whitespace (spaces, tabs, newlines)

Usage:
    python wordCount.py fileWithData.txt
"""
# -----------------------------------------------------------------------------
# pylint_P3_v1
# Pylint notes:
    # - W0612: Unused variable 'start_time' (unused-variable):
    #   Code is corrected to include de use of 'start_time'
    #   as requested.
    # - C0305: Trailing newlines (trailing-newlines)
    #   Aditional lines are the end of the code are eliminated.
    # -----------------------------------------------------------------------------
# pylint: disable=invalid-name

import os
import sys
import time


def get_results_path(input_file: str) -> str:
    """Builds the output file path based on the input file name."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(current_dir, "..", "results")

    input_name = os.path.basename(input_file)
    base_name, _ = os.path.splitext(input_name)
    result_file = f"{base_name}_Results_generated.txt"

    if os.path.isdir(results_dir):
        return os.path.join(results_dir, result_file)

    return result_file


def count_words(file_path: str) -> tuple[dict[str, int], int]:
    """
    Counts word frequency in a text file.
    Words are defined as tokens separated by whitespace.
    """
    frequencies: dict[str, int] = {}
    total_words = 0

    with open(file_path, "r", encoding="utf-8") as file:
        line_number = 0
        for line in file:
            line_number += 1
            raw = line.strip()

            if raw == "":
                print(f"Invalid data at line {line_number}: empty")
                continue

            tokens = raw.split()

            for token in tokens:
                total_words += 1
                frequencies[token] = frequencies.get(token, 0) + 1

    return frequencies, total_words


def format_results(frequencies: dict[str, int], total_words: int) -> list[str]:
    """Formats the results with aligned columns."""
    word_width = 20
    count_width = 8

    sorted_items = sorted(frequencies.items(), key=lambda item: (-item[1], item[0]))

    lines: list[str] = []
    for word, count in sorted_items:
        lines.append(f"{word:<{word_width}}{count:>{count_width}}")

    lines.append(f"{'Grand Total':<{word_width}}{total_words:>{count_width}}")
    return lines


def main() -> None:
    """Main execution function for P3."""
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Usage: python wordCount.py input_file.txt")
        return

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print(f"Error: file not found -> {input_file}")
        return

    frequencies, total_words = count_words(input_file)

    elapsed_time = time.time() - start_time

    if total_words == 0:
        print("No valid data found.")
        print(f"TIME_ELAPSED_SECONDS\t{elapsed_time}")
        return

    results = format_results(frequencies, total_words)
    results.append(f"TIME_ELAPSED_SECONDS\t{elapsed_time}")

    for line in results:
        print(line)

    output_path = get_results_path(input_file)
    with open(output_path, "w", encoding="utf-8") as output_file:
        for line in results:
            output_file.write(line + "\n")


if __name__ == "__main__":
    main()
