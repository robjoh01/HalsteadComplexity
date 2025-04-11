"""
Main module
"""

import os

from rich.console import Console
from prompt_toolkit import prompt
from prompt_toolkit.completion import PathCompleter

from app import get_arguments
from analyzer import analyze_code
from analyzer import combine_results_to_csv

console = Console()

def handle_single_file_mode(input_path, output_path, silent=False):
    """
    Handle single file mode.

    Args:
        input_path (str): The path to the input file.
        output_path (str): The path to the output file.

    Returns:
        None
    """
    # Ask for input file path if not provided as an argument
    if not input_path:
        input_path = prompt("Enter the path to the input file (e.g., 'example_code.txt'): ", completer=PathCompleter())

    # Ensure the input file exists
    if not os.path.exists(input_path):
        console.print(f"[red]Error: The input file '{input_path}' does not exist.[/red]")
        exit(1)

    # Ask for output file path if not provided
    if output_path == "":
        output_path = None
    elif not output_path:
        output_path = prompt("Enter the path for the output file (leave blank to display on console): ", completer=PathCompleter())
        output_path = output_path.strip() if output_path.strip() else None

    # Ensure directory for output file exists if provided
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Check if output file is a CSV
    csv = output_path and output_path.endswith(".csv")

    # Call analyze_code with the specified files
    analyze_code(input_path, output_path, csv, silent)

def handle_batch_mode(input_list_path, output_list_path=None, combined_output_path=None, silent=False):
    """
    Handle batch mode for multiple input/output files.

    Args:
        input_list_path (str): The path to the input list file.
        output_list_path (str): The path to the output list file.
        combined_output_path (str): Path to save combined results to a single file.

    Returns:
        None
    """
    # Validate input list file
    if not os.path.exists(input_list_path):
        console.print(f"[red]Error: The input list file '{input_list_path}' does not exist.[/red]")
        exit(1)

    # Read input file paths
    with open(input_list_path, "r") as file:
        input_files = [line.strip() for line in file.readlines() if line.strip()]

    if combined_output_path:
        # Combined output mode
        all_results = []

        # Process each input file and collect the results
        for input_path in input_files:
            if not os.path.exists(input_path):
                console.print(f"[yellow]Warning: Skipping '{input_path}' (file not found).[/yellow]")
                continue

            # Get the filename for identification in the combined output
            filename = os.path.basename(input_path)

            # Analyze the file and get the result
            result = analyze_code(input_path, None, False, silent)
            all_results.append((filename, result))

            # Print status
            console.print(f"Analyzed [cyan]{input_path}[/cyan]")

        # Save all results to a single CSV file
        combine_results_to_csv(all_results, combined_output_path)
        console.print(f"[green]Combined results saved to {combined_output_path}[/green]")

    else:
        # Individual output files mode
        # If an output list file is provided, read output file paths
        output_files = []
        if output_list_path:
            if not os.path.exists(output_list_path):
                console.print(f"[red]Error: The output list file '{output_list_path}' does not exist.[/red]")
                exit(1)
            with open(output_list_path, "r") as file:
                output_files = [line.strip() for line in file.readlines() if line.strip()]
            # Ensure input and output lists are the same length
            if len(input_files) != len(output_files):
                console.print("[red]Error: The number of input and output files must match.[/red]")
                exit(1)
        else:
            output_files = [None] * len(input_files)  # Output to console if no output list is provided

        # Process each input file
        for input_path, output_path in zip(input_files, output_files):
            if not os.path.exists(input_path):
                console.print(f"[yellow]Warning: Skipping '{input_path}' (file not found).[/yellow]")
                continue
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Check if output file is a CSV
            csv_output = output_path and output_path.endswith(".csv")

            # Call analyze_code with the specified files
            analyze_code(input_path, output_path, csv_output, silent)

if __name__ == "__main__":
    args = get_arguments()

    if args.batch:
        if not args.input_list:
            console.print("[red]Error: --batch mode requires --input-list.[/red]")
            exit(1)

        # Check if a single output file is specified with -o
        if args.output and not args.output_list:
            handle_batch_mode(args.input_list, combined_output_path=args.output, silent=args.silent)
        else:
            handle_batch_mode(args.input_list, args.output_list, silent=args.silent)
    else:
        handle_single_file_mode(args.input, args.output, silent=args.silent)
