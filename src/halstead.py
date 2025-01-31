"""
Halstead Complexity Metrics Module
"""

import re
import math

from collections import Counter

KEYWORDS = {
    'if',
    'else',
    'for',
    'while',
    'return',
    'import',
    'def',
    'class',
    'try',
    'except',
    'with',
    'lambda'
}

OPERATORS = {
    '+',
    '-',
    '*',
    '/',
    '=',
    '==',
    '<',
    '>',
    '&&',
    '||',
    '!',
    '(',
    ')',
    '{',
    '}',
    '[',
    ']',
    ',',
    ';'
}

def calc_loc_metrics(lines: list) -> dict:
    """
    Calculate Line of Code (LOC) metrics.

    Args:
        lines (list): List of code lines.

    Returns:
        dict: Dictionary containing LOC metrics.
    """

    total_lines = len(lines)
    blank_lines = sum(1 for line in lines if line.strip() == "")
    comment_lines = sum(1 for line in lines if line.strip().startswith("#"))
    code_lines = total_lines - blank_lines - comment_lines
    
    return {
        'Total Lines': total_lines,
        'Blank Lines': blank_lines,
        'Comment Lines': comment_lines,
        'Code Lines': code_lines
    }

def calc_halstead_metrics(lines: list) -> dict:
    """
    Calculate Halstead complexity metrics.

    Args:
        lines (list): List of code lines.

    Returns:
        dict: Dictionary containing Halstead metrics.
    """

    code_text = " ".join(lines)
    tokens = re.findall(r'\b\w+\b|\S', code_text)
    
    operands = set(re.findall(r'\b\w+\b', code_text))

    unique_operators = set(tok for tok in tokens if tok in OPERATORS)
    unique_operands = operands
    
    # Halstead calculations
    n1 = len(unique_operators)
    n2 = len(unique_operands)
    N1 = sum(1 for tok in tokens if tok in OPERATORS)
    N2 = sum(1 for tok in tokens if tok in operands)
    
    vocabulary = n1 + n2
    length = N1 + N2
    volume = length * math.log2(vocabulary) if vocabulary > 0 else 0
    difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
    effort = difficulty * volume
    
    return {
        'Unique Operators': n1,
        'Unique Operands': n2,
        'Total Operators': N1,
        'Total Operands': N2,
        'Vocabulary': vocabulary,
        'Length': length,
        'Volume': volume,
        'Difficulty': difficulty,
        'Effort': effort
    }

def calc_keyword_frequency(lines: list) -> dict:
    """
    Calculate keyword frequency.

    Args:
        lines (list): List of code lines.

    Returns:
        dict: Dictionary containing keyword frequency.
    """

    tokens = re.findall(r'\b\w+\b', " ".join(lines))
    keyword_counts = Counter(tok for tok in tokens if tok in KEYWORDS)
    
    return keyword_counts or Counter({"None": 0})

def calc_average_line_length(lines: list) -> float:
    """
    Calculate the average line length.

    Args:
        lines (list): List of code lines.

    Returns:
        float: Average line length.
    """

    non_blank_lines = [line for line in lines if line.strip()]
    avg_length = sum(len(line) for line in non_blank_lines) / len(non_blank_lines) if non_blank_lines else 0
    return avg_length
