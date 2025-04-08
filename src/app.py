"""
App module
"""

import argparse

def get_arguments():
    """
    Get the command line arguments.

    Args:
        -i, --input: Path to a single input file containing code to analyze.
        -o, --output: Path to a single output file (leave blank to display on console).
        -b, --batch: Enables batch mode for multiple input/output files.
        -il, --input-list: Path to a text file containing a list of input file paths.
        -ol, --output-list: Path to a text file containing a list of output file paths.

    Returns:
        args: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="Halstead Complexity Analyzer",
        description="Analyze code for complexity."
    )

    # Single file mode
    parser.add_argument(
        "-i", "--input",
        type=str,
        help="Path to a single input file containing code to analyze."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Path to a single output file or combined output in batch mode (leave blank to display on console)."
    )

    # Batch mode
    parser.add_argument(
        "-b", "--batch",
        action="store_true",
        help="Enable batch mode for multiple input/output files."
    )
    parser.add_argument(
        "-il", "--input-list",
        type=str,
        help="Path to a text file containing a list of input file paths (used with --batch)."
    )
    parser.add_argument(
        "-ol", "--output-list",
        type=str,
        help="Path to a text file containing a list of output file paths (used with --batch)."
    )

    return parser.parse_args()
