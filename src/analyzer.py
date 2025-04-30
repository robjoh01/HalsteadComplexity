"""
Analyzer module for analyzing code for complexity.
"""

import csv
import os
from rich.console import Console
from rich.table import Table
from rich import box
from utils import (
    calc_score_and_grade,
    extract_version,
    remove_path_prefix,
    extract_date_from_quarterly_path
)
from halstead import (
    calc_loc_metrics,
    calc_halstead_metrics,
    calc_keyword_frequency,
    calc_average_line_length,
)

console = Console()

class Result:
    """
    An object to hold the analysis results.
    """
    def __init__(self, filepath, loc_metrics, halstead_metrics, keyword_frequency, avg_line_length):
        self.filepath = remove_path_prefix(filepath, 'plotly/python')
        self.date = extract_date_from_quarterly_path(filepath)
        self.version  = extract_version(filepath)
        self.loc_metrics = loc_metrics
        self.halstead_metrics = halstead_metrics
        self.keyword_frequency = keyword_frequency
        self.avg_line_length = avg_line_length
        self.score, self.grade = calc_score_and_grade(loc_metrics, halstead_metrics, keyword_frequency, avg_line_length)

    def write_to_file(self, output_file):
        """
        Write the analysis results to a file.

        Args:
            output_file (str): The path to the output file.

        Returns:
            None
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as file:
            file.write("Code Analysis Report\n")
            for section, data in {
                "LOC Metrics": self.loc_metrics,
                "Halstead Metrics": self.halstead_metrics,
                "Keyword Frequency": self.keyword_frequency,
            }.items():
                file.write(f"\n{section}:\n")
                for key, value in data.items():
                    file.write(f"{key}: {value:.2f}\n" if isinstance(value, float) else f"{key}: {value}\n")
            file.write(f"\nAverage Line Length: {self.avg_line_length:.2f} characters\n")
            file.write(f"\nFinal Score: {self.score}/100\nGrade: {self.grade}\n")

    def write_to_csv(self, output_file):
        """
        Write the analysis results to a CSV file.

        Args:
            output_file (str): The path to the output file.

        Returns:
            None
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Section", "Metric", "Value"])
            for section, data in {
                "LOC Metrics": self.loc_metrics,
                "Halstead Metrics": self.halstead_metrics,
                "Keyword Frequency": self.keyword_frequency,
            }.items():
                for key, value in data.items():
                    writer.writerow([section, key, f"{value:.2f}" if isinstance(value, float) else str(value)])
                writer.writerow([])
            writer.writerow(["Average Line Length", self.avg_line_length])
            writer.writerow(["Final Score", self.score])
            writer.writerow(["Grade", self.grade])

    def print_to_console(self):
        """
        Print the analysis results to the console.

        Returns:
            None
        """

        console.print("\n[bold underline]Code Analysis Report[/bold underline]\n", style="green")

        def create_table(title, data):
            table = Table(title=title, box=box.SIMPLE)
            table.add_column("Metric", justify="left", style="cyan", no_wrap=True)
            table.add_column("Value", justify="right", style="magenta")
            for key, value in data.items():
                table.add_row(key, f"{value:.2f}" if isinstance(value, float) else str(value))
            console.print(table)

        create_table("LOC Metrics", self.loc_metrics)
        create_table("Halstead Metrics", self.halstead_metrics)
        create_table("Keyword Frequency", self.keyword_frequency)
        console.print(f"[bold]Average Line Length:[/bold] [magenta]{self.avg_line_length:.2f} characters[/magenta]\n")
        console.print(f"[bold cyan underline]Final Score:[/bold cyan underline] [bright_cyan bold]{self.score}/100[/bright_cyan bold]")
        console.print(f"[bold magenta underline]Grade:[/bold magenta underline] [bright_magenta bold]{self.grade}[/bright_magenta bold]")

def combine_results_to_csv(results, output_path):
    """
    Combine multiple analysis results into a single CSV file.

    Args:
        results (list): List of tuples containing (filename, Result object)
        output_path (str): Path to the output CSV file
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header row
        writer.writerow(["Filepath", "Filename", "Date", "Version", "Section", "Metric", "Value"])

        # Write data for each file
        for filename, result in results:
            # Add LOC metrics
            for key, value in result.loc_metrics.items():
                writer.writerow([result.filepath, filename, result.date, result.version, "LOC Metrics", key, f"{value:.2f}" if isinstance(value, float) else str(value)])

            # Add Halstead metrics
            for key, value in result.halstead_metrics.items():
                writer.writerow([result.filepath, filename, result.date, result.version, "Halstead Metrics", key, f"{value:.2f}" if isinstance(value, float) else str(value)])

            # Add keyword frequency
            for key, value in result.keyword_frequency.items():
                writer.writerow([result.filepath, filename, result.date, result.version, "Keyword Frequency", key, f"{value:.2f}" if isinstance(value, float) else str(value)])

            # Add average line length
            writer.writerow([result.filepath, filename, result.date, result.version, "General", "Average Line Length", f"{result.avg_line_length:.2f}"])

            # Add score and grade
            writer.writerow([result.filepath, filename, result.date, result.version, "Results", "Final Score", result.score])
            writer.writerow([result.filepath, filename, result.date, result.version, "Results", "Grade", result.grade])

            # Add a blank row between files for better readability
            writer.writerow([])

def analyze_code(file_path, output_file=None, csv=False, silent=False):
    """
    Analyze the code in the given file and print or save the results.

    Args:
        file_path (str): The path to the file to analyze.
        output_file (str): The path to the output file (optional).

    Returns:
        None
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    result = Result(
        file_path,
        calc_loc_metrics(lines),
        calc_halstead_metrics(lines),
        calc_keyword_frequency(lines),
        calc_average_line_length(lines)
    )

    if output_file:
        if csv:
            result.write_to_csv(output_file)
        else:
            result.write_to_file(output_file)
    else:
        if not silent:
            result.print_to_console()

    return result
