"""
Main module
"""

import os

from rich.console import Console

from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

from app import get_arguments
from analyzer import analyze_code

console = Console()

if __name__ == "__main__":
    args = get_arguments()

    # Determine input and output file paths
    input_path = args.input
    output_path = args.output # If not provided, display on console

    # Ask for input file path if not provided as an argument
    if not input_path:
        input_path = prompt("Enter the path to the input file (e.g., 'example_code.txt'): ", completer=PathCompleter())

    # Ensure the input file exists
    if not os.path.exists(input_path):
        console.print(f"[red]Error: The input file '{input_path}' does not exist.[/red]")
        exit(1)

    # Determine output file path (optional)
    if output_path == "":
        output_path = None
    elif not output_path:
        output_path = prompt("Enter the path for the output file (leave blank to display on console): ", completer=PathCompleter())
        output_path = output_path if output_path.strip() else None

    # Ensure directory for output file exists if provided
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Call analyze_code with the specified files
    analyze_code(input_path, output_path)