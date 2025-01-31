"""
App module
"""

import argparse

def get_arguments():
    """
    Get the command line arguments.

    Args:
        -i --input: Path to the input file containing code to analyze.
        -o --output: Path to the output file (leave blank to display on console).

    Returns:
        args: The command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="Halstead Complexity Analyzer",
        description="Analyze code for complexity."
    )

    parser.add_argument(
        "-i", "--input",
        type=str,
        help="Path to the input file containing code to analyze."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Path to the output file (leave blank to display on console)."
    )

    args = parser.parse_args()

    return args
